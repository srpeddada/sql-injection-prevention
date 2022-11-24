from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.defaulttags import register
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
import django.http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import OrderForm, InterestForm
from django.db import connection

def index(request):
    return render(request, 'myapp/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        sql_statement = "SELECT * FROM myapp_login WHERE username = %s AND password = %s"
        print(sql_statement)
        col_list, data = sqlexecute(sql_statement,[username,password])

        print(col_list, data)

        if col_list:
            if len(data) > 0 :
                request.session['login'] = "True"
                request.session.set_expiry(3600)
                # return HttpResponseRedirect(reverse(''))
                # return render(request, 'myapp/empdetails.html')
                return HttpResponseRedirect(reverse('nds_app:empdet'))
            else:
                request.session['login'] = "False"
                return HttpResponse('Invalid login details.')
        else:
            return render(request, 'myapp/index.html')


        # user = authenticate(username=username, password=password)
        # if user:
        #     if user.is_active:
        #         login(request, user)
        #         return HttpResponseRedirect(reverse('myapp:index'))
        #     else:
        #         return HttpResponse('Your account is disabled.')
        # else:
        #     return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        sql_statement = "SELECT * FROM myapp_adminlogin WHERE username = %s AND password = %s"
        print(sql_statement)
        col_list, data = sqlexecute(sql_statement, [username,password])

        print(col_list, data)

        if col_list:
            if len(data) > 0:
                request.session['admin_login'] = "True"
                request.session.set_expiry(3600)
                # return HttpResponseRedirect(reverse(''))
                return HttpResponseRedirect(reverse('nds_app:admindet'))
            else:
                request.session['admin_login'] = "False"
                return HttpResponse('Invalid login details.')
        else:
            return render(request, 'myapp/index.html')
    else:
        return render(request, 'myapp/admin_login.html')

def sqlexecute(sql_statement, parameters):
    try:
        print("in side sql function")
        cursor = connection.cursor()
        col_list = []
        if ";" in sql_statement:
            data = cursor.executescript(sql_statement,parameters)
        else:
            data = cursor.execute(sql_statement,parameters)
            if cursor.description:
                for i in range(len(cursor.description)):
                    col_list.append(cursor.description[i][0])
        data = data.fetchall()
        results = []
        for i in data:
            results.append(list(i))
        return col_list, results
    except Exception as e:
        return 0, 0




def empdet(request):
    if request.method == 'POST':
        empID = request.POST['empID']
        print(empID, "data-------------")
        sql_statement = "SELECT * FROM myapp_employee WHERE Eid = %s"
        col_list, data = sqlexecute(sql_statement, [empID,])
        print(col_list, data)
        if col_list:
            return render(request, 'myapp/empdetails.html', {'columns': col_list, 'data': data})
        else:
            return render(request, 'myapp/index.html')
    else:
        return render(request, 'myapp/empdetails.html')

def admindet(request):
    sql_statement = "SELECT * FROM myapp_employee emp inner join myapp_empsin esin ON emp.eid = esin.eid order by emp.id"
    col_list, data = sqlexecute(sql_statement,[])
    print(col_list, data)
    if col_list:
        return render(request, 'myapp/admindetails.html', {'columns': col_list, 'data': data})
    else:
        return render(request, 'myapp/index.html')

def adminedit(request, id):
    # return render(request, 'myapp/.html')
    if request.method == 'POST':
        print(id, "id")
        username = request.POST['user_name']
        status = request.POST['statusq']
        depart = request.POST['departq']
        sin = request.POST['sinq']
        salary = request.POST['salaryq']

        sql_statement1 = "UPDATE myapp_employee SET name = %s, status = %s ,department = %s Where eid = %s"
        sql_statement2 = "UPDATE myapp_empsin SET sin = %s, salary = %s Where eid = %s"
        print(sql_statement1)
        print(sql_statement2)
        sqlexecute(sql_statement1,[username, status, depart, str(id)])
        sqlexecute(sql_statement2, [sin, salary, str(id)])
        dict1 = ''
        # sql_statement = "SELECT * FROM myapp_employee emp inner join myapp_empsin esin ON emp.eid = esin.eid where emp.Eid = "+str(id)
        # col_list, data = sqlexecute(sql_statement)
        # dict1 = dict(zip(col_list, list(data[0])))
    else:
        #print(id)
        sql_statement = "SELECT * FROM myapp_employee emp inner join myapp_empsin esin ON emp.eid = esin.eid where emp.Eid = %s"
        args = [str(id),]
        col_list, data = sqlexecute(sql_statement, args)
        #print(col_list)
        if col_list:
            dict1 = dict(zip(col_list, data[0]))
        else:
            return render(request, 'myapp/index.html')
        #print(dict1)

    # if request.method == "POST":
    #     search_word = request.POST['data']
    #     print(search_word)
    return render(request, 'myapp/adminedit.html', {"dictionary": dict1})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#This is a test view function
def test(request):
    #print(no, "helloooooooooo")
    if request.method == 'POST':
        username = request.POST['user']

        cursor = connection.cursor()
        cursor.execute("SELECT name ,stock FROM myapp_product WHERE stock =" + username)
        col_list =[]
        for i in range(len(cursor.description)):
            col_list.append(cursor.description[i][0])
        print(col_list)

        #data1 = cursor.fetchone()
       # print(list(data1))

        #data2 = cursor.execute("select name,type from sqlite_master")
        #print(list(data2))

        #data1 = cursor.executescript("SELECT * FROM myapp_product WHERE stock =" + username)
        #data1 = cursor.executescript("SELECT * FROM myapp_product WHERE stock =" + username + "; UPDATE myapp_product SET stock =100")
        #print(cursor.fetchall())

    return render(request, 'myapp/test.html')
