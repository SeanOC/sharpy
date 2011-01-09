

class CheddarError(Exception):
    "Base class for exceptions returned by cheddar"
    
    def __init__(self, response, content, *args, **kwargs):
        # Importing in method to break circular dependecy
        from sharpy.parsers import parse_error
        
        super(CheddarError, self).__init__(*args, **kwargs)
        error_info = parse_error(content)
        self.response = response
        self.error_info = error_info
        
    def __str__(self):
        return '%s (%s) %s - %s' % (
            self.response.status,
            self.error_info['aux_code'],
            self.response.reason,
            self.error_info['message'],
        )

class AccessDenied(CheddarError):
    "A request to cheddar returned a status code of 401"
    pass
    
class BadRequest(CheddarError):
    "A request to cheddar was invalid in some way"
    pass

class NotFound(CheddarError):
    "A request to chedder was made for a resource which doesn't exist"
    pass
    
class CheddarFailure(CheddarError):
    "A request to cheddar encountered an unexpected error on the cheddar side"
    pass
    
class PreconditionFailed(CheddarError):
    "A request to cheddar was made but failed CG's validation in some way."
    pass
    
class NaughtyGateway(CheddarError):
    """
    Cheddar either couldn't contact the gateway or the gateway did something
    very unexpected.
    """
    pass
    
class UnprocessableEntity(CheddarError):
    """
    An error occurred during processing. Please fix the error and try again.
    """
    pass
    
class ParseError(Exception):
    """
    Sharpy recieved unknown output from cheddar and doesn't know what
    to do with it.
    """
    pass