from django.db import models
from django.contrib.auth.models import User

class Arac(models.Model):
    plaka = models.CharField(max_length=20)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    durum = models.CharField(max_length=20)

    def __str__(self):
        return self.plaka


class Sofor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ad_soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    ehliyet_no = models.CharField(max_length=30)

    def __str__(self):
        return self.ad_soyad


class Sefer(models.Model):
    arac = models.ForeignKey(Arac, on_delete=models.CASCADE)
    sofor = models.ForeignKey(Sofor, on_delete=models.CASCADE)

    cikis_noktasi = models.CharField(max_length=100)
    varis_noktasi = models.CharField(max_length=100)

    tahmini_sure = models.IntegerField()
    durum = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.cikis_noktasi} - {self.varis_noktasi}"
