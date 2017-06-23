from django import forms

class RouteForm(forms.Form):
    route=forms.CharField(max_length=10)
