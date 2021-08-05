from django.db import models


CATEGORIES = (
    ('inventory', 'Прокат инвентаря'),
    ('auto', 'Прокат авто'),
    ('bicycle', 'Прокат велосипедов'),
    ('scooter', 'Прокат самокатов'),
    ('moped', 'Прокат мопедов'),
    ('boat', 'Прокат яхт'),
    ('aquabike', 'Прокат аквабайков')
)


class ModelWithCategory(models.Model):
    base_category = models.CharField(max_length=32, choices=CATEGORIES, default='inventory')
