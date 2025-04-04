from django.http import HttpResponse , HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from django.shortcuts import render ,get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Case, When, BooleanField , Value
from django.http import JsonResponse
from django.shortcuts import redirect
from csdata.models import Cdetail
from csdata.models import Ticket
from csdata.models import Employee
from csdata.models import Bookings
from django.db.models import Q

def logout_view(request):
    response = redirect('/signin')  

    response.delete_cookie('user_name')
    response.delete_cookie('user_email')
    response.delete_cookie('user_image')

    return response 

def home(request):
    return render(request, 'templates/home/index.html')


def about(request):
    return render(request, 'templates/home/about.html')

def signup(request):
    if request.method == 'POST':
        profile_image=request.POST['profile_image']
        name=request.POST['name']
        phone=request.POST['phone']
        mail=request.POST['mail']
        passw=request.POST['passw']
        rpass=request.POST['rpass']
        gender=request.POST['gender']
        address=request.POST['address']
        
        
        d1=Cdetail(profile_image=profile_image,name=name,phone=phone,mail=mail,passw=passw,gender=gender,address=address)
        if passw == rpass:
            d1.save()
        else:
            return HttpResponseRedirect('/signup')
        
        return HttpResponseRedirect('/signin')
    return render(request, 'templates/home/signup.html')


