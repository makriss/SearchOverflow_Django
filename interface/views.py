import requests
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from interface.utility_functions import input_validation


def render_page(request):
    return render(request, "index.html")


class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context


@input_validation
def call_stack_api(request, filters):
    print(filters)
    response = requests.get('https://api.stackexchange.com/2.2/search/advanced?site=stackoverflow', filters)
    print(response.request.url)
    return JsonResponse(response.json())
