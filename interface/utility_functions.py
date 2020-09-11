import json

from django.http import JsonResponse


def input_validation(func):
    def inner(request):
        filters = request.GET.get('filters') or request.POST.get('filters') or json.loads(request.body).get('filters')
        if not filters:  # return in case no data is sent
            filters = {}
        return func(request, filters)

    return inner
