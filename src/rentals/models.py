from django.db import models
from django.conf import settings
from dashboard.models import Device
# Create your models here.



class Rental(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    )

    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    location_lat = models.FloatField(blank=True,null=True)
    location_lng = models.FloatField(blank=True,null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    buyer_returned = models.BooleanField(default=False)
    seller_confirmed = models.BooleanField(null=True, blank=True)  # None = ما رد


    def __str__(self):
        return f"{self.device.name} - {self.user.username} ({self.start_date} to {self.end_date})"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField()  # من 1 إلى 5
    comment = models.TextField(blank=True)
    sentiment = models.CharField(max_length=10, default='neutral')  # تحليل المشاعر
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'device')

    def __str__(self):
        return f"{self.device.name} - {self.stars}⭐ by {self.user.username}"

    

class DeviceNotification(models.Model):
    device = models.ForeignKey('dashboard.Device', on_delete=models.CASCADE)
    email = models.EmailField()
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.device.name}"


