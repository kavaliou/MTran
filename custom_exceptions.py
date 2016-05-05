class CustomException(Exception):
    def __unicode__(self):
        return self.message


class NotAssignedVariableError(CustomException):
    def __init__(self, value, lineno, message=None):
        if message is None:
            message = 'Error at line %s : Variable \'%s\' is not assigned.' % (lineno, value)
        super(NotAssignedVariableError, self).__init__(message)


class VariableOverridingError(CustomException):
    def __init__(self, value, lineno, message=None):
        if message is None:
            message = 'Error at line %s : Variable \'%s\' is assigned already.' % (lineno, value)
        super(VariableOverridingError, self).__init__(message)


class CustomZeroDivisionError(CustomException):
    def __init__(self, lineno, message=None):
        if message is None:
            message = 'Error at line %s : Divide by zero.' % lineno
        super(CustomZeroDivisionError, self).__init__(message)

