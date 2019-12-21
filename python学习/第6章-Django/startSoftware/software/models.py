from django.db import models

# Create your models here.
class AppInfo(models.Model):
    userName = models.CharField(max_length=128, default=None)
    appName = models.CharField(max_length=20)
    appDir = models.CharField(max_length=100)
    remark = models.CharField(max_length=100,default=None)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table='appinfo'

    apps = models.Manager()
    def showname(self):
        return self.appName
    def showdir(self):
        return self.appDir
    def showID(self):
        return self.pk
    def showusername(self):
        return self.userName
