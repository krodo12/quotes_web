from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count


class Quote(models.Model):
    text = models.TextField()   # цитата,
    source = models.CharField(max_length=200)  # книга / фильм
    weight = models.PositiveIntegerField(default=1)  # вес выпадения
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def clean(self):
        # ограничение веса 1–10
        if not (1 <= self.weight <= 10):
            raise ValidationError("Вес должен быть от 1 до 10")

        # максимум 3 цитаты на источник
        count = Quote.objects.filter(source=self.source).exclude(pk=self.pk).count()
        if count >= 3:
            raise ValidationError("У источника уже есть 3 цитаты")
        
        # проверяем уникальность текста
        if Quote.objects.exclude(pk=self.pk).filter(text=self.text).exists():
            raise ValidationError("Такая цитата уже существует!")
            
    def __str__(self):
        return f"{self.text[:50]}..."

