from setuptools import setup

setup(
    name="pytest-zephyr-telegram",
    version="0.2.1",
    addopts=['--config', 'pytest.ini'],
    description="Плагин для отправки данных автотестов в Телеграм и Зефир",
    author="slug",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author_email="",
    py_modules=["pytest_report_plugin"],
    packages=["pytest_report_plugin"],
    package_data={"pytest_report_plugin": ["py.typed"]},
    entry_points={"pytest11": ["pytest-zephyr-telegram = pytest_report_plugin"]},
    install_requires=[
        "pytest == 8.3.2",
        "pytelegrambotapi == 4.22.1",
        "emoji == 2.7.0",
        "pytz == 2024.1",
        "curlify == 2.2.1",
        "allure-pytest == 2.13.5",
    ],
)
