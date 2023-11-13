from django import forms
from .models import IncidentReport

class IncidentReportForm(forms.ModelForm):
    
    class Meta:
        model = IncidentReport
        fields = ['obstruction',
                 'imageUrls',
                 'description',
                 'latitude',
                 'longitude',
                ]
        labels = {
            'imageUrls': 'Image',
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)
        