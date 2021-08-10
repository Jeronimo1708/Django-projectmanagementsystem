from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from powercons_app.models import CustomUser, AdminUser, Staffs, Projects, Tasks, Clients, Contracts
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
    
    # For Saffs
    # staff_attendance_present_list=[]
    # staff_attendance_leave_list=[]
    # staff_name_list=[]

    # staffs = Staffs.objects.all()
    # for staff in staffs:
    #     subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
    #     attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
    #     leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
    #     staff_attendance_present_list.append(attendance)
    #     staff_attendance_leave_list.append(leaves)
    #     staff_name_list.append(staff.admin.first_name)
        
    
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
        # "staff_attendance_present_list": staff_attendance_present_list,
        # "staff_attendance_leave_list": staff_attendance_leave_list,
        # "staff_name_list": staff_name_list,
        # "student_attendance_present_list": student_attendance_present_list,
        # "student_attendance_leave_list": student_attendance_leave_list,
        # "student_name_list": student_name_list,
    }
    return render(request, "admintemplate/home_content.html", context)
    
def add_client(request):
    return render(request, "admintemplate/add_client_template.html")


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
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
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
        address = request.POST.get('address')

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
            staff_model.address = address
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
        project = request.POST.get('project')
        try:
            project_model = Projects(project_name=project)
            project_model.save()
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
        "id": project_id
    }
    return render(request, 'admintemplate/edit_course_template.html', context)


def edit_project_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project')

        try:
            project = Projects.objects.get(id=project_id)
            project.project_name = project_name
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
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')

        try:
            contractdate = Contracts(contract_start_date=contract_start_date, contract_end_date=contract_end_date)
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
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')

        try:
            contract_year = Contracts.objects.get(id=contract_id)
            contract_year.contract_start_date = contract_start_date
            contract_year.contract_end_date = contract_end_date
            contract_year.save()

            messages.success(request, "Contract Updated Successfully.")
            return redirect('/edit_contract/'+contract_id)
        except:
            messages.error(request, "Failed to Update Contract Year.")
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




def add_student_save(request):
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
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course_id']
            #gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year_obj

                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Student Added Successfully!")
                return redirect('add_student')
            except:
                messages.error(request, "Failed to Add Student!")
                return redirect('add_student')
        else:
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['course_id'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                course = Courses.objects.get(id=course_id)
                student_model.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)



def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)



def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


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



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


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


def student_profile(requtest):
    pass