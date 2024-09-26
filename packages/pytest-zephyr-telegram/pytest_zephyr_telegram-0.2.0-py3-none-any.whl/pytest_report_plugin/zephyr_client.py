import logging
from typing import Optional, BinaryIO, List, Dict, Any, Union

import requests
from requests import Response

logger = logging.getLogger(__name__)


class ZephyrClient:

    def __init__(self, base_address: str, token: str, project_name: str):
        self.base_url = f"{base_address}/rest/atm/1.0"
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base_address = base_address
        self.project_name = project_name
        self.logger = logging.getLogger(__name__)

    def create_run(self, name: str) -> Optional[str]:
        data = {
            "projectKey": self.project_name,
            "name": name,
        }

        resp = requests.request(
            url=self.base_url + "/testrun",
            json=data,
            method="POST",
            headers=self.headers,
        )
        if resp.status_code == 201:
            return resp.json()["key"]
        self.logger.error(resp.content, "не удалось создать прогон zephyr")
        return None

    # pylint: disable=too-many-arguments
    def post_result(
        self,
        run_id: str,
        case_id: str,
        status: str,
        time: float,
        start_time: str,
        end_time: str,
        comment: str,
        environment: str,
        issues=None,
    ) -> Optional[Response]:
        if issues is None:
            issues = []
        data = {
            "status": status,
            "comment": comment,
            "environment": environment,
            "executionTime": time,  # 18000
            "actualStartDate": start_time,  # 2016-02-14T19:22:00+0300
            "actualEndDate": end_time,  # 2016-02-15T19:22:00+0300
            "issueLinks": issues,
        }
        # noinspection PyBroadException
        try:
            return requests.request(
                url=f"{self.base_url}/testrun/{run_id}/testcase/{case_id}/testresult",
                json=data,
                headers=self.headers,
                method="POST",
            )
        except Exception as e:
            self.logger.error(e.__str__())
            return None

    def _upload_file_by_name(
        self, request_url: str, attachment: str, filename: str
    ) -> bool:

        if not filename:
            raise SyntaxError("No filename given.")
        try:
            fp = open(attachment, "rb")
        except OSError as ex:
            logger.error("attachment failed. %s", ex)
            return False
        success = self._upload_file(request_url, fp, filename)
        fp.close()
        return success

    def get_test_results(self, test_run_key: str) -> List[Dict[str, Any]]:
        res = requests.request(
            method="GET",
            url=f"{self.base_url}/testrun/{test_run_key}/testresults",
            headers=self.headers,
        )
        if not res:
            return []
        results = res.json()
        for result in results:
            if len(result["scriptResults"]) > 1:
                result["scriptResults"] = sorted(
                    result["scriptResults"], key=lambda result: result["index"]
                )
        return results

    def get_test_result(self, test_run_key: str, test_case_key: str) -> Dict[str, Any]:
        response = self.get_test_results(test_run_key)
        return (
            max(
                (item for item in response if item["testCaseKey"] == test_case_key),
                key=lambda item: item["id"],
                default={},
            )
            or {}
        )

    def add_test_result_attachment(
        self,
        test_run_key: str,
        test_case_key: str,
        attachment: Union[str, BinaryIO],
        filename: str = "",
    ) -> bool:
        test_result_id = self.get_test_result(test_run_key, test_case_key)["id"]
        path = f"/testresult/{test_result_id}/attachments"
        return (
            self._upload_file_by_name(path, attachment, filename)
            if isinstance(attachment, str)
            else self._upload_file(path, attachment, filename)
        )

    def _upload_file(
        self, request_url: str, attachment: BinaryIO, filename: str
    ) -> bool:
        files = {"file": (filename, attachment, "application/octet-stream")}
        try:
            response = requests.request(
                url=request_url,
                files=files,
                headers={**self.headers, "X-Atlassian-Token": "nocheck"},
                method="POST",
            )
            response.raise_for_status()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
        ) as ex:
            logger.error("request failed. %s", ex)
            return False

        return True
