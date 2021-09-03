from django.db.models import Avg
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Car
from api.serializers import CarSerializer


class CarViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john", password="password")
        Car.objects.create(user=self.user, make="Nissan", model="350z")
        Car.objects.create(user=self.user, make="Subaru", model="Impreza")
        Car.objects.create(user=self.user, make="Mitschubishi", model="LancerEvolution")

    def test_car_list_view(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(reverse("car-list"))
        qs = Car.objects.annotate(avg_rating=Avg("ratings"))
        serializer = CarSerializer(qs, many=True)
        self.assertEqual(serializer.data, resp.data)
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_car_list_view_unauthenticated(self):
        resp = self.client.get(reverse("car-list"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)
