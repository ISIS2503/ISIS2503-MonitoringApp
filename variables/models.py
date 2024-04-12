from django.db import models

class Variable(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='Colombia')
    city = models.CharField(max_length=50, default='Bogota')
    phone = models.IntegerField()
    mail = models.CharField(max_length=50, default='@bancodelosalpes.com.co')

    def __str__(self):
        return '{}'.format(self.name)

