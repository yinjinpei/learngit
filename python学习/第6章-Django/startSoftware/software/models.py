from django.db import models

# Create your models here.
class AppInfo(models.Model):
    appName = models.CharField(max_length=20)
    appDir = models.CharField(max_length=100)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table='appinfo'

    def showname(self):
        return self.appName
    def showdir(self):
        return self.appDir
    def showID(self):
        return self.pk
