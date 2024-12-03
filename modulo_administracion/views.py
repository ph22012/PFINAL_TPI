from django.shortcuts import render

# Create your views here.
def GeneralView(request):
    return render(request, 'administracion/inicio.html')


