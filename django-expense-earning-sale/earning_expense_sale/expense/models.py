from django.db import models
from django.utils.timezone import now
# Create your models here.

class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    purpose = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering : ['-date']
