import urllib

import requests
from django.core.cache import cache, InvalidCacheBackendError
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from interface.utility_functions import input_validation, session_validation


def render_page(request):
    return render(request, "index.html")


class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context


@session_validation
@input_validation
def call_stack_api(filters):
    params = urllib.parse.urlencode(filters)

    if cache.get(params):
        return JsonResponse(cache.get(params))
    else:
        response = requests.get('https://api.stackexchange.com/2.2/search/advanced?site=stackoverflow', params=filters)
        cache.set(params, response.json())

    return JsonResponse(response.json())
