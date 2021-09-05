from django.db.models import Avg
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Car, Rating
from api.serializers import CarSerializer


class CarModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john", password="password")
        self.c1 = Car.objects.create(user=self.user, make="Nissan", model="350z")
        self.c2 = Car.objects.create(user=self.user, make="Subaru", model="Impreza")
        self.c3 = Car.objects.create(
            user=self.user, make="Mitschubishi", model="LancerEvolution"
        )
        Rating.objects.create(user=self.user, car=self.c1, rating=1)
        Rating.objects.create(user=self.user, car=self.c1, rating=2)
        Rating.objects.create(user=self.user, car=self.c1, rating=3)
        Rating.objects.create(user=self.user, car=self.c2, rating=2)
        Rating.objects.create(user=self.user, car=self.c2, rating=4)

    def test_car_popular(self):
        qs = Car.objects.popular()
        self.assertEqual(qs.first(), self.c1)
        self.assertEqual(qs.last(), self.c3)


class CarViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john", password="password")
        self.c1 = Car.objects.create(user=self.user, make="Nissan", model="350z")
        Car.objects.create(user=self.user, make="Subaru", model="Impreza")
        Car.objects.create(user=self.user, make="Mitschubishi", model="LancerEvolution")

    def test_car_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("car-list"))
        qs = Car.objects.annotate(avg_rating=Avg("ratings__rating"))
        serializer = CarSerializer(qs, many=True)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_car_list_unauthenticated(self):
        response = self.client.get(reverse("car-list"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_car_create(self):
        self.client.force_authenticate(user=self.user)
        payload = {"make": "nissan", "model": "GT-R"}
        response = self.client.post(reverse("car-list"), payload)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue(Car.objects.filter(id=response.data["id"]).exists())

    def test_car_create_invalid(self):
        self.client.force_authenticate(user=self.user)
        payload = {"make": "asdasdasd", "model": "asdasdasd"}
        prev_count = Car.objects.count()
        response = self.client.post(reverse("car-list"), payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(prev_count, Car.objects.count())

    def test_car_retrive(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("car-detail", kwargs={"pk": self.c1.id}))
        obj = Car.objects.annotate(avg_rating=Avg("ratings__rating")).get(id=self.c1.id)
        serializer = CarSerializer(obj)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_car_retrive_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("car-detail", kwargs={"pk": 100}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_car_update(self):
        self.client.force_authenticate(user=self.user)
        payload = {"make": "BMW", "model": "X4"}
        response = self.client.put(
            reverse("car-detail", kwargs={"pk": self.c1.id}), payload
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.c1.refresh_from_db()
        self.assertEqual(response.data["make"], self.c1.make)
        self.assertEqual(response.data["model"], self.c1.model)

    def test_car_update_invalid(self):
        self.client.force_authenticate(user=self.user)
        payload = {"make": "asdasdasd", "model": "asdasdasd"}
        response = self.client.put(
            reverse("car-detail", kwargs={"pk": self.c1.id}), payload
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_car_update_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse("car-detail", kwargs={"pk": 100}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_car_delete_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("car-detail", kwargs={"pk": 100}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_car_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("car-detail", kwargs={"pk": self.c1.pk}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Car.objects.filter(id=self.c1.id).exists())


class RateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john", password="password")
        self.c1 = Car.objects.create(user=self.user, make="Nissan", model="350z")
        Car.objects.create(user=self.user, make="Subaru", model="Impreza")
        Car.objects.create(user=self.user, make="Mitschubishi", model="LancerEvolution")

    def test_rate_view(self):
        payload = {"rating": 4, "car": self.c1.id}
        response = self.client.post(reverse("rate"), payload)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("rate"), payload)
        response = self.client.post(reverse("rate"), {"rating": 3, "car": self.c1.id})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        avg_rating = self.c1.ratings.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        self.assertEqual(float(avg_rating), 3.5)
        self.assertEqual(self.c1.ratings.count(), 2)

    def test_rate_view_invalid_rating(self):
        self.client.force_authenticate(user=self.user)
        payload = {"rating": 0, "car": self.c1.id}
        response = self.client.post(reverse("rate"), payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        payload = {"rating": 6, "car": self.c1.id}
        response = self.client.post(reverse("rate"), payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_rate_view_invalid_car(self):
        self.client.force_authenticate(user=self.user)
        payload = {"rating": 1, "car": 100}
        response = self.client.post(reverse("rate"), payload)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class PopularViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john", password="password")
        self.c1 = Car.objects.create(user=self.user, make="Nissan", model="350z")
        self.c2 = Car.objects.create(user=self.user, make="Subaru", model="Impreza")
        self.c3 = Car.objects.create(
            user=self.user, make="Mitschubishi", model="LancerEvolution"
        )
        Rating.objects.create(user=self.user, car=self.c1, rating=1)
        Rating.objects.create(user=self.user, car=self.c1, rating=2)
        Rating.objects.create(user=self.user, car=self.c1, rating=3)
        Rating.objects.create(user=self.user, car=self.c2, rating=2)
        Rating.objects.create(user=self.user, car=self.c2, rating=4)

    def test_popular_view(self):
        response = self.client.get(reverse("cars-popular"))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("cars-popular"))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        qs = Car.objects.popular()
        serializer = CarSerializer(qs, many=True)
        self.assertEqual(serializer.data, response.data)
