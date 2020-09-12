import json

from django.http import JsonResponse


def input_validation(func):
    def inner(request):
        filters = request.GET.get('filters') or request.POST.get('filters')
        filters = json.loads(request.body).get('filters') if not filters and request.body else {}
        # print(filters)
        # removing key having empty value
        filters = {k:v for k,v in filters.items() if v}
        return func(request, filters)

    return inner
