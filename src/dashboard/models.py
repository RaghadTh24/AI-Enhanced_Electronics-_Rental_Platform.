from django.db import models
from accounts.models import User

# Create your models here.

# التصنيفات المتاحة
CATEGORY_CHOICES = [
    ('computers', 'Computers'),
    ('televisions', 'Televisions'),
    ('projectors', 'Projectors'),
    ('printers', 'Printers'),
    ('cameras', 'Cameras'),
    ('speakers', 'Speakers'),
]

class Device(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # البائع
    name = models.CharField(max_length=100)
    specs = models.TextField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='devices/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # التصنيف
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.stars for r in ratings) / ratings.count(), 1)
        return None