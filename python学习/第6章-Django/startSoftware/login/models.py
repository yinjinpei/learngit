from django.db import models

# Create your models here.


class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    # name必填，最长不超过128个字符，并且唯一，也就是不能有相同姓名；
    # password必填，最长不超过256个字符（实际可能不需要这么长）；
    # email使用Django内置的邮箱类型，并且唯一；
    # 性别使用了一个choice，只能选择男或者女，默认为男；
    # 使用__str__帮助人性化显示对象信息；
    # 元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
    #注意：这里的用户名指的是网络上注册的用户名，不要等同于现实中的真实姓名，所以采用了唯一机制。如果是现实中可以重复的人名，那肯定是不能设置unique的。
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"