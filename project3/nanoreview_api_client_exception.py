class NanoReviewApiClientException(Exception):
    def __init__(self, e: Exception):
        self.message = repr(e)
