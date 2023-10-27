from django.shortcuts import render , redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os 
from django.contrib.auth.models import *
from .models import *
import csv
from django.conf import settings
import pandas as pd
# Create your views here.

# def welcome(request):
#     return HttpResponse("Hello, world!")
@login_required
def welcome(request):
    return render(request, 'welcome.html')
@login_required
def home(request):
    return render(request, 'reg.html')

# def upload(request):
#     if request.method == 'GET':
#         return render(request, 'upload.html')
#     if request.method == 'POST':
#         uploaded_file = request.FILES['file']
#         file_path = os.path.join('uploads', uploaded_file.name)
#         return JsonResponse({'message': 'File uploaded successfully.'})
#     return render(request, 'upload.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,password,"!!!!!!!!!!!!!!!!!!!")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"Sucessfully Logged IN")
                return redirect('welcome')  # Redirect to the dashboard or another page
            else:
                messages.error(request,"Invalid Credentials! Pleases try again")
                return redirect('welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def users(requet):
    pass

# def query(request):
#     print(request.method,'11111111111111111',request.headers,'22222222222222',type(request.body),request.body)

#     return HttpResponse("hiiii")


# def data_query(request):
#     if request.method=="GET":
#         # Get the post parameters
#         username=request.POST['username']
#         email=request.POST['email']
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']

#         # check for errorneous input
        
#         # Create the user
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name= fname
#         myuser.last_name= lname
#         myuser.save()
#         messages.success(request, " Your iCoder has been successfully created")
#         return redirect('home')

#     else:
#         return HttpResponse("404 - Not found")

@login_required
def query(request):
    # Define your dropdown options (retrieve these from the backend as needed)
    industry = Data.objects.values_list('industry', flat=True).distinct()
    year = Data.objects.values_list('year_founded', flat=True).distinct()
    city = Data.objects.values_list('locality', flat=True).distinct()
    # u_city = {i.split()[0] for i in city}
    u_city = {i.replace(',', '').split()[0] for i in city}
    # print(u_city,len(u_city))
    # state = Data.objects.values_list('locality', flat=True).distinct()
    # u_state = {i.split()[1] for i in city}
    # u_state = {i.split()[1] if len(i.split()) > 1 else 'N/A' for i in city}
    u_state = {i.replace(',', '').split()[1] if len(i.split()) > 1 else 'N/A' for i in city}
    # print(state)
    country = Data.objects.values_list('country', flat=True).distinct()
    empfr = Data.objects.values_list('current_employee_estimate', flat=True).distinct()
    empto = Data.objects.values_list('total_employee_estimate', flat=True).distinct()
    # print(industry,len(industry))


    if request.method == 'POST':
        # print(request.META,"AAAAAAAAAAAAAa")
        # Handle form submission
        textfield_value = request.POST.get('textfield')
        dropdown1_value = request.POST.get('dropdown1')
        dropdown2_value = request.POST.get('dropdown2')
        dropdown3_value = request.POST.get('dropdown3')
        dropdown4_value = request.POST.get('dropdown4')
        dropdown5_value = request.POST.get('dropdown5')
        dropdown6_value = request.POST.get('dropdown6')
        dropdown7_value = request.POST.get('dropdown7')
        print(textfield_value,dropdown1_value,dropdown2_value,dropdown3_value,dropdown4_value,dropdown5_value,dropdown6_value,dropdown7_value)
        query_params = {}
        if dropdown1_value != 'default':
            query_params['industry']=dropdown1_value
        if dropdown2_value != 'default':
            query_params['year_founded']=dropdown2_value
        if dropdown3_value != 'default':
            query_params['locality']=dropdown3_value
        if dropdown4_value != 'default':
            query_params['locality']=dropdown4_value
        if dropdown5_value != 'default':
            query_params['country']=dropdown5_value
        if dropdown6_value != 'default':
            query_params['current_employee_estimate']=dropdown6_value
        if dropdown7_value != 'default':
            query_params['total_employee_estimate']=dropdown7_value

        print(query_params,"qqqqqqqqqqqqq")
        queryset = Data.objects.filter(**query_params)
        record_count = queryset.count()
        # print(record_count)
        return JsonResponse({'count': record_count})

        # Process the data, e.g., save it to the database

        # Redirect to a success page or return a response
        # return HttpResponse("Form submitted successfully")
        # return redirect('query')

    context = {
        'dropdown1_options': industry,
        'dropdown2_options': year,
        'dropdown3_options': u_city,
        'dropdown4_options': u_state,
        'dropdown5_options': country,
        'dropdown6_options': empfr,
        'dropdown7_options': empto,
    }

    return render(request, 'query.html', context)
@login_required
def user_management(request):
    # Retrieve a list of all users
    # users = User.objects.all()
    users = Users.objects.all()
    return render(request, 'user_management.html', {'users': users})

# def add_user(request):
#     # Handle user creation logic here
#     if request.method == 'POST':
#         pass
#         # Retrieve and process form data
#         # Create a new user using User.objects.create_user() or a custom form
#         # Redirect to the user management page

#     return render(request, 'add_user.html')
@login_required
def add_user(request):
    if request.method == 'POST':
        # Retrieve user data from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a new user
        user = Users(username=username, password=password, email=email)
        user.save()

        return redirect('um')  # Redirect to the user management page or a success page

    return render(request, 'add_user.html')
@login_required
def delete_user(request, user_id):
    user = Users(id=user_id)
    user.delete()
    return redirect('um')



def process_csv_file(filepath):
    with open(filepath, 'r') as csv_file:
        chunk_size = 1000
        csv_reader = pd.read_csv(csv_file, chunksize=chunk_size)
        # reader = csv.reader(csv_file)
        # for row in reader:
        #     # Process each row, e.g., save it to a database table
        #     print(row)
        for chunk in csv_reader:
            chunk['year founded'].fillna(0, inplace=True)
            for index, row in chunk.iterrows():
                # print(row)
                Data.objects.create(
                    name=row['name'],
                    domain=row['domain'],
                    year_founded=row['year founded'],
                    industry=row['industry'],
                    size_range=row['size range'],
                    locality=row['locality'],
                    country=row['country'],
                    linkedin_url=row['linkedin url'],
                    current_employee_estimate=row['current employee estimate'],
                    total_employee_estimate=row['total employee estimate']
                )
@login_required
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csvfile'):
        uploaded_file = request.FILES['csvfile']
        fs = FileSystemStorage(location=settings.FILE_UPLOAD_TEMP_DIR)
        filename = fs.save(uploaded_file.name, uploaded_file)
        filepath = os.path.join(settings.FILE_UPLOAD_TEMP_DIR, filename)
        # Process the file
        process_csv_file(filepath)
        # return HttpResponse("File uploaded and processed successfully")
        return redirect('upload_csv')
    return render(request, 'upload.html')