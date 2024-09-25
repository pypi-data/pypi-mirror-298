from django.db import models
from django.contrib.contenttypes.models import ContentType
# Create your models here.
    
class Chart(models.Model):
    model_name = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    model_field = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.model_name.name