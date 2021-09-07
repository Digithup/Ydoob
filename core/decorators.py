import functools
import logging
import time

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect

from DNigne import settings


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = [ 'vendor']

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home:Error403')

        return wrapper_func

    return decorator
def vendor_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name



        if group == 'vendor':
            return redirect('home:Error403')

        if group == 'customer':
            return view_func(request, *args, **kwargs)

    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name



        if group == 'customer':
            return redirect('home:Error403')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function


def allow_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:Error403')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def superuser_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner


def superuser_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url='account_login_url'):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='user:CustomerLogin'):
    """
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.active and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
        return result

    return timed


logger = logging.getLogger(__name__)


def user_can_write_a_review(func):
    """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.points < 10:
            logger.warning('The {} user has tried to write a review, but does not have enough points to do so'.format(
                request.user.pk))
            return HttpResponseForbidden()

        return func(request, *args, **kwargs)

    return wrapper


def required(wrapping_functions, patterns_rslt):
    '''
    Used to require 1..n decorators in any view returned by a url tree

    Usage:
      urlpatterns = required(func,patterns(...))
      urlpatterns = required((func,func,func),patterns(...))

    Note:
      Use functools.partial to pass keyword params to the required
      decorators. If you need to pass args you will have to write a
      wrapper function.

    Example:
      from functools import partial

      urlpatterns = required(
          partial(login_required,login_url='/accounts/login/'),
          patterns(...)
      )
    '''
    if not hasattr(wrapping_functions, '__iter__'):
        wrapping_functions = (wrapping_functions,)

    return [
        _wrap_instance__resolve(wrapping_functions, instance)
        for instance in patterns_rslt
    ]


def _wrap_instance__resolve(wrapping_functions, instance):
    if not hasattr(instance, 'resolve'): return instance
    resolve = getattr(instance, 'resolve')

    def _wrap_func_in_returned_resolver_match(*args, **kwargs):
        rslt = resolve(*args, **kwargs)

        if not hasattr(rslt, 'func'): return rslt
        f = getattr(rslt, 'func')

        for _f in reversed(wrapping_functions):
            # @decorate the function from inner to outter
            f = _f(f)

        setattr(rslt, 'func', f)

        return rslt

    setattr(instance, 'resolve', _wrap_func_in_returned_resolver_match)

    return instance
