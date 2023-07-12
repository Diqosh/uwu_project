from django import forms

from main_app.models import NotificationTemplate

class NotificationTemplateForm(forms.ModelForm):
    structure = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = NotificationTemplate
        fields = '__all__'