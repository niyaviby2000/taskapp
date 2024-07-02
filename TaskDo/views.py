from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View

from TaskDo.forms import TaskForm,RegistrationForm,LoginForm

from TaskDo.models import Task

from django.contrib import messages

from django.utils import timezone

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator

from TaskDo.decorators import signin_required

@method_decorator(signin_required,name="dispatch")
class TaskCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=TaskForm()

        qs=Task.objects.filter(user_object=request.user)

        return render(request,"task_add.html",{"form":form_instance,"data":qs})
    
    def post(self,request,*args,**kwargs):

        form_instance=TaskForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user_object=request.user

            form_instance.save()


            messages.success(request,"task added")

            print("no msg yet")

            return redirect("task-add")
        
        else:

            return render(request,"task_add.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("room")

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_obj)

        return render(request,"task_add.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get(id=id)

        task_obj=Task.objects.get(id=id)

        form_instance=TaskForm(instance=task_obj,data=request.POST)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"task updated")

            return redirect("task-add")
        
        else:

            return render(request,"task_add.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id)

        return render(request,"task_detail.html",{"data":qs})

@method_decorator(signin_required,name="dispatch") 
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Task.objects.get(id=id).delete()

        messages.success(request,"task deleted")

        return redirect("task-add")

class TaskSummaryView(View):

    def get(self,request,*args,**kwargs):

        current_month=timezone.now().month

        current_year=timezone.now().year

        task_list=Task.objects.filter(

            created_date__month=current_month,

            created_date__year=current_year

        )

class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            # form_instance.save()

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            print("no msg yet")

            return redirect("signin")
        
        else:

            return render(request,"register.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=LoginForm()

        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=LoginForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            # print("user",uname,pwd)
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("task-add")
        messages.error(request,"invalid credential")
            
        return render(request,"login.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout=(request)

        return redirect("signin")
