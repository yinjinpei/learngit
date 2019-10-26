from django.db import models

# Create your models here.


class BookInfoManager(models.Manager):
    def get_queryset(self):
        return super(BookInfoManager,self).get_queryset().filter(isDelete=False)


class BookInfo(models.Model):
    btitle=models.CharField(max_length=20)
    bpub_date=models.DateTimeField(db_column='pub_date')
    bread=models.IntegerField(default=0)
    bcommet=models.IntegerField(null=False)
    isDelete=models.BooleanField(default=False)
    class Meta:
        db_table='bookinfo'
    books1=models.Manager()
    books2 = BookInfoManager()

class HeroInfo(models.Model):
    hanme=models.CharField(max_length=10)
    hgender=models.BooleanField(default=True)
    hcontent=models.CharField(max_length=1000)
    isDelete=models.BooleanField(default=False)
    book=models.ForeignKey(BookInfo, on_delete=models.CASCADE)

