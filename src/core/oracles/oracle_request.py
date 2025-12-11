class OracleRequest:
    _TOTAL_REQUESTS: int = 0
    _REQUEST_WITH_SUCCESS: int = 0

    @classmethod
    def set_total_requests(cls, total_requests: int) -> None:
        cls._TOTAL_REQUESTS = total_requests

    @classmethod
    def get_total_requests(cls) -> int:
        return cls._TOTAL_REQUESTS

    @classmethod
    def register_new_success_request(cls):
        cls._REQUEST_WITH_SUCCESS += 1

    @classmethod
    def get_success_request(cls) -> int:
        return cls._REQUEST_WITH_SUCCESS

    @classmethod
    def get_rate_success(cls) -> float:
        return cls._REQUEST_WITH_SUCCESS / cls._TOTAL_REQUESTS

    @classmethod
    def get_error_request(cls) -> int:
        return cls._TOTAL_REQUESTS - cls._REQUEST_WITH_SUCCESS

    @classmethod
    def get_rate_error_request(cls) -> float:
        return (cls._TOTAL_REQUESTS - cls._REQUEST_WITH_SUCCESS) / cls._TOTAL_REQUESTS

    @classmethod
    def reset(cls) -> None:
        cls._REQUEST_WITH_SUCCESS = 0