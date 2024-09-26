import logging
import tempfile
from datetime import datetime
from os import getenv

import emoji
import pytest
import pytz
from _pytest.fixtures import FixtureRequest
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from pluggy._result import _Result
from telebot.formatting import escape_html
from telebot.util import MAX_MESSAGE_LENGTH
from pytest_report_plugin.log_helper import log_http
from pytest_report_plugin.telegram import TelegramReporter
from pytest_report_plugin.zephyr import ZephyrReporter

ENV_STAGING_NAME = "DEV"
RUN_PREFIX_NAME = ""
logger = logging.getLogger(__name__)


__all__ = ["log_helper", "log_http"]


# для хранения информации о тестах
class TestState:
    def __init__(self):
        self.failed_tests = {}


test_state = TestState()


def pytest_addoption(parser):
    parser.addoption("--reports", action="store_true", help="включает плагин")
    parser.addoption("--zephyr-url", action="store", default=None, help="Zephyr URL")
    parser.addoption("--telegram-token", action="store", default=None, help="Telegram token")
    parser.addoption("--telegram_id", action="store", dest="telegram_id", default=None, help="Id of telegram chat")
    parser.addoption("--telegram_token", action="store", dest="telegram_token", default=None, help="telegram token")
    parser.addini('markers', type='linelist', help='markers')


def pytest_configure(config):
    global ENV_STAGING_NAME
    global RUN_PREFIX_NAME
    telegram_chat_id = config.getoption("--telegram_id")
    telegram_token = config.getoption("--telegram-token")
    ZephyrReporter.setup()
    if telegram_token:
        TelegramReporter.setup(True, telegram_chat_id, telegram_token)
    else:
        TelegramReporter.enabled = False
    ENV_STAGING_NAME = getenv("STAGING_NAME", default="DEV")
    RUN_PREFIX_NAME = getenv("RUN_PREFIX_NAME", default="CCT API")

    config.addinivalue_line(
        'markers',
        'testcase(test_case_key): тесткейс в Зефире'
    )
    config.addinivalue_line(
        'markers',
        'project(project_key): проект тесткейса в Зефире, если он отличается от PROJECT_KEY в енв.переменных'
    )



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo):
    outcome: _Result = yield  # тест выполняется
    rep: TestReport = outcome.get_result()

    # отправка результатов в Телеграм, в реальном времени по каждой ошибке
    if rep.failed and rep.when != "teardown":

        # не отправляем данные в телеграм если тест упал первый раз
        # а также не отправляем если эта ошибка уже была отправлена
        # (отправляем только если ошибка повторилась на перезапуске)
        if item.nodeid not in test_state.failed_tests:
            test_state.failed_tests.update({item.nodeid: False})
            return

        if not test_state.failed_tests.get(item.nodeid):
            send_exception_to_telegramm(call, item)
            test_state.failed_tests.update({item.nodeid: True})

    # отправка результата теста в Зефир
    if ZephyrReporter.enabled:
        send_zephyr_result(item, call, outcome, rep)

    # сбор логов запросов для Zephyr
    if call.when in ["teardown"]:
        testcase_id = extract_testcase_id(item)
        upload_http_logs_to_zephyr(item, testcase_id)


class TestState:
    def __init__(self):
        self.failed_tests = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter):
    yield

    if TelegramReporter.enabled:
        failed = len(terminalreporter.stats.get("failed", []))
        passed = len(terminalreporter.stats.get("passed", []))
        skipped = len(terminalreporter.stats.get("skipped", []))
        error = len(terminalreporter.stats.get("error", []))

        chat_id = TelegramReporter.chat_id

        list_failed_amount = 10

        failed_tests = ""
        error_tests = ""
        if failed != 0:
            failed_tests = "\nFailed tests:\n"

            for failed_test in terminalreporter.stats.get("failed", [])[
                :list_failed_amount
            ]:
                failed_tests += f"{failed_test.nodeid}\n"

            if failed > list_failed_amount:
                failed_tests += "..."
        if error != 0:
            error_tests = "\nError tests:\n"

            for error_test in terminalreporter.stats.get("error", [])[
                :list_failed_amount
            ]:
                error_tests += f"{error_test.nodeid}\n"

            if error > list_failed_amount:
                error_tests += "..."
        final_results = (
            f"Passed={passed} Failed={failed} Skipped={skipped} Error={error}"
        )

        success_emoji = (
            emoji.emojize(":thumbs_up:")
            if error == 0 and failed == 0
            else emoji.emojize(":cross_mark:")
        )

        TelegramReporter.bot.send_message(
            chat_id=chat_id,
            text=f"""
                    {success_emoji}{final_results}
                    {failed_tests}
                    {error_tests}
                    """,
        )


@pytest.fixture(scope="session", autouse=True)
def report_start_run(request: FixtureRequest):
    now = datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d-%m-%Y %H:%M:%S")
    run_name = f"Автотесты CCT API {ENV_STAGING_NAME} {now}"
    if TelegramReporter.enabled:
        telegram_create_run(run_name)

    if ZephyrReporter.enabled:
        zephyr_create_run(run_name)


