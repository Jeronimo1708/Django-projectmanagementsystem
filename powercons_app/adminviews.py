from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from powercons_app.models import CustomUser, AdminUser, Staffs, Projects, Tasks, Clients, Contracts, Suppliers, Services, Parts, Payments, Documents, Locations
from .forms import AddClientForm, EditClientForm

def admin_home(request):
    all_client_count = Clients.objects.all().count()
    task_count = Tasks.objects.all().count()
    project_count = Projects.objects.all().count()
    staff_count = Staffs.objects.all().count()
    
    # Total Tasks and clients in Each Project
    project_all = Projects.objects.all()
    project_name_list = []
    task_count_list = []
    client_count_list_in_project = []
    
    for project in project_all:
        tasks = Tasks.objects.filter(project_id=project.id).count()
        clients = Clients.objects.filter(project_id=project.id).count()
        project_name_list.append(project.project_name)
        task_count_list.append(tasks)
        client_count_list_in_project.append(clients)
        
    task_all = Tasks.objects.all()
    task_list = []
    client_count_list_in_task = []
    for task in task_all:
        project = Projects.objects.get(id=task.project_id.id)
        client_count = Clients.objects.filter(project_id=project.id).count()
        task_list.append(task.task_name)
        client_count_list_in_task.append(client_count)

    
    context={
        "all_client_count": all_client_count,
        "task_count": task_count,
        "project_count": project_count,
        "staff_count": staff_count,
        "project_name_list": project_name_list,
        "task_count_list": task_count_list,
        "client_count_list_in_project": client_count_list_in_project,
        "task_list": task_list,
        "client_count_list_in_task": client_count_list_in_task,
    }
    return render(request, "admintemplate/home_content.html", context)
    
def add_staff(request):
    return render(request, "admintemplate/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            staffs = Staffs.objects.create(admin=user, phone=phone)
            user.staffs.phone = phone
            user.staffs.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')



def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "admintemplate/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "admintemplate/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.phone = phone
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)



def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')




def add_project(request):
    return render(request, "admintemplate/add_project_template.html")


def add_project_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_project')
    else:
        # project_name = request.POST.get('project')
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        try:
            projects = Projects(project_name=project_name, project_description=project_description)
            projects.project_name=project_name
            projects.project_description=project_description
            projects.save()
            messages.success(request, "Project Added Successfully!")
            return redirect('add_project')
        except:
            messages.error(request, "Failed to Add Project!")
            return redirect('add_project')


def manage_project(request):
    projects = Projects.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'admintemplate/manage_project_template.html', context)


def edit_project(request, project_id):
    project = Projects.objects.get(id=project_id)
    context = {
        "project": project,
        #"project_description": project_description,
        "id": project_id
    }
    return render(request, 'admintemplate/edit_project_template.html', context)


def edit_project_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')

        try:
            project = Projects.objects.get(id=project_id)
            project.project_name = project_name
            project.project_description = project_description
            project.save()

            messages.success(request, "Project Updated Successfully.")
            return redirect('/edit_project/'+project_id)

        except:
            messages.error(request, "Failed to Update Project.")
            return redirect('/edit_project/'+project_id)


def delete_project(request, project_id):
    project = Projects.objects.get(id=project_id)
    try:
        project.delete()
        messages.success(request, "Project Deleted Successfully.")
        return redirect('manage_project')
    except:
        messages.error(request, "Failed to Delete Project.")
        return redirect('manage_project')


def manage_contract(request):
    contracts = Contracts.objects.all()
    context = {
        "contracts": contracts
    }
    return render(request, "admintemplate/manage_contracts_template.html", context)


def add_contract(request):
    return render(request, "admintemplate/add_contracts_template.html")


def add_contract_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_project')
    else:
        contract_name = request.POST.get('contract_name')
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')

        try:
            contract = Contracts(contract_name=contract_name, contract_start_date=contract_start_date, contract_end_date=contract_end_date)
            contract.save()
            messages.success(request, "Contract added Successfully!")
            return redirect("add_contract")
        except:
            messages.error(request, "Failed to Add Contract")
            return redirect("add_contract")


def edit_contract(request, contract_id):
    contracts = Contracts.objects.get(id=contract_id)
    context = {
        "contracts": contracts
    }
    return render(request, "admintemplate/edit_contracts_template.html", context)


