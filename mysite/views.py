from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def redirect_to_z(req):
    return redirect('z/');
