import requests
from django.conf.urls import url
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import StudentForm, HeadmasterForm, ParentForm, DriverForm, CreateSchool, AddUser, loginForm, SchoolForm, \
    DriverSearch, PickyAuthenticationForm
from .models import *
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.contrib.auth.views import PasswordResetView


# --------------------------------------------------FORGOT PASSWORD-----------------------------------------------------
def forgot_password(request):
    if request.method == 'POST':
        return PasswordResetView(request,
                                 from_email=request.POST.get('email'))
    else:
        return render(request, 'Base/forgot_password.html')


# --------------------------------------------------CHANGE PASSWORD-----------------------------------------------------
def change_password(request):
    message = " "
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('رمز عبور شما با موفقیت تغییر یافت!'))
            message = "رمز عبور شما با موفقیت تغییر یافت!"
        else:
            message = 'لطفا خطای زیر را برطرف کنید.'
            messages.error(request, _('لطفا خطای زیر را برطرف کنید.'))

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Base/change_password.html', {
        'form': form, "message": message
    })


# --------------------------------------------------LOGIN---------------------------------------------------------------
class Login(View):

    def get(self, request):
        form = PickyAuthenticationForm()
        return render(request, "Base/login.html", context={"form": form})

    def post(self, request):
        message = ''
        cd_form = loginForm(request.POST)
        if cd_form.is_valid():
            cd = cd_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                client = User.objects.get(username=cd['username'])
                # return redirect("/home")
                message1 = client.first_name + " " + client.last_name
                message = message1 + " " + " عزیز خوش آمدی"
                return render(request, 'Base/base.html', {"message": message})


            else:
                message = "نام کاربری یا رمز عبور شما اشتباه است مجددا تلاش کنید"

        else:
            print(cd_form.errors)
        form = PickyAuthenticationForm()
        return render(request, "Base/login.html", context={"message": message, "form": form})


# --------------------------------------------------JOIN STUDENT&DRIVER-------------------------------------------------
class join(View):
    def get(self, request, driver_id):
        list_student = []
        student_choice = []
        driver = []
        if "action" in request.GET and "id" in request.GET:
            if request.GET["action"] == "add":
                try:
                    student = Student.objects.get(id=request.GET["id"])
                    #    driver = UserProfile.objects.get(id=driver_id)
                    DriverStudent.objects.create(student=student, driver=driver.user)
                #    student_choice = DriverStudent.objects.filter(driver_id=driver.user.id)
                # for i in student_choice:
                #     list_student.append(User.objects.get(id=i.student_id))
                except:
                    print("Error")

            elif request.GET["action"] == "dell":
                try:
                    student = Student.objects.get(id=request.GET["id"])
                    DriverStudent.objects.filter(student_id=student.id).delete()
                except:
                    print("UU")
        #     driver = UserProfile.objects.get(id=driver_id)
        #    student_choice = DriverStudent.objects.filter(driver_id=driver.user.id)
        # for i in student_choice:
        #     list_student.append(User.objects.get(id=i.student_id))

        driver = UserProfile.objects.get(id=driver_id)
        student_choice = DriverStudent.objects.filter(driver_id=driver.user.id)

        try:
            driver = UserProfile.objects.get(id=driver_id)
            students = Student.objects.filter().exclude(user_id__in=student_choice.values("student_id"))
            paginator = Paginator(students, 8)  # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        except NameError:
            pass
        else:
            return render(request, "Base/join.html",
                          {"driver": driver, "contents": page_obj, "student_choice": student_choice})
        return render(request, "Base/join.html")


# ----------------------------------------------PARENT------------------------------------------------------------------
class Main(View):
    def get(self, request):
        return render(request, 'Base/base.html')


# ----------------------------------------------SCHOOL------------------------------------------------------------------
class School_list(View):
    def get(self, request):
        if "delete" in request.GET:
            temp = School.objects.get(id=request.GET["delete"])
            list_member = UserProfile.objects.filter(school=temp)
            for item in list_member:
                User.objects.get(id=item.user_id).delete()
            temp.delete()
        contact_list = School.objects.filter()
        master = UserProfile.objects.filter(user_type=1)
        paginator = Paginator(contact_list, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/SchoolList.html',
                      context={"contents": page_obj, 'master': master})


