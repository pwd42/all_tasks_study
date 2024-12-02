from Tema_5.project_await_parser_okx.requestsUtil.BaseRequest import BaseRequest


class PriceLimitRequest(BaseRequest):
    def __init__(self, ticker):
        super().__init__()
        self.url = self.url + "price-limit"
        self.params["instId"] = ticker