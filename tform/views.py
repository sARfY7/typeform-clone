from django.shortcuts import render
from .models import Form

# Create your views here.

def form_list(request):
    tforms = Form.objects.all()
    return render(request, 'tform/form_list.html', {'tforms': tforms})
