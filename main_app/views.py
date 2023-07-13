# Create your views here.
from django.shortcuts import render, redirect
from main_app.models import NotificationTemplate
from main_app.froms import NotificationTemplateForm

def create_view(request):
    is_success =  False
    if request.method == 'POST':
        form = NotificationTemplateForm(request.POST)
        if form.is_valid():
            kind = form.cleaned_data['kind']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            
            template = NotificationTemplate.objects.create(kind=kind, title=title, body=body)
            
            template.send(user=request.user)
            is_success = True
    else:
        form = NotificationTemplateForm()
    return render(request, 'main_app/create.html', {'form': form, 'is_success': is_success})
