from functools import wraps
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render


def heavy_ratelimit(rate, key="ip"):

    

        def decorator(view_func):

            # Original ratelimit decorator apply karo
            limited_view = ratelimit(
                key=key,
                rate=rate,
                block=False,
            )(view_func)

            @wraps(view_func)
            def wrapped_view(request, *args, **kwargs):

                response = limited_view(request, *args, **kwargs)

                if getattr(request, "limited", False):
                    return render(request, "pages/429.html", status=429)

                return response

            return wrapped_view

        return decorator