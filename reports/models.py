from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IncidentReport(models.Model):
    incident_id = models.AutoField(primary_key=True)
    obstruction = models.CharField(max_length=20)
    imageUrls = models.ImageField(upload_to='incident_reports/')
    description = models.TextField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20)
    createdAt = models.DateTimeField(auto_now=True)
    createdBy = models.CharField(max_length=20)


    class Meta:
            db_table = "IncidentReport"


# class RoadSign(models.Model):
#     roadsign_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     image = models.ImageField(upload_to='roadsign_images/')

#     class Meta:
#             db_table = "RoadSigns"


# class Contact(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    
#     class Meta:
#             db_table = "Contact"