def edit_contract_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_contract')
    else:
        contract_id = request.POST.get('contract_id')
        contract_name = request.POST.get('contract_name')
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')
        
        try:
            contracts = Contracts.objects.get(id=contract_id)
            contracts.contract_name = contract_name
            contracts.contract_start_date = contract_start_date
            contracts.contract_end_date = contract_end_date
            contracts.save()

            messages.success(request, "Contract Updated Successfully.")
            return redirect('/edit_contract/'+contract_id)
        except:
            messages.error(request, "Failed to Update Contract.")
            return redirect('/edit_contract/'+contract_id)


def delete_contract(request, contract_id):
    contract = Contracts.objects.get(id=contract_id)
    try:
        contract.delete()
        messages.success(request, "Contract Deleted Successfully.")
        return redirect('manage_contract')
    except:
        messages.error(request, "Failed to Delete Contract.")
        return redirect('manage_contract')



def add_client(request):
    form = AddClientForm()
    context = {
        "form": form
    }
    return render(request, 'admintemplate/add_client_template.html', context)


def add_client_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_client')
    else:
        
        form = AddClientForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            project = form.cleaned_data['project_id']
            contract = form.cleaned_data['contract_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            # if len(request.FILES) != 0:
            #     profile_pic = request.FILES['profile_pic']
            #     fs = FileSystemStorage()
            #     filename = fs.save(profile_pic.name, profile_pic)
            #     profile_pic_url = fs.url(filename)
            # else:
            #     profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                clients = Clients.objects.create(admin=user, phone=phone, location=location, project_id=project, contract_id=contract)
                user.clients.location = location
                user.clients.phone = phone

                project_obj = Projects.objects.get(id=project)
                user.clients.project_id = project_obj

                contract_obj = Contracts.objects.get(id=contract)
                user.clients.contract_id = contract_obj

                user.clients.save()
                messages.success(request, "Client Added Successfully!")
                return redirect('add_client')
            except:
                messages.error(request, "Failed to Add Client!")
                return redirect('add_client')
        else:
            return redirect('add_client')


def manage_client(request):
    clients = Clients.objects.all()
    context = {
        "clients": clients
    }
    return render(request, 'admintemplate/manage_client_template.html', context)


def edit_client(request, client_id):
    request.session['client_id'] = client_id

    client = Clients.objects.get(admin=client_id)
    form = EditClientForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = client.admin.email
    form.fields['username'].initial = client.admin.username
    form.fields['first_name'].initial = client.admin.first_name
    form.fields['last_name'].initial = client.admin.last_name
    form.fields['location'].initial = client.location
    form.fields['project_id'].initial = client.project_id.id
    form.fields['contract_id'].initial = client.contract_id.id

    context = {
        "id": client_id,
        "username": client.admin.username,
        "form": form
    }
    return render(request, "admintemplate/edit_client_template.html", context)


def edit_client_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        client_id = request.session.get('client_id')
        if client_id == None:
            return redirect('/manage_client')

        form = EditClientForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            location = form.cleaned_data['location']
            project_id = form.cleaned_data['project_id']
            contract_id = form.cleaned_data['contract_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            # if len(request.FILES) != 0:
            #     profile_pic = request.FILES['profile_pic']
            #     fs = FileSystemStorage()
            #     filename = fs.save(profile_pic.name, profile_pic)
            #     profile_pic_url = fs.url(filename)
            # else:
            #     profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=client_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Client Table
                client_model = Clients.objects.get(admin=client_id)
                client_model.location = location

                project = Projects.objects.get(id=project_id)
                client_model.project_id = project

                contract_obj = Contracts.objects.get(id=contract_id)
                client_model.contract_id = contract_obj

                client_model.save()
                del request.session['client_id']

                messages.success(request, "Client Updated Successfully!")
                return redirect('/edit_client/'+client_id)
            except:
                messages.success(request, "Failed to Uupdate Client.")
                return redirect('/edit_client/'+client_id)
        else:
            return redirect('/edit_client/'+client_id)


def delete_client(request, client_id):
    client = Clients.objects.get(admin=client_id)
    try:
        client.delete()
        messages.success(request, "Client Deleted Successfully.")
        return redirect('manage_client')
    except:
        messages.error(request, "Failed to Delete Client.")
        return redirect('manage_client')


def add_task(request):
    projects = Projects.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "projects": projects,
        "staffs": staffs
    }
    return render(request, 'admintemplate/add_task_template.html', context)



def add_task_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_task')
    else:
        task_name = request.POST.get('task')

        project_id = request.POST.get('project')
        project = Projects.objects.get(id=project_id)
        
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            task = Tasks(task_name=task_name, project_id=project, staff_id=staff)
            task.save()
            messages.success(request, "Task Added Successfully!")
            return redirect('add_task')
        except:
            messages.error(request, "Failed to Add Task!")
            return redirect('add_task')


def manage_task(request):
    tasks = Tasks.objects.all()
    context = {
        "tasks": tasks
    }
    return render(request, 'admintemplate/manage_task_template.html', context)


def edit_task(request, task_id):
    task = Tasks.objects.get(id=task_id)
    projects = Projects.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "task": task,
        "projects": projects,
        "staffs": staffs,
        "id": task_id
    }
    return render(request, 'admintemplate/edit_task_template.html', context)


