from django.urls import path

from measurement.views import Sensors, SensorView, Measurements

urlpatterns = [
    path('sensors/', Sensors.as_view()),
    path('sensors/<int:id>/', Sensors.as_view()),
    path('sensors/<pk>/', SensorView.as_view()),
    path('measurements/', Measurements.as_view()),

]
