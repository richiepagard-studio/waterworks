import jdatetime

class JalaliLocaleMiddleware:
    """
    Middleware to change Jalali Date format
    to the Farsi, especially for Months (%B).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Set 'Farsi' date format for Jalali Date
        per request.
        """
        jdatetime.set_locale('fa_IR')

        return self.get_response(request)
