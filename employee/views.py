# Create your views here.
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import EmployeeForm, ProductForm
from .models import Employee, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from rest_framework import filters


#signup & login & logout
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'employee/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/home')
    else:
        form = AuthenticationForm()
    return render(request, 'employee/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/home')

#employee

def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, 'employee/index.html', {'form':form})

def show(request):
    if request.user.is_authenticated:
        sort = request.GET.get('sort', '')
        desc = request.GET.get('desc', False)
        cuser= Employee.objects.all()
        # search
        ctx = {}
        url_parameter = request.GET.get("q")
        if url_parameter:
            employees = cuser.filter(fname__icontains=url_parameter)
        else:
            employees = cuser

            if sort:
                if desc:
                    employees = employees.order_by("-" + sort)
                else:
                    employees = employees.order_by(sort)
                    
        page = request.GET.get('page', 1)
        paginator = Paginator(employees, 3)
        try:
            employees = paginator.page(page)
        except PageNotAnInteger:
            employees = paginator.page(1)
        except EmptyPage:
            employees = paginator.page(paginator.num_pages)
        ctx["desc"] = desc
        ctx["q"] = url_parameter
        ctx["employees"] = employees
        ctx["sorts"] = sort

        if request.is_ajax():
            html = render_to_string(
                template_name="employee/showuserfile.html",
                context={"employees" : employees, "q" : url_parameter, "desc" : desc, "sorts" : sort}
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, "employee/show.html", context=ctx)
    else:
        return redirect('/login')
def edit(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'employee/edit.html', {'employee': employee})

def update(request, id):
    if request.user.is_authenticated:
        employee = Employee.objects.get(id=id)
        if request.method == "POST":
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('/show')
        form = EmployeeForm(instance=employee)

        return render(request, 'employee/edit.html', {'employee': form, "id": id})
    else:
        return redirect('/')

def destroy(request, id):
    Employee.objects.get(id=id).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

#product
def prd(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/showp')
            except:
                pass
    else:
        form = ProductForm()
    return render(request, 'employee/indexp.html', {'form': form})

def showp(request):
    products = Product.objects.all()
    if request.GET.get('user_id', ''):
        user = Employee.objects.get(id=request.GET.get('user_id'))
        products = user.product.all()
    return render(request, "employee/showp.html", {'products':products})


def editp(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'employee/editp.html', {'product', product})

def updatep(request, id):
    # product = Product.objects.get(id=id)
    # form = ProductForm(request.POST, instance = product)
    # if form.is_valid():
    #     form.save()
    #     return redirect("/showp")
    # return render(request, 'employee/editp.html', {'product': product})

    product = Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/showp')
    form = ProductForm(instance=product)

    return render(request, 'employee/editp.html', {'product': form, "id": id})

def destroyp(id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("/showp")

def home(request):
    return render(request, "employee/home.html")
#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    search_fields = ['^fname', '=lname', '=email']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    queryset = Employee.objects.all().order_by('-fname')
    serializer_class = EmployeeSerializer
    ordering_fields = ['fname', 'lname']

    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('id').reverse()
    serializer_class = ProductSerializer




def showdata(request):
    return render(request, 'employee/showdata.html')

