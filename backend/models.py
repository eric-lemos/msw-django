from django.contrib.auth.models import Group
from django.db import models

class Config(models.Model):
    name = models.CharField(primary_key=True,unique=True,max_length=40)
    value = models.CharField(max_length=40)
    description = models.TextField()

    class Meta:
        db_table = 'config'

class Models(models.Model):
    manufacturer = models.CharField(max_length=20)
    model = models.CharField(max_length=16)
    description = models.TextField(blank=True)
    max_rf = models.IntegerField(default=-60)
    min_rf = models.IntegerField(default=-100)
    max_aud = models.IntegerField(default=0)
    min_aud = models.IntegerField(default=-40)
    max_gain = models.IntegerField(default=10)
    min_gain = models.IntegerField(default=-18)

    class Meta:
        verbose_name_plural = "models"
        db_table = 'models'
        
    def __str__(self):
        return self.model
    
class Devices(models.Model):
    alias = models.CharField(max_length=20)
    host = models.CharField(max_length=16)
    port = models.IntegerField()
    model = models.ForeignKey(Models, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "devices"
        db_table = 'devices'  

    def __str__(self):
        return self.alias
    
class Mics(models.Model):
    name = models.CharField(max_length=20)
    alias = models.CharField(max_length=20, blank=True)
    detail = models.CharField(max_length=10)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "mics"
        db_table = 'mics'
    
    def __str__(self):
        return self.name
    
class Log(models.Model):
    type = models.CharField(max_length=20)
    system = models.CharField(max_length=40)
    subsystem = models.CharField(max_length=40)
    user = models.CharField(max_length=20)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'log'
           
class GroupExtend(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    mics = models.ManyToManyField(Mics, blank=True)