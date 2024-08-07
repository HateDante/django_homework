from django.db import models
# from django.forms.fields import ImageField


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)


class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    # Попытка добавить изображение
    # image = ImageField(allow_empty_file=True)
