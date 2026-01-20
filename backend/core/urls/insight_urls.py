from django.urls import path
from core.views.insight_views import ThermalComfortInsightView

urlpatterns = [
    path(
        "insights/thermal-comfort/",
        ThermalComfortInsightView.as_view(),
        name="thermal-comfort-insight",
    )
]

