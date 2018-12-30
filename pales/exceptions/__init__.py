class PalesException(BrokenPipeError):
    def __init__(self, message, *args):
        self.message = message
        super(PalesException, self).__init__(message, *args)
