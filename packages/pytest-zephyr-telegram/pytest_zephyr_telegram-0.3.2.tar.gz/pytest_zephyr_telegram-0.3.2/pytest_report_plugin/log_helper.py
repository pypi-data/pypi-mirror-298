import json
import logging
import os
from functools import wraps

import allure
import curlify
from requests import Response

logger = logging.getLogger(__name__)

logs = {}


# pylint: disable=line-too-long
def log_http(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        is_response = isinstance(result, Response)
        if not is_response:
            return result

        # формирование текста для логирования
        status_code_text = f" \n\r {result.status_code}"
        response_json = (
            f" \n\r {json.dumps(result.json(), indent=4)}"
            if "Content-Type" in result.headers
            and "application/json" in result.headers["Content-Type"]
            and len(result.content) > 0
            else ""
        )
        curl_text = f" {curlify.to_curl(result.request)}"
        response_url = f" \n\r {result.url}"

        logger.info("****** Начало HTTP запроса ******")
        logger.info(curl_text)

        result_text = (
            f"""
            {response_url} {status_code_text}
            {response_json}
            """
            if result is not None
            else "Пустое тело ответа"
        )

        logger.info(result_text)
        logger.info("****** Конец HTTP запроса ******")

        jira_server = os.getenv("JIRA_SERVER")

        if jira_server and jira_server not in result.url:
            attach_res = "" if result is None else result
            allure.attach(
                body=str(attach_res),
                name=curl_text,
                attachment_type=allure.attachment_type.TEXT,
            )

            # сбор логов запроса
            if is_response:
                try:
                    test_name = (
                        os.environ.get("PYTEST_CURRENT_TEST")
                        .split(":")[-1]
                        .split(" ")[0]
                    )
                    log = f"{curl_text} {status_code_text}\n"
                    if result.content:
                        log += f"{result.text}\n"
                    logs.setdefault(test_name, []).append(log)
                except Exception:
                    pass

        return result

    return wrapper


# Экспортируем функцию log_http
__all__ = ["log_http"]
