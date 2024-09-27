import os

from .zephyr_client import ZephyrClient


class ZephyrReporter:
    enabled: bool = False
    server: str
    username: str
    password: str
    project_key: str
    run_id: str
    client: ZephyrClient
    run_created: bool = False

    @classmethod
    def setup(cls):
        cls.project_key = os.getenv("PROJECT_KEY")
        cls.server = os.getenv("JIRA_SERVER")
        cls.username = os.getenv("JIRA_USERNAME")
        cls.password = os.getenv("JIRA_TOKEN")

        if cls.server:
            cls.client = ZephyrClient(
                base_address=cls.server,
                token=cls.password,
                project_name=cls.project_key,
            )
            cls.enabled = True
