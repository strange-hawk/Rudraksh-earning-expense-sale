from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from django.contrib import messages
import json
from party.models import Party
from django.http import JsonResponse
from django.utils.dateparse import parse_date

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        start_date = json.loads(request.body).get('startDate')
        end_date = json.loads(request.body).get('endDate')
        
        expenses = None
        
        if search_str.isdigit():
            expenses = Expense.objects.filter(amount__gte=float(search_str))
            expenses = expenses | Expense.objects.filter(name__icontains=search_str) | Expense.objects.filter(area__icontains=search_str) | Expense.objects.filter(purpose__icontains=search_str)
        else:
            expenses = Expense.objects.filter(name__icontains=search_str) | Expense.objects.filter(area__icontains=search_str) | Expense.objects.filter(purpose__icontains=search_str)
        print(len(expenses))
        if start_date:
            expenses = (expenses.filter(date__month__gte=parse_date(start_date).month) & expenses.filter(date__day__gte=parse_date(start_date).day) & expenses.filter(date__year__gte=parse_date(start_date).year))
        if end_date:
            expenses = (expenses.filter(date__month__lte=parse_date(end_date).month) & expenses.filter(date__day__lte=parse_date(end_date).day) & expenses.filter(date__year__lte=parse_date(end_date).year))
        data = expenses.values()
        return JsonResponse(list(data),safe=False)




@login_required(login_url="/authentication/login")
def index(request):
    expenses = Expense.objects.all()
    context = {
        'expenses' : expenses
    }
    return render(request, 'expense/index.html', context)


def add_expense(request):
    party = Party.objects.all().order_by('name')
    context = {
        'values': request.POST,
        'parties' : party
    }
    if request.method == 'GET':
        return render(request, 'expense/add_expense.html', context=context)

    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        amount = request.POST['amount']
        date = request.POST['expense_date']
        purpose = request.POST['purpose']
        if purpose == None:
            purpose = ""
        if not name:
            messages.error(request,'name is required')
            return render(request, 'expense/add_expense.html', context=context)
        if not amount:
            messages.error(request,'amount is required')
            return render(request, 'expense/add_expense.html', context=context)
        if not date:
            Expense.objects.create(name=name, amount=amount, area=area, purpose=purpose)
        else:
            Expense.objects.create(name=name, amount=amount,area=area, purpose=purpose, date=date)
        messages.success(request, 'entry saved successfully')
        return redirect('expenses')
    
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    party = Party.objects.all().order_by('name')
    context = {
        'expense': expense,
        'values' : expense,
        'parties' : party
    }
    if request.method == 'GET':
        return render(request, 'expense/edit_expense.html', context)
     
    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        amount = request.POST['amount']
        date = request.POST['expense_date']
        purpose = request.POST['purpose']
        if purpose == None:
            purpose = ""
        if not name:
            messages.error(request,'name is required')
            return render(request, 'expense/add_expense.html', context=context)
        if not amount:
            messages.error(request,'amount is required')
            return render(request, 'expense/edit_expense.html', context=context)
        
        expense.name = name
        expense.area = area
        expense.purpose = purpose
        expense.amount = amount
        if date:
            expense.date = date
        expense.save()
        messages.success(request, 'entry updated successfully')
        return redirect('expenses')
    
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'entry deleted')
    return redirect('expenses')