from django.db import models
import uuid

class Game(models.Model):
    code = models.CharField(max_length=8, unique=True, default='', blank=True)
    player1_choice = models.CharField(max_length=10, null=True, blank=True)
    player2_choice = models.CharField(max_length=10, null=True, blank=True)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='waiting')  # waiting, in_progress, finished
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game {self.code} ({self.status})"
