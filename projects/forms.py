from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        
        
class QueryBuilderForm(forms.Form):
    file = forms.FileField()
    query = forms.CharField(widget=forms.Textarea)
