class RequestNotFoundError(Exception):
    pass

class RequestAlreadyProcessedError(Exception):
    pass

class DuplicateRoleRequestError(Exception):
    pass

class ForbiddenRoleRequestError(Exception):
    pass