from django import forms


class UserForm(forms.Form):
    account = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):

    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    account = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(label="联系电话", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="地址", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class goodsRegisterForm(forms.Form):

    price = forms.FloatField(label="价格")
    quantity = forms.IntegerField(label="数量")
    detail = forms.CharField(label="描述",max_length=256)
    category = forms.CharField(label="类别",max_length=256)