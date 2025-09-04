from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.models import User

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


class Vote(models.Model):
    VOTE_CHOICES = [
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="votes")
    vote_type = models.CharField(max_length=7, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'quote')