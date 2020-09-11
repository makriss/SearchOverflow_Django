from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


def render_page(request):
    return render(request, "index.html")


class PartialGroupView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartialGroupView, self).get_context_data(**kwargs)
        # update the context
        return context
