from django.urls import path
from core.views.insight_views import ThermalComfortInsightView
from core.views.temperature_insight import temperature_insight_view

urlpatterns = [
    path(
        "insights/thermal-comfort/",
        ThermalComfortInsightView.as_view(),
        name="thermal-comfort-insight",
    ),
    path(
        "v1/insights/temperature/",
        temperature_insight_view,
        name="temperature-insight",
    ),
]

