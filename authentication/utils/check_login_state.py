from django.shortcuts import redirect


def check_login(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            return redirect('authentication:login')
            
    return inner
