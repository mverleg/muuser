
from settings import LOGIN_REDIRECT_URL
from django.utils.http import is_safe_url
from django.core.urlresolvers import reverse


'''
    decorator to extract and validate the next page in the url, 
    and pass it as an argument, otherwise falling back to login url
    @next_GET_or(url)   (brackets also without arg)
'''
def next_GET_or(url_name):
    def next_GET(func):
        def func_with_next(request, *args, **kwargs):
            if url_name is None:
                next = LOGIN_REDIRECT_URL
            else:
                next = reverse(url_name)
            if 'next' in request.GET:
                if is_safe_url(url = request.GET['next'], host = request.get_host()):
                    next = request.GET['next']
            return func(request, *args, next = next, **kwargs)
        return func_with_next
    return next_GET

'''
    no argument version (so also no brackets)
'''
next_GET = next_GET_or(None)