def signin(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        password = request.POST.get('pass')

        if not mail or not password:
            return HttpResponseRedirect('/signin')

        # 1. First check if it's admin
        if mail == 'admin@gmail.com':
            try:
                admin_user = Cdetail.objects.get(mail=mail, passw=password)
                response = redirect('/aadmin')
                response.set_cookie('user_name', admin_user.name, max_age=604800)
                response.set_cookie('user_email', admin_user.mail, max_age=604800)
                response.set_cookie('user_type', 'admin', max_age=604800)  # Add user type
                return response
            except Cdetail.DoesNotExist:
                return HttpResponseRedirect('/signin')

        # 2. Check if it's an employee
        try:
            employee = Employee.objects.get(email=mail,passw=password)
            # In your Employee model, there's no password field, so we're only checking email
            # If you want password auth for employees, add passw field to Employee model
            response = redirect('/employeeservicebooked')
            response.set_cookie('user_name', employee.name, max_age=604800)
            response.set_cookie('user_email', employee.email, max_age=604800)
            response.set_cookie('user_phone', employee.phone, max_age=604800)
            response.set_cookie('user_type', 'employee', max_age=604800)  # Add user type
            profile_image_url = employee.profile_image if employee.profile_image else 'https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg'
            response.set_cookie('user_image', profile_image_url, max_age=604800)
            return response
        except Employee.DoesNotExist:
            pass  # Not an employee, continue to check regular user

        # 3. Check if it's a regular user
        try:
            user = Cdetail.objects.get(mail=mail, passw=password)
            response = redirect('/bookservice')
            response.set_cookie('user_name', user.name, max_age=604800)
            response.set_cookie('user_email', user.mail, max_age=604800)
            response.set_cookie('user_phone', user.phone, max_age=604800)
            response.set_cookie('user_type', 'user', max_age=604800)  # Add user type
            profile_image_url = user.profile_image if user.profile_image else 'https://static.vecteezy.com/system/resources/previews/005/544/718/non_2x/profile-icon-design-free-vector.jpg'
            response.set_cookie('user_image', profile_image_url, max_age=604800)
            return response
        except Cdetail.DoesNotExist:
            # Invalid credentials
            return HttpResponseRedirect('/signin')

    return render(request, 'templates/home/signin.html')                                   


def contact(request):
    return render(request, 'templates/home/contact.html')



def servicebooked(request):
    bookings = Bookings.objects.all()
    users = Cdetail.objects.all()
    services = Employee.objects.all()

    # Create dictionaries for quick lookup by unique ID
    user_dict = {user.unique: user for user in users}
    service_dict = {service.unique: service for service in services}

    combined = []
    for booking in bookings:
        user = user_dict.get(booking.uniqueuser)
        service = service_dict.get(booking.uniqueservice)
        if user and service:
            combined.append({
                'booking_unique': booking.unique,    
                'user': user,                        
                'service': service,                    
                'advance': booking.advance           
            })

    context = {
        'combined_list': combined
    }
    return render(request, 'templates/admin/servicebooked.html', context)




def aadmin(request):
  
    customer_count = Cdetail.objects.count()      
    employee_count = Employee.objects.count()     
    ticket_count = Ticket.objects.count()         

    context = {
        'data1': customer_count,
        'data2': employee_count,
        'data3': ticket_count
    }
    return render(request, 'templates/admin/aadmin.html', context)

def addemp(request):
    if request.method == 'POST':
            profile_image = request.POST['profile_image']
            name = request.POST['name']
            phone = int(request.POST['phone'])
            email = request.POST['email']
            passw = request.POST['passw']
            gender = request.POST['gender']
            address = request.POST['address']
            service_provided = request.POST['service_provided']
            experience = int(request.POST['experience'])
            specialization = request.POST['specialization']
            description = request.POST['description']
            no_of_services = int(request.POST.get('no_of_service_provided', 0))  

            Employee.objects.create(
                profile_image=profile_image,
                name=name,
                phone=phone,
                email=email,
                passw=passw,
                gender=gender,
                address=address,
                service_provided=service_provided,
                experience=experience,
                specialization=specialization,
                description=description,
                no_of_service_provided=no_of_services  )
            return HttpResponseRedirect('/employeeinfo')  
    
    return render(request, 'templates/admin/addemp.html')
def userinfo(request):
    query = request.GET.get('q', '').strip()  # Get search query from request
    s3 = Cdetail.objects.all()

    if query:
        s3 = Cdetail.objects.filter(
            name__icontains=query
        ) | Cdetail.objects.filter(
            mail__icontains=query
        ) | Cdetail.objects.filter(
            phone__icontains=query
        ) | Cdetail.objects.filter(
            address__icontains=query
        )

    context = {
        'data': s3,
        'search_query': query  # Pass query back to template for persistence
    }
    return render(request, 'admin/userinfo.html', context)

def employeeinfo(request):
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        employees = Employee.objects.filter(
            name__icontains=search_query
        ) | Employee.objects.filter(
            email__icontains=search_query
        ) | Employee.objects.filter(
            phone__icontains=search_query
        ) | Employee.objects.filter(
            service_provided__icontains=search_query
        ) | Employee.objects.filter(
            specialization__icontains=search_query
        )
    else:
        employees = Employee.objects.all()

    context = {
        'data': employees,
        'search_query': search_query
    }
    return render(request, 'admin/employeeinfo.html', context)


def delete_employee(request, employee_id):
    """Delete an employee when the delete button is clicked."""
    if request.method == "POST":
        employee = get_object_or_404(Employee, unique=employee_id)  # Get employee or return 404
        employee.delete()
        return redirect("employeeinfo")  # Redirect back to the employee list
    
    return HttpResponseNotAllowed(["POST"])

def ticketraised(request):
    s4=Ticket.objects.all()
    dict2={
        'data':s4
    }
    return render(request, 'templates/admin/ticketraised.html',dict2)

def employeeinfocommon(request, employee_id):
    """Fetch employee details and pass them to the template."""
    employee = get_object_or_404(Employee, unique=employee_id)
    return render(request, "admin/employeeinfocommon.html", {"employeeinfocommon": employee})


@require_POST
def submit_booking(request, unique):
    """Handle booking submissions"""
    try:
        customer_instance = Cdetail.objects.get(mail=request.COOKIES.get('user_email'))
        service_provider_instance = Employee.objects.get(unique=unique)
        
        Bookings.objects.create(
            uniqueuser=customer_instance.unique,
            uniqueservice=service_provider_instance.unique,
            advance=0,
            email=customer_instance.mail
        )
        
        if not customer_instance.servicehistory:
            customer_instance.servicehistory = []
        customer_instance.servicehistory.append(service_provider_instance.unique)
        customer_instance.save()

        return redirect('servicehistory')  # Use URL name, not template path
    
    except (Cdetail.DoesNotExist, Employee.DoesNotExist):
        return redirect('bookservice') 


def favorites(request):
    user_email = request.COOKIES.get('user_email')
    
    if not user_email:
        return redirect('/signin')

    try:
        user = Cdetail.objects.get(mail=user_email)
    except Cdetail.DoesNotExist:
        return redirect('/signin')

    favorite_ids = user.service if user.service else []
    services = Employee.objects.filter(unique__in=favorite_ids)
    
    # Add search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(service_provided__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Add is_favorite annotation (all services in favorites are by definition favorites)
    services = services.annotate(is_favorite=Value(True, output_field=BooleanField()))

    context = {
        'data': services,  # Changed key from 'services' to 'data'
        'search_query': search_query,
        'user_name': user.name,
        'user_email': user.mail
    }

    return render(request, 'templates/user/favorites.html', context)

def raiseticket(request):
    if request.method == 'POST':
        phone=int(request.POST['phone'])
        mail=request.POST['mail']
        ticketdetail=request.POST['ticketdetail']
        
        
        d9=Ticket(mail=mail,phone=phone, ticketdetail=ticketdetail)
        d9.save()
    
        return HttpResponseRedirect('/bookservice')
    return render(request, 'templates/user/raiseticket.html')

def servicehistory(request):
    user_email = request.COOKIES.get('user_email')

    if not user_email:
        return redirect('/signin')

    try:
        user = Cdetail.objects.get(mail=user_email)
    except Cdetail.DoesNotExist:
        return redirect('/signin')

    history_ids = user.servicehistory if user.servicehistory else []
    services = Employee.objects.filter(unique__in=history_ids)

    context = {
        'services': services,
        'user_name': user.name,
        'user_email': user.mail
    }

    return render(request, 'templates/user/servicehistory.html', context)



def usercommon(request, unique):
    usercommon = Employee.objects.get(unique=unique)
    return render(request, 'templates/user/usercommon.html', {'usercommon': usercommon})

def bookservice(request):
    search_query = request.GET.get('q', '')
    user_email = request.COOKIES.get('user_email')
    favorite_ids = []
    
    if user_email:
        try:
            user = Cdetail.objects.get(mail=user_email)
            favorite_ids = user.service or []
        except Cdetail.DoesNotExist:
            pass

    if search_query:
        employees = Employee.objects.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(service_provided__icontains=search_query)
        )
    else:
        employees = Employee.objects.all()
    
    # Add favorite status annotation
    employees = employees.annotate(
        is_favorite=Case(
            When(unique__in=favorite_ids, then=True),
            default=False,
            output_field=BooleanField()
        )
    )
    
    return render(request, 'templates/user/bookservice.html', {
        'data': employees,
        'search_query': search_query
    })