class AddSchool(View):
    def get(self, request):
        form = SchoolForm()
        return render(request, 'Base/AddSchool.html', {'form': form})

    def post(self, request):
        message = ""
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            message = "مشخصات مورد نظر با موفقیت ثبت گردید"
        else:
            message = "مشکلی بوجود آمده لطفا مجددا تلاش کنید"
        form = SchoolForm()
        args = {'form': form, "message": message}
        return render(request, 'Base/AddSchool.html', args)


class UpdateSchool(View):
    def get(self, request, id):
        print(id)
        data_input = {}
        try:
            temp = School.objects.get(id=id)
        except:
            print("no")
        else:
            data_input = {
                "lng": temp.lng,
                "lat": temp.lat,
                "name_school": temp.name_school,
                "mobile_school": temp.mobile_school,
            }
        form = SchoolForm(initial=data_input)
        return render(request, 'Base/AddSchool.html', {'form': form})

    def post(self, request, id):
        try:
            temp = School.objects.get(id=id)
            print(temp)
        except:
            print("no")
        else:
            form = SchoolForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                temp.name_school = cd["name_school"]
                temp.mobile_school = cd["mobile_school"]
                temp.lat = cd["lat"]
                temp.lng = cd["lng"]
                temp.save()
                return redirect('/school')
            else:
                return render(request, 'Base/SchoolList.html')


# ----------------------------------------------PARENT------------------------------------------------------------------
class Parent(View):
    def get(self, request):
        if "delete" in request.GET:
            parent = User.objects.get(id=request.GET["delete"]).delete()
            list_student = ParentsStudent.objects.filter(parents_id=request.GET["delete"])
            for item in list_student:
                Student.objects.get(id=item.student_id).delete()
                item.delete()
        if "schoolID" in request.GET:
            contents = UserProfile.objects.filter(user_type=4, school_id=request.GET["schoolID"])
        else:
            contents = UserProfile.objects.filter(user_type=4)
        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = ParentForm()
        return render(request, 'Base/ParentList.html', context={'form': form, "contents": page_obj})


class AddParent(View):
    def get(self, request):
        form = ParentForm()
        if "schoolID" in request.GET:
            contents = UserProfile.objects.filter(user_type=4, school_id=request.GET["schoolID"])
        else:
            contents = UserProfile.objects.filter(user_type=4)
        paginator = Paginator(contents, 3)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/parentschool.html', context={"contents": page_obj, "form": form})

    def post(self, request):
        message = ''
        form = ParentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            parent = User.objects.create_user(password=cd["mobile"], username=cd["mobile"], email=cd["email"],
                                              first_name=cd["first_name"], last_name=cd["last_name"])
            if "schoolID" in request.GET:
                schools = School.objects.get(id=request.GET["schoolID"])
                UserProfile.objects.create(user=parent, mobile=cd["mobile"], user_type=cd["user_type"], school=schools)
                contents = UserProfile.objects.filter(user_type=4, school_id=request.GET["schoolID"])
            else:
                UserProfile.objects.create(user=parent, mobile=cd["mobile"], user_type=cd["user_type"])
                contents = UserProfile.objects.filter(user_type=4)
            message = "مشخصات مورد نظر با موفقیت ثبت گردید"
            parentsID = parent.id
            form = ParentForm()
            schoolId = request.GET["schoolID"]
            args = {'form': form, 'contents': contents, 'parentsID': parentsID, "message": message,
                    "schoolId": schoolId}
            return render(request, 'Base/parentschool.html', args)
        else:
            message = "مشکلی بوجود آمده لطفا مجددا تلاش کنید"
            form = ParentForm()
            if "schoolID" in request.GET:
                contents = UserProfile.objects.filter(user_type=4, school_id=request.GET["schoolID"])
            else:
                contents = UserProfile.objects.filter(user_type=4)
            args = {'form': form, 'contents': contents, 'pas': "/parent/", "message": message}
            return render(request, 'Base/parentschool.html', args)


