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


class GoodsRegisterForm(forms.Form):

    name = forms.CharField(label="商品名", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.FloatField(label="价格",widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(label="数量",widget=forms.TextInput(attrs={'class': 'form-control'}))
    detail = forms.CharField(label="描述",max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label="类别",max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    img = forms.ImageField(label="图片")


class CommentForm(forms.Form):
    detail = forms.CharField(label="内容", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    satisfaction = forms.IntegerField(label="满意度",widget=forms.TextInput(attrs={'class': 'form-control'}))


class ImgForm(forms.Form):
    img = forms.ImageField(label="图片")