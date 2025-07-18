from django.db import models
from django.utils import timezone
import json


class EmailUser(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Kategorie(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artikeln(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    beschreibung = models.TextField()
    picture = models.ImageField(upload_to='artikeln/')  # <--- korrektes Feld für Bilder
    preis = models.CharField(max_length=20)
    saving = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=255)
    datum = models.DateTimeField(default=timezone.now)
    kategorie = models.ForeignKey(Kategorie, on_delete=models.CASCADE, related_name='artikel')

    def __str__(self):
        return json.dumps({
            'asin': self.asin,
            'beschreibung': self.beschreibung,
            'picture': self.picture.url if self.picture else '',
            'preis': self.preis,
            'saving': self.saving,
            'title': self.title,
            'datum': str(self.datum),
            'kategorie': self.kategorie.name
        })
