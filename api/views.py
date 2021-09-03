from django.db.models import Avg, Sum, Count
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    DestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)

# /cars/ Create, list
# /cars/<id> Retrieve, Update, Destory
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

# /cars/ Create, list
# /cars/<id> Retrieve, Update, Destory

from api.serializers import CarSerializer, RatingSerializer
from api.models import Car, Rating
from api.info_car import car_info


class CarViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer

    def get_queryset(self):
        if self.action == "delete":
            return Car.objects.all()
        if self.request.query_params.get("ordering") == "popular":
            return Car.objects.popular()
        return Car.objects.annotate(avg_rating=Avg("ratings"))

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.validated_data["model"]
        make = serializer.validated_data["make"]
        _, created = Car.objects.get_or_create(
            model=model, make=make, user=request.user
        )
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class CarPopularView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarSerializer
    queryset = Car.objects.popular()


class RateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class CarClassView(ListCreateAPIView):
#     permission_classes = [IsAuthenticated]

#     serializer_class = CarSerializer
#     queryset = Car.objects.annotate(avg_rating=Avg("ratings"))

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         model = serializer.validated_data["model"]
#         make = serializer.validated_data["make"]
#         _, created = Car.objects.get_or_create(
#             model=model, make=make, user=request.user
#         )
#         if created:
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data)


# class DeleteClassView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CarSerializer
#     queryset = Car.objects.all()


# cars/?ordering=popular
# https://stackoverflow.com/questions/48299466/django-rest-framework-passing-parameters-with-get-request-classed-based-views


# class CarView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         cars = Car.objects.annotate(avg_rating=Avg("ratings"))
#         serializer = CarSerializer(cars, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = CarSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         model = serializer.validated_data["model"]
#         make = serializer.validated_data["make"]
#         try:
#             obj = Car.objects.get(model=model, make=make, user=request.user)
#             serializer = CarSerializer(obj)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Car.DoesNotExist:
#             if car_info(make, model):
#                 serializer.save(make=make, model=model, user=request.user)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(
#                     {"message": "Wrong Make or Model"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#     def delete(self, request, car_id, *args, **kwargs):
#         car = get_object_or_404(Car, id=car_id, user=request.user)
#         car.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# def post(self, request):
#     serializer = RatingSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     car_id = serializer.validated_data["car_id"]
#     rating = serializer.validated_data["rating"]

#     try:
#         obj = Rating.objects.create(user=request.user, car_id=car_id, rating=rating)
#         serializer = RatingSerializer(obj)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     except IntegrityError:
#         raise NotFound


# class RateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = RatingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         car_id = serializer.validated_data["car_id"]
#         rating = serializer.validated_data["rating"]
#         try:
#             obj = Rating.objects.create(user=request.user, car_id=car_id, rating=rating)
#             serializer = RatingSerializer(obj)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except IntegrityError:
#             raise NotFound


# class CarPopularView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         car = Car.objects.popular()
#         serializer = CarSerializer(car, many=True)
#         return Response(serializer.data)
