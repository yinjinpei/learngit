from django.db import models
from django import forms
from captcha.fields import CaptchaField
# Create your models here.


gender = (
    ('male', "男"),
    ('female', "女"),
)

class User(models.Model):
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
    class Meta:
        ordering = ["c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
    def __str__(self):
        return self.name
    userinfo = models.Manager()
    def showname(self):
        return self.name
    def showpasswd(self):
        return self.password
    def showemail(self):
        return self.email
    def showsex(self):
        return self.sex
    def showctime(self):
        return self.c_time


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password1和password2，用于注册时输入两遍密码，并进行比较，防止误输密码；
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


class ModifyPasswordForm(forms.Form):
    oldPassword = forms.CharField(label="旧密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newPassword1 = forms.CharField(label="新密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    newPassword2 = forms.CharField(label="确认新密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
