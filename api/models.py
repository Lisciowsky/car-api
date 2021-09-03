from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class CarManager(models.Manager):
    def popular(self):
        return self.annotate(
            total_rates=models.Count("ratings__id"),
            avg_rating=models.Avg("ratings__rating"),
        ).order_by("-total_rates")


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    make = models.CharField(max_length=300)
    model = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    objects = CarManager()

    def __str__(self):
        return f"{str(self.user)}"


class Rating(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    rating = models.DecimalField(
        blank=True,
        null=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        decimal_places=1,
        max_digits=2,
    )
