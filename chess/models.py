from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fen = models.CharField(max_length=255)  # Board state in FEN
    created_at = models.DateTimeField(auto_now_add=True)
