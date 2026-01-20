from django.urls import path
from api.views.temperature_insight import temperature_insight_view

urlpatterns = [
    path(
        "v1/insights/temperature/",
        temperature_insight_view,
        name="temperature-insight",
    ),
]

