from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction

class Source(models.Model):
    SOURCE_TYPES = [
        ('book', 'Книга'),
        ('movie', 'Фильм'),
        ('series', 'Сериал'),
        ('other', 'Другое'),
    ]
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='other')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    

class Quote(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField(unique=True)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.text[:50]}..." — {self.source.name}'

    class Meta:
        ordering = ['-likes', '-views']