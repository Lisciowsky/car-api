from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from api.models import Car, Rating

from api.info_car import car_info


class CarSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(required=False)
    total_rates = serializers.IntegerField(required=False)

    class Meta:
        model = Car
        fields = ["id", "make", "model", "avg_rating", "total_rates", "created_at"]
        read_only_fields = ["avg_rating", "total_rates"]

    def validate(self, data):
        if not car_info(data["make"], data["model"]):
            raise serializers.ValidationError("Wrong Make or Model")
        return data


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rating", "car"]
