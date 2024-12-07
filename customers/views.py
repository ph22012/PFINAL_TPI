from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect
from .models import CustomUser, Customer, Employee
from django.contrib.auth.decorators import login_required
# Create your views here.

def registro(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            return render(request, 'usuarios/signup.html')
        else:
            if CustomUser.objects.filter(username=username).exists():
                #return render(request, 'usuarios/signup.html', {'error': 'El usuario ya existe'})
                print('El usuario ya existe')
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password, is_customer=True)
                Customer.objects.create(user=user, firstName=firstName, lastName=lastName)
                return redirect('profile')
    
    return render(request, 'usuarios/signup.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect( 'profile' )
        else:
            print('Username or password is incorrect')
            return render(request, 'usuarios/login.html')
    else:
        return render(request, 'usuarios/login.html')
    
@login_required
def profile(request):
    user = request.user
    return render(request, 'usuarios/profile.html', {'user': user})