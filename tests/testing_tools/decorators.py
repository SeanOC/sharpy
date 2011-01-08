from nose.tools import make_decorator

from utils import clear_users as clear_users_func

def clear_users(func):
    '''
    Calls cheddar's delete all users method no matter the test result
    '''
    def new(*args, **kwargs):
        raised_exception = None
        try:
            func(*args, **kwargs)
        except Exception, e:
            clear_users_func()
            raise
            
        clear_users_func()
    
    new = make_decorator(func)(new)
        
    return new