from django.db import models

# Create your models here.
class Party(models.Model):
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    reference = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    
    
    def __str__(self):
        return self.name + ' , '  +self.area
    
    class Meta:
        ordering : ['name']
        verbose_name_plural = "Parties"