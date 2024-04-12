from django.db import models

class Solicitud(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.IntegerField(max_length=50)
    mail = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.name)

