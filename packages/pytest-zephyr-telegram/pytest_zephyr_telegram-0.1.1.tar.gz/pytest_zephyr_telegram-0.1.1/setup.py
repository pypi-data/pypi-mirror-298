from setuptools import setup

setup(
    name='pytest-zephyr-telegram',
    version='0.1.1',
    description='Плагин для отправки данных автотестов в Телеграм и Зефир',
    author='slug',
    author_email='',
    py_modules=['plugin'],
    install_requires=[
        'pytest == 8.3.2',
        'pytelegrambotapi == 4.22.1',
        'emoji == 2.7.0',
        'pytz == 2024.1',
        'curlify == 2.2.1',
        'allure-pytest == 2.13.5',
    ],
    entry_points={'pytest11': ['zephyr_telegram = plugin']},
)