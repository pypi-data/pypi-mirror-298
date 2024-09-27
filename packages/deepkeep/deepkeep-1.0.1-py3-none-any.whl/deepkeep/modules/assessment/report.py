from ..base_module import BaseModule
from .templates import Templates


class Report(BaseModule):
    root_path: str = "assessment/report"
    templates: Templates

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.templates = Templates(self._client)

    def add(self, assessment_id: str, report_template_id: str):
        return self._make_request(method="POST", path=f"{self.root_path}/{assessment_id}/{report_template_id}")

    def get(self, assessment_id: str, report_id: str = None):
        if report_id:
            return self._make_request(method="GET", path=f"{self.root_path}/{report_id}")
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}/list")

    def delete(self, report_id: str):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{report_id}")


