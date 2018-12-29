class CarmentaException(BrokenPipeError):
    def __init__(self, message, *args):
        self.message = message
        super(CarmentaException, self).__init__(message, *args)


class InvalidJunoObject(CarmentaException):
    def __init__(self, message, *args):
        self.message = message
        super(InvalidJunoObject, self).__init__(message, *args)
