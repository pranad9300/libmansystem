from django import forms
from .models import Book,User,Profile
class BookForm(forms.ModelForm):
    class Meta:
       model = Book
       fields = ('book_name','book_author','description','avalaible','book_image','category')
       widgets = { 
                 "book_name" : forms.TextInput(attrs={'class':'inputs'}),
                 "book_author" : forms.TextInput(attrs={'class':'inputs'}),
                 "description" : forms.TextInput(attrs={'class':'inputs'}),
                 "avalaible" : forms.NumberInput(attrs={'class':'inputs'}),
                 "category" : forms.Textarea(attrs={'class':'inputs'})
                }

class UpdateUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'inputs'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'inputs'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs'}))
    password2 =  forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputs'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )