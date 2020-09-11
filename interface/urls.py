from django.conf.urls import url
from django.urls import path, include

from interface import views

app_name = "interface"

partial_patterns = [
    url(r'^result-template.html$', views.PartialGroupView.as_view(template_name='result-template.html'), name='result_template'),
    # ... more partials ...,
]

urlpatterns = [
    path('', views.render_page),
    url(r'^templates/', include(partial_patterns)),
]