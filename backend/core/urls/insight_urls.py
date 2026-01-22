
""" URL patterns for all API endpoints.

    URL mapping -> View function
"""



from django.urls import path
from core.views.insight_views import ThermalComfortInsightView
from api.views.temperature_insight import temperature_insight_view

urlpatterns = [
    path(
        "v1/insights/temperature/",
        temperature_insight_view,       # function-based view located in api/views/temperature_insight.py
        name="temperature-insight",
    ),
    path(
        "insights/thermal-comfort/",
        ThermalComfortInsightView.as_view(),  # class-based view located in core/views/insight_views.py
        name="thermal-comfort-insight",
    )
]

