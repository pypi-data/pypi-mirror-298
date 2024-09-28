'''
errors for egger
'''
class EggerError(Exception):
    '''
    base error class for egger
    '''
    pass

class BadArgumentsError(EggerError):
    '''
    error raised when arguments provided are bad
    '''
    pass
