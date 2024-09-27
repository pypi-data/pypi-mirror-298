### Как настроить отчетность Telegram
Для включения отчетности Telegram добавить вашего бота в чат отчетов,
передать при запуске 
--telegram-token="..." чат для отправки
--telegram_id="..." токен бота    

### Как настроить отчетность Zephyr
Для включения отчетности Zephyr добавить переменные окружения
PROJECT_KEY
JIRA_SERVER
JIRA_USERNAME
JIRA_TOKEN

расставить декораторы с ключами тесткейсов над тестами:
@pytest.mark.testcase(test_case_key="T3260")
@pytest.mark.project(project_key="RNDAGB") - если проект тесткейса отличается от PROJECT_KEY

для кастомазиции имени прогона в Zephyr задать переменную окружения RUN_PREFIX_NAME