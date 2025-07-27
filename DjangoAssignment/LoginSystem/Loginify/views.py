from django.shortcuts import render
from .models import Register
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#  GET ALL USERS
def get_all_users(request):
    if request.method == 'GET':
        users = Register.objects.all()
        user_list = [{'username': u.username, 'email': u.email, 'password': u.password} for u in users]
        return JsonResponse(user_list, safe=False)

# GET SINGLE USER BY EMAIL
def get_user_by_email(request, email):
    try:
        user = Register.objects.get(email=email)
        return JsonResponse({'username': user.username, 'email': user.email, 'password': user.password})
    except Register.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

#  UPDATE USER DETAILS
@csrf_exempt
def update_user(request, email):
    if request.method == 'PUT':
        try:
            user = Register.objects.get(email=email)
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

            user.username = data.get('username', user.username)
            user.password = data.get('password', user.password)

            # Update email if changed and not already in use
            new_email = data.get('email')
            if new_email and new_email != user.email:
                if Register.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                    return JsonResponse({'error': 'Email already in use'}, status=400)
                user.email = new_email

            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except Register.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


#  DELETE USER
@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE' or request.method == 'GET':
        try:
            user = Register.objects.get(email=email)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except Register.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


# Home Page
def home(request):
     return render(request, 'home.html')

#Signup page
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        if Register.objects.filter(email=email).exists():
         messages.error(request,"Email already exists")
         return render(request,"Signup.html")
        
        user = Register(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Signup successful! Please log in.')
        return redirect('login')

    return render(request, 'Signup.html')

# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Register.objects.get(email=email, password=password)
            return render(request, 'Success.html', {'user': user})
        except Register.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return render(request, 'Login.html')

    return render(request, 'Login.html')
   