class UpdateParent(View):
    def get(self, request):
        message = ""
        data_input = {}
        try:
            temp = UserProfile.objects.get(user_id=request.GET["display"])
        except:
            print("Error")
        else:
            data_input = {
                "mobile": temp.mobile,
                "email": temp.user.email,
                "last_name": temp.user.last_name,
                "first_name": temp.user.first_name,
            }
        form = ParentForm(initial=data_input)
        if "display" in request.GET:
            try:
                list_student = ParentsStudent.objects.filter(parents_id=request.GET["display"])
            except:
                message = "شما هنوز فرزندان خود را به لیست اضافه نکرده اید"
            else:
                students = list_student
        else:
            students = ParentsStudent.objects.filter()
        paginator = Paginator(students, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/AddParent.html',
                      context={"contents": page_obj, "form": form, 'message': message})

    def post(self, request):
        try:
            temp = UserProfile.objects.get(user_id=request.GET['display'])
        except:
            print("no")
        else:
            form = ParentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                temp.mobile = cd["mobile"]
                temp.user.email = cd["email"]
                temp.user_type = cd["user_type"]
                temp.user.last_name = cd["last_name"]
                temp.user.first_name = cd["first_name"]
                temp.save()
                temp.user.save()
                return redirect('/parent-school/?schoolID=%s' % temp.school_id)
        form = ParentForm()
        return render(request, 'Base/AddParent.html', {'form': form})


# ----------------------------------------------STUDENT-------------------------------------------------------------------
class StudentList(View):
    def get(self, request):
        if "delete" in request.GET:
            temp = Student.objects.get(id=request.GET["delete"])
            temp.delete()
        if "display" in request.GET:
            parent = UserProfile.objects.get(user_type=4, school_id=request.GET["display"])
            contents = Student.objects.get(school_id=parent.school_id)
        else:
            contents = Student.objects.filter()
        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/StudentList.html', {"contents": page_obj})


class AddStudent(View):
    def get(self, request):
        if "display" in request.GET:
            parent = UserProfile.objects.get(user_id=request.GET["display"])
            formStudent = StudentForm(initial={'user_type': 'دانش آموزان'})
            list_student = ParentsStudent.objects.filter(parents_id=parent.user_id)
            paginator = Paginator(list_student, 8)  # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Base/Prent_Student.html',
                          context={"contents": page_obj, 'parent': parent, "form": formStudent, 'pas': "/school/"})
        else:
            print("Error")
            return redirect('/parent-school')

    def post(self, request):
        message = ""
        form = StudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if "display" in request.GET:
                location = Destination.objects.create(title=cd["title"], latitude=cd["latitude"],
                                                      longitude=cd["longitude"],
                                                      latitudeDelta=cd["latitudeDelta"],
                                                      longitudeDelta=cd["longitudeDelta"],
                                                      is_active=cd["is_active"])
                # position = Position.objects.create(title=cd["title"], bus_to_home=cd["latitude"],
                #                                    bus_to_school=cd["longitude"],
                #                                    home_to_bus=cd["latitudeDelta"],
                #                                    school_to_bus=cd["longitudeDelta"],
                #                                    status=cd["is_active"])
                school_parent = UserProfile.objects.get(user_id=request.GET["display"])
                student = Student.objects.create(name=cd["name"], className=cd["className"],
                                                 school=school_parent.school, location=location)
                ParentsStudent.objects.create(user_student=student, student_id=student.id,
                                              parents_id=request.GET["display"],
                                              )
            else:
                message = "ارتباط شما با دانش آموز برقرار نشد"
            form = StudentForm()
            parent = UserProfile.objects.get(user_id=request.GET["display"])
            student_list = ParentsStudent.objects.filter(parents_id=parent.user_id)
            paginator = Paginator(student_list, 8)  # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Base/Prent_Student.html',
                          context={"contents": page_obj, 'parent': parent, 'form': form, "message": message})
        else:
            message = "مشکلی بوجود آمده لطفا مجددا تلاش کنید"
            form = ParentForm()
            parent = UserProfile.objects.get(user_id=request.GET["display"])
            contents = UserProfile.objects.filter(user_type=4)
            paginator = Paginator(contents, 8)  # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'Base/Prent_Student.html',
                          context={"contents": page_obj, 'parent': parent, 'form': form, "message": message})


