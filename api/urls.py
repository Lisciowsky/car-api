from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("cars", views.CarViewSet, basename="car")

# https://www.django-rest-framework.org/api-guide/viewsets/
urlpatterns = [
    # path("cars-overview/", views.api_overview, name="overview"),
    # path("cars/", views.car_list, name="car-list"),
    # path("cars-create/", views.car_create, name="car-create"),
    # path("cars-delete/<int:pk>/", views.car_delete, name="car-delete"),
    # path("cars-rate/", views.car_rate, name="car-rate"),
    # path("cars-popular/", views.car_popular, name="car-popular"),
    # path("cars/", views.CarView.as_view(), name="cars"),
    # path("cars/<int:car_id>/", views.CarView.as_view(), name="cars"),
    path("rate/", views.RateView.as_view(), name="rate"),
    path("popular/", views.CarPopularView.as_view(), name="cars-popular"),
    # class ones
    # path("cars-class/", views.CarClassView.as_view(), name="cars-class"),
    # path("cars-class/<int:pk>/", views.DeleteClassView.as_view(), name="cars-class"),
]
# http "<token>" example.org -h
# http DELETE  localhost:8000/v1/cars/3/ --auth-type=jwt --auth="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwNTI4MDI2LCJqdGkiOiJkODM1Yzk2Zjg1OWI0MGViOGNmZDAzYzYwNWY2YzNhZSIsInVzZXJfaWQiOjF9.Vx5-BtHLtztIB90KK6oU6PqtwZGPxtrWNygt-xYAYgM"

urlpatterns += router.urls
