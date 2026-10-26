class UnauthorizedError(Exception):
    def __init__(self, message="Unauthorized: service token is missing or invalid"):
        super().__init__(message)


class ForbiddenError(Exception):
    def __init__(self, message="Forbidden: token does not have sufficient permissions"):
        super().__init__(message)


class RateLimitError(Exception):
    def __init__(self, message="Rate limit exceeded. Please try again later."):
        super().__init__(message)