class UpdateStudent(View):
    def get(self, request, id):
        data_input = {}
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            data_input = {
                "lat": temp.user,
                "lng": temp.user.email,
                "last_name": temp.user.last_name,
                "first_name": temp.user.first_name,
            }
        form = StudentForm(initial=data_input)
        return render(request, 'Base/AddStudent.html', {'form': form})

    def post(self, request, id):
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            form = StudentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                temp.mobile = "12525365478"
                temp.user.email = "h@g.com"
                temp.user_type = cd["user_type"]
                temp.user.last_name = cd["last_name"]
                temp.user.first_name = cd["first_name"]
                temp.save()
                temp.user.save()
                return redirect("/student/add/?display=14")
        return render(request, 'Base/AddStudent.html', {'form': form})


# ----------------------------------------------HEADMASTER--------------------------------------------------------------
class Headmaster(View):
    def get(self, request):
        if "delete" in request.GET:
            temp = User.objects.get(id=request.GET["delete"])
            temp.delete()
        contents = UserProfile.objects.filter(user_type=1)
        paginator = Paginator(contents, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = HeadmasterForm()
        return render(request, 'Base/HeadmasterList.html', context={'form': form, "contents": page_obj})


class AddHeadmaster(View):
    def get(self, request):
        form = HeadmasterForm()
        if "delete" in request.GET:
            temp = User.objects.get(id=request.GET["delete"])
            temp.delete()
        if "schoolID" in request.GET:
            headmaster = UserProfile.objects.filter(user_type=1, school_id=request.GET["schoolID"])
            contents = UserProfile.objects.filter(user_type=5, school_id=request.GET["schoolID"])
        else:
            headmaster = UserProfile.objects.filter(user_type=1, school_id=request.GET["schoolID"])
            contents = UserProfile.objects.filter(user_type=5, school_id=request.GET["schoolID"])
        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/AddHeadmaster.html',
                      context={'form': form, "contents": page_obj, 'headmaster': headmaster})

    def post(self, request):
        message = ""
        form = HeadmasterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if 1 == cd["user_type"]:
                try:
                    headmaster = UserProfile.objects.get(user_type=cd["user_type"])
                except:
                    master = User.objects.create_user(password=cd["mobile"], username=cd["mobile"], email=cd["email"],
                                                      first_name=cd["first_name"], last_name=cd["last_name"])
                    if "schoolID" in request.GET:
                        schools = School.objects.get(id=request.GET["schoolID"])
                        UserProfile.objects.create(user=master, mobile=cd["mobile"], user_type=cd["user_type"],
                                                   school=schools)
                        message = "مشخصات مورد نظر با موفقیت ثبت گردید"
                else:
                    message = "مشخصات مدیر قبلا ذخیره گردیده شما مجاز به انتخاب ادمین هستید"

            form = HeadmasterForm()
        else:
            message = "مشکلی بوجود آمده لطفا مجددا تلاش کنید"
        headmaster = UserProfile.objects.filter(user_type=1, school=schools)
        admins = UserProfile.objects.filter(user_type=5, school=schools)

        args = {'form': form, 'headmaster': headmaster, "message": message, 'contents': admins}
        return render(request, 'Base/AddHeadmaster.html', args)


class UpdateHeadmaster(View):
    def get(self, request, id):
        data_input = {}
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            data_input = {
                "mobile": temp.mobile,
                "email": temp.user.email,
                "last_name": temp.user.last_name,
                "first_name": temp.user.first_name,
            }
        list_headmaster = UserProfile.objects.filter(user_type=1)
        form = HeadmasterForm(initial=data_input)
        paginator = Paginator(list_headmaster, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/AddHeadmaster.html',
                      context={"contents": page_obj, "form": form})

    def post(self, request, id):
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            form = HeadmasterForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                temp.mobile = cd["mobile"]
                temp.user.email = cd["email"]
                temp.user_type = cd["user_type"]
                temp.user.last_name = cd["last_name"]
                temp.user.first_name = cd["first_name"]
                temp.user.save()
                return redirect('/headmaster/add/')
        form = HeadmasterForm()
        return render(request, 'Base/AddHeadmaster.html', {'form': form})


