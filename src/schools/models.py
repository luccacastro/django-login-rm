from django.db import models

class School(models.Model):
    urn = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=100, blank=True)
    open_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True)
    city = models.CharField(max_length=100, null=True)
    postcode = models.CharField(max_length=20, null=True)
    website = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.name} ({self.city})" 
