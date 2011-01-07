
class AccessDenied(Exception):
    "A request to cheddar returned a status code of 401"
    pass
    
class BadRequest(Exception):
    "A request to cheddar was invalid in some way"
    pass

class NotFound(Exception):
    "A request to chedder was made for a resource which doesn't exist"
    pass