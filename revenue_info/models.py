from django.db import models

class Song(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=500,default='')
    title = models.CharField(max_length=255)
    views = models.BigIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
