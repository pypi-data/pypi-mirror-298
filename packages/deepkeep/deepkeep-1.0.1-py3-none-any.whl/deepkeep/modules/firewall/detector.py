from ..base_module import BaseModule
from .templates import Templates


class Detector(BaseModule):
    root_path: str = "firewall/detector"
    templates: Templates

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.templates = Templates(self._client)

    def add(self, firewall_id: str, detector_template_id: str):
        """
        Add a detector to a firewall
        :param firewall_id: str: firewall id
        :param detector_template_id: str: detector template id
        :return: dict: response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/{firewall_id}/{detector_template_id}")
