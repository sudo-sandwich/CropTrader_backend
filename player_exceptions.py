class PlayerException(Exception):
    # should never get this exception, if you do it means i messed up
    exception_id = 0

class NotEnoughMoneyException(PlayerException):
    exception_id = 1

class NotEnoughProductsException(PlayerException):
    exception_id = 2

class NotEnoughSeedsException(PlayerException):
    exception_id = 3

class PlotNotEmptyException(PlayerException):
    exception_id = 4

class PlotNotLargeEnoughException(PlayerException):
    exception_id = 5

class PlotNotReadyException(PlayerException):
    exception_id = 6