def toggle_favorite(request, employee_id):
    if not request.COOKIES.get('user_email'):
        return JsonResponse({'status': 'error', 'message': 'Not logged in'}, status=401)
    
    try:
        user = Cdetail.objects.get(mail=request.COOKIES['user_email'])
        employee = Employee.objects.get(unique=employee_id)
        
        # Toggle favorite
        if employee.unique in user.service:
            user.service.remove(employee.unique)
            action = 'removed'
        else:
            user.service.append(employee.unique)
            action = 'added'
            
        user.save()
        return JsonResponse({'status': 'success', 'action': action})
    
    except (Cdetail.DoesNotExist, Employee.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Not found'}, status=404)
    
def employeeservicebooked(request):
    # Get the logged-in employee's email from cookies
    employee_email = request.COOKIES.get('user_email')
    
    if not employee_email:
        # If no employee is logged in, return empty context
        context = {'combined_list': []}
        return render(request, 'templates/employee/employeeservicebooked.html', context)
    
    # Get the employee record for the logged-in user
    try:
        employee = Employee.objects.get(email=employee_email)
    except Employee.DoesNotExist:
        # If employee doesn't exist, return empty context
        context = {'combined_list': []}
        return render(request, 'templates/employee/employeeservicebooked.html', context)
    
    # Get only bookings for this employee
    bookings = Bookings.objects.filter(uniqueservice=employee.unique)
    users = Cdetail.objects.all()

    # Create dictionary for user lookup
    user_dict = {user.unique: user for user in users}

    combined = []
    for booking in bookings:
        user = user_dict.get(booking.uniqueuser)
        if user:
            combined.append({
                'booking_unique': booking.unique,    
                'user': user,                        
                'service': employee,  # We already have the employee object                
                'advance': booking.advance           
            })

    context = {
        'combined_list': combined
    }
    return render(request, 'templates/employee/employeeservicebooked.html', context)