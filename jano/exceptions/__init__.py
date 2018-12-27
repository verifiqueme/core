class JunoException(BrokenPipeError):
    def __init__(self, message, *args):
        self.message = message
        super(JunoException, self).__init__(message, *args)


class NoAzureKey(JunoException):
    def __init__(self, message, *args):
        self.message = message
        super(NoAzureKey, self).__init__(message, *args)

class TextUnavailable(JunoException):
    def __init__(self, message, *args):
        self.message = message
        super(TextUnavailable, self).__init__(message, *args)
