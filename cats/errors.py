class CatsError(Exception):
    pass


class RouteError(CatsError):
    pass


class ControllerConflict(CatsError):
    pass

