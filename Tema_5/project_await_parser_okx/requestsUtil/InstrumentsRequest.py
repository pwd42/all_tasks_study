from Tema_5.project_await_parser_okx.requestsUtil.BaseRequest import BaseRequest


class InstrumentsRequest(BaseRequest):
    def __init__(self):
        super().__init__()
        self.url = self.url + "instruments"
        self.params["instType"] = "SPOT"