def extract_stacktrace(call: CallInfo):
    exception_text = str(call.excinfo.value)
    # Список атрибутов, которые нужно проверить и добавить к exception_text
    attributes = [
        "msg",
        "locator",
        "image",
        "text",
        "timeout",
        "full_image",
        "contains",
        "message",
        "x",
        "y",
    ]
    for attr in attributes:
        if hasattr(call.excinfo.value, attr):
            value = getattr(call.excinfo.value, attr)
            exception_text += f"\n {attr} {value}"
    exception_text = exception_text.split("\nStacktrace:")[0]
    return exception_text


def send_exception_to_telegramm(call, item):
    # сообщение об ошибке в Telegram и в Зефир
    if TelegramReporter.enabled:
        exception_text = extract_stacktrace(call)
        if len(exception_text) > MAX_MESSAGE_LENGTH:
            exception_text = exception_text.split("\n")[0]
        exception_text = escape_html(exception_text)
        message = f"""Имя теста: <code>{item.name}</code>\n
            Текст ошибки: <code>{exception_text} \n</code>"""
        # отправка в телеграмм
        try:
            TelegramReporter.bot.send_message(
                chat_id=TelegramReporter.chat_id, text=message
            )
        except Exception as e:
            logger.error(e.__str__())


def send_zephyr_result(
    item: Function, call: CallInfo, outcome: _Result, rep: TestReport
):
    if rep.failed and rep.when != "setup":

        if item.nodeid not in test_state.failed_tests:
            test_state.failed_tests.add(item.nodeid)
            return

    if (
        call.when != "setup"
        and call.when != "teardown"
        and ZephyrReporter.enabled
        and ZephyrReporter.run_created
    ):

        testcase_id = extract_testcase_id(item)

        if testcase_id is not None:
            status = "Pass" if outcome.get_result().passed else "Fail"
            error = "" if status == "Pass" else extract_stacktrace(call)
            time_zone = pytz.timezone("Europe/Moscow")
            start_time = datetime.fromtimestamp(call.start, time_zone).isoformat()
            end_time = datetime.fromtimestamp(call.stop, time_zone).isoformat()

            env = "DEV-branch" if ENV_STAGING_NAME == "dev" else "RC"

            ZephyrReporter.client.post_result(
                run_id=ZephyrReporter.run_id,
                case_id=testcase_id,
                environment=env,
                status=status,
                comment=error,
                start_time=start_time,
                end_time=end_time,
                time=call.duration * 1000,
            )


@pytest.fixture(scope="session", autouse=True)
def report_zephyr_link():
    report_run_link()
    yield
    report_run_link()


def report_run_link():
    if ZephyrReporter.enabled and TelegramReporter.enabled:
        test_run_key = ZephyrReporter.run_id
        if test_run_key:
            run_link = (
                f"{ZephyrReporter.server}/secure/Tests.jspa#/testPlayer/{test_run_key}"
            )
            TelegramReporter.bot.send_message(
                text=f"Прогон в Zephyr: {run_link}",
                chat_id=TelegramReporter.chat_id,
            )


def zephyr_create_run(run_name):
    run_id = ZephyrReporter.client.create_run(name=run_name)
    ZephyrReporter.run_created = True
    ZephyrReporter.run_id = run_id


def extract_testcase_id(item):
    testcase_id = None
    if hasattr(item, "callspec"):  # атрибут появляется если тест параметризрован
        # если case_id и issue_id есть в параметрах параметризированного теста, то берем их оттуда
        # в другом случае ищем их в декораторах
        parametrized_case_id = item.callspec.params.get("test_case_key")
        testcase_id = parametrized_case_id.__str__() if parametrized_case_id else None
    else:
        parametrized_case_id = None
    if not parametrized_case_id:
        for m in item.own_markers:
            if m.name == "testcase":
                testcase_id = m.kwargs["test_case_key"]
                break

        project_key = ZephyrReporter.project_key
        for m in item.own_markers:
            if m.name == "project":
                project_key = m.kwargs["project_key"]
                break
        testcase_id = f"{project_key}-{testcase_id}"
    return testcase_id


def upload_http_logs_to_zephyr(item, test_case_key):
    if ZephyrReporter.enabled:
        if item.funcargs.get("request"):
            request = item.funcargs["request"]
            try:
                if request.node:
                    test_name = request.node.name
                    test_log = "\n".join(log_helper.logs.get(test_name, []))
                    with tempfile.NamedTemporaryFile(
                        delete=False, mode="wb", suffix=".txt"
                    ) as temp_file:
                        temp_file.write(test_log.encode("utf-8"))
                        temp_file.seek(0)
                        ZephyrReporter.client.add_test_result_attachment(
                            ZephyrReporter.run_id,
                            test_case_key,
                            temp_file.name,
                            f"{test_name}.txt",
                        )
            except Exception as e:
                logger.error(f"Не удалось добавить логи в Zephyr {e}")


def telegram_create_run(run_name):
    global RUN_PREFIX_NAME
    message = f"""{emoji.emojize(":rocket:")} Тесты {RUN_PREFIX_NAME} запущены на {ENV_STAGING_NAME.upper()}\n<code>{run_name}</code>"""

    TelegramReporter.bot.send_message(chat_id=TelegramReporter.chat_id, text=message)
