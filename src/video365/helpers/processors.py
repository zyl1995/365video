from django.conf import settings

def path_context_processor(request):
    path = {
        'PATH': settings.APP_PATH,
    }

    return path