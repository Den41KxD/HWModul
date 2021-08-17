from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.session.get('count', False):
            print('Na 4 click = ', request.session['count'])
            request.session['count'] += 1
            if request.session['count'] == 4:
                request.session['count'] = 0

        else:
            request.session['count'] = 1




