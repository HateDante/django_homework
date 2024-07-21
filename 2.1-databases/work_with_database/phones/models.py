from autoslug import AutoSlugField
from django.db import models


# В файле models.py нашего приложения создаём модель Phone с полями id, name, price, image, release_date, lte_exists и
# slug. Поле id — должно быть основным ключом модели.

class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(max_length=10)
    image = models.CharField(max_length=150)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = AutoSlugField(populate_from='name', unique_with='name')


