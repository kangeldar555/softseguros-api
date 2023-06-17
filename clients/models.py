from django.db import models

# Create your models here.
class Client(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    birth_date = models.DateField()
    creation_date = models.DateField()
    deleted = models.BooleanField(default=False)

    # Me muestra en el administrador el nombre completo de cada cliente
    def __str__(self):
        return self.full_name