# ----------------------------------------------DRIVER------------------------------------------------------------------
class Driver(View):
    def get(self, request):
        if "delete" in request.GET:
            driver = User.objects.get(id=request.GET["delete"]).delete()
            list_student = DriverStudent.objects.filter(driver_id=request.GET["delete"])
            for item in list_student:
                User.objects.get(id=item.student_id).delete()
                item.delete()
        if "schoolID" in request.GET:
            contents = UserProfile.objects.filter(user_type=3, school_id=request.GET["schoolID"])
        else:
            if 'search' in request.GET:
                contents = UserProfile.objects.filter(user_type=3).filter(
                    Q(user__first_name__contains=request.GET["search"]) |
                    Q(user__last_name__contains=request.GET["search"]) |
                    Q(mobile__contains=request.GET["search"])

                )
                search = request.GET["search"]
            else:
                contents = UserProfile.objects.filter(user_type=3)
                search = ""

        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = DriverForm()
        return render(request, 'Base/DriverList.html',
                      context={'form': form, "contents": page_obj, "search": search})


class AddDriver(View):
    def get(self, request):
        form = DriverForm()
        if "schoolID" in request.GET:
            contents = UserProfile.objects.filter(user_type=3, school_id=request.GET["schoolID"])
        else:
            contents = UserProfile.objects.filter(user_type=3)
        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Base/AddDriver.html', context={'form': form, "contents": page_obj})

    def post(self, request):
        message = ''
        form = DriverForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            driver = User.objects.create_user(password=cd["mobile"], username=cd["mobile"], email=cd["email"],
                                              first_name=cd["first_name"], last_name=cd["last_name"])
            if "schoolID" in request.GET:
                schools = School.objects.get(id=request.GET["schoolID"])
                UserProfile.objects.create(user=driver, mobile=cd["mobile"], user_type=cd["user_type"],
                                           school=schools)
                contents = UserProfile.objects.filter(user_type=3, school_id=request.GET["schoolID"])
            else:
                UserProfile.objects.create(user=driver, mobile=cd["mobile"], user_type=cd["user_type"])
                contents = UserProfile.objects.filter(user_type=3)
            message = "مشخصات مورد نظر با موفقیت ثبت گردید"
            form = DriverForm()
            args = {'form': form, 'contents': contents, "message": message}
            return render(request, 'Base/AddDriver.html', args)
        else:
            message = "مشکلی بوجود آمده لطفا مجددا تلاش کنید"
            form = DriverForm()
            if "schoolID" in request.GET:
                contents = UserProfile.objects.filter(user_type=3, school_id=request.GET["schoolID"])
            else:
                contents = UserProfile.objects.filter(user_type=3)
            args = {'form': form, 'contents': contents, "message": message}
            return render(request, 'Base/AddDriver.html', args)


class UpdateDriver(View):
    def get(self, request, id):
        data_input = {}
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            data_input = {
                "mobile": temp.mobile,
                "email": temp.user.email,
                "last_name": temp.user.last_name,
                "first_name": temp.user.first_name,
            }
        contents = UserProfile.objects.filter(user_type=3)
        paginator = Paginator(contents, 8)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = DriverForm(initial=data_input)
        return render(request, 'Base/AddDriver.html',
                      context={'form': form, "contents": page_obj})

    def post(self, request, id):
        try:
            temp = UserProfile.objects.get(id=id)
        except:
            print("no")
        else:
            form = DriverForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                temp.mobile = cd["mobile"]
                temp.user.email = cd["email"]
                temp.user_type = cd["user_type"]
                temp.user.last_name = cd["last_name"]
                temp.user.first_name = cd["first_name"]
                temp.save()
                temp.user.save()
                return redirect('/driver/add/')
        contents = UserProfile.objects.filter(user_type=3)
        args = {' contents': contents, 'form': form, 'pas': "/driver/"}
        return render(request, 'Base/AddDriver.html', args)