def edit_task_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        task_id = request.POST.get('task_id')
        task_name = request.POST.get('task')
        project_id = request.POST.get('project')
        staff_id = request.POST.get('staff')

        try:
            task = Tasks.objects.get(id=task_id)
            task.task_name = task_name

            project = Projects.objects.get(id=project_id)
            task.project_id = project

            staff = CustomUser.objects.get(id=staff_id)
            task.staff_id = staff
            
            task.save()

            messages.success(request, "Task Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_task", kwargs={"task_id":task_id}))

        except:
            messages.error(request, "Failed to Update Task.")
            return HttpResponseRedirect(reverse("edit_task", kwargs={"task_id":task_id}))



def delete_task(request, task_id):
    task = Tasks.objects.get(id=task_id)
    try:
        task.delete()
        messages.success(request, "Task Deleted Successfully.")
        return redirect('manage_task')
    except:
        messages.error(request, "Failed to Delete Task.")
        return redirect('manage_task')
        
    





def add_supplier(request):
    return render(request, "admintemplate/add_suppliers_template.html")


def add_supplier_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_supplier')
    else:
        supplier = request.POST.get('supplier_name')

        try:
            
            #suppliers = Suppliers.objects.create(name=supplier)
            supplier = Suppliers(name=supplier)
            supplier.save()
            messages.success(request, "Supplier added Successfully!")
            return redirect("add_supplier")
        except:
            messages.error(request, "Failed to Add Supplier")
            return redirect("add_supplier")

def manage_supplier(request):
    suppliers = Suppliers.objects.all()
    context = {
        "suppliers": suppliers
    }
    return render(request, 'admintemplate/manage_suppliers_template.html', context)


def edit_supplier(request, supplier_id):
    suppliers = Suppliers.objects.get(id=supplier_id)
    context = {
        "suppliers": suppliers,
        "id": supplier_id
    }
    return render(request, "admintemplate/edit_suppliers_template.html", context)


def edit_supplier_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        supplier_id = request.POST.get('supplier_id')
        supplier_name = request.POST.get('supplier_name')

        try:
            suppliers = Suppliers.objects.get(id=supplier_id)
            suppliers.name = supplier_name
            suppliers.save()

            messages.success(request, "Supplier Updated Successfully.")
            return redirect('/edit_supplier/'+supplier_id)
        except:
            messages.error(request, "Failed to Update Supplier.")
            return redirect('/edit_supplier/'+supplier_id)


def delete_supplier(request, supplier_id):
    supplier = Suppliers.objects.get(id=supplier_id)
    try:
        supplier.delete()
        messages.success(request, "Supplier Deleted Successfully.")
        return redirect('manage_supplier')
    except:
        messages.error(request, "Failed to Delete Supplier.")
        return redirect('manage_supplier')
        


def add_service(request):
    suppliers = Suppliers.objects.all()
    context = {
        "suppliers": suppliers
    }
    return render(request, 'admintemplate/add_services_template.html', context)



def add_service_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_service')
    else:
        name = request.POST.get('service_name')
        service_type = request.POST.get('service_type')

        supplier_id = request.POST.get('supplier')
        suppliers = Suppliers.objects.get(id=supplier_id)
        
        try:
            service = Services(name=name, service_type=service_type, supplier_id=suppliers)
            service.save()
            messages.success(request, "Service Added Successfully!")
            return redirect('add_service')
        except:
            messages.error(request, "Failed to Add Service!")
            return redirect('add_service')


