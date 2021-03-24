from django.db import models
from django.utils.timezone import now

# Create your models here.
class Sale(models.Model):
    name = models.CharField(max_length=255)
    bill_no = models.CharField(max_length=50)
    amount = models.FloatField()
    date = models.DateField(default=now)
    area = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name + ' - ' + self.area
    
    class Meta:
        ordering: ['-date']