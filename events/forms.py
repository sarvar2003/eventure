from django import forms

from . import models

class EventForm(forms.ModelForm):
    themes = forms.ModelMultipleChoiceField(queryset=models.Event.objects, widget=forms.CheckboxSelectMultiple(), required=False)