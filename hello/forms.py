from django import forms
 
class UserForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
