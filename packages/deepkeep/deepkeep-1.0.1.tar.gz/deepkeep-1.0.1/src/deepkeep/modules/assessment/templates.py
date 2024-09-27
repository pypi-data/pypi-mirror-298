from ..base_module import BaseModule


class Templates(BaseModule):
    root_path: str = "assessment/report/templates"

    def get(self, assessment_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}")