def manage_service(request):
    services = Services.objects.all()
    context = {
        "services": services
    }
    return render(request, 'admintemplate/manage_services_template.html', context)


def edit_service(request, service_id):
    service = Services.objects.get(id=service_id)
    suppliers = Suppliers.objects.all()
    context = {
        "service": service,
        "suppliers": suppliers,
        "id": service_id
    }
    return render(request, 'admintemplate/edit_services_template.html', context)


def edit_service_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        service_id = request.POST.get('task_id')
        service_name = request.POST.get('task')
        supplier_id = request.POST.get('project')
        
        try:
            service = Services.objects.get(id=service_id)
            service.name = service_name
            supplier = Supplier.objects.get(id=supplier_id)
            service.supplier_id = suppliertask.staff_id = staff
            service.save()
            messages.success(request, "Service Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_service", kwargs={"service_id":service_id}))
        except:
            messages.error(request, "Failed to Update Service.")
            return HttpResponseRedirect(reverse("edit_service", kwargs={"service_id":service_id}))



def delete_service(request, service_id):
    service = Services.objects.get(id=service_id)
    try:
        service.delete()
        messages.success(request, "Service Deleted Successfully.")
        return redirect('manage_service')
    except:
        messages.error(request, "Failed to Delete Service.")
        return redirect('manage_service')
        
 


def add_part(request):
    suppliers = Suppliers.objects.all()
    context = {
        "suppliers": suppliers
    }
    return render(request, 'admintemplate/add_parts_template.html', context)



def add_part_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_part')
    else:
        part_name = request.POST.get('part_name')
        part_type = request.POST.get('part_type')
        supplier_id = request.POST.get('suppliers')
        suppliers = Suppliers.objects.get(id=supplier_id)
        

        try:
            part = Parts(name=part_name, part_type=part_type, supplier_id=supplier)
            part.save()
            messages.success(request, "Part Added Successfully!")
            return redirect('add_part')
        except:
            messages.error(request, "Failed to Add Part!")
            return redirect('add_part')


def manage_part(request):
    parts = Parts.objects.all()
    context = {
        "parts": parts
    }
    return render(request, 'admintemplate/manage_parts_template.html', context)


def edit_part(request, part_id):
    part = Parts.objects.get(id=part_id)
    suppliers = Suppliers.objects.all()
    context = {
        "part": part,
        "suppliers": suppliers,
        "id": part_id
    }
    return render(request, 'admintemplate/edit_parts_template.html', context)


def edit_part_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        part_id = request.POST.get('part_id')
        part_name = request.POST.get('part')
        part_type = request.POST.get('part')
        supplier_id = request.POST.get('supplier')
        
        try:
            part = Parts.objects.get(id=part_id)
            part.name = part_name
            part.type = part_type
            supplier = Supplier.objects.get(id=supplier_id)
            part.supplier_id = part
            part.save()
            messages.success(request, "Part Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_part", kwargs={"part_id":part_id}))
        except:
            messages.error(request, "Failed to Update Part.")
            return HttpResponseRedirect(reverse("edit_part", kwargs={"part_id":part_id}))



def delete_part(request, part_id):
    part = Parts.objects.get(id=part_id)
    try:
        part.delete()
        messages.success(request, "Part Deleted Successfully.")
        return redirect('manage_part')
    except:
        messages.error(request, "Failed to Delete Part.")
        return redirect('manage_part')      

# def add_supplier(request):
#     return render(request, "admintemplate/add_suppliers_template.html")


# def add_supplier_save(request):
#     if request.method != "POST":
#         messages.error(request, "Invalid Method")
#         return redirect('add_supplier')
#     else:
#         supplier_name = request.POST.get('supplier_name')

#         try:
#             supplier = Suppliers(supplier_name=supplier_name)
#             supplier.save()
#             messages.success(request, "Supplier added Successfully!")
#             return redirect("add_supplier")
#         except:
#             messages.error(request, "Failed to Add Supplier")
#             return redirect("add_supplier")


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)






def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admintemplate/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def staff_profile(request):
    pass


def client_profile(requtest):
    pass
