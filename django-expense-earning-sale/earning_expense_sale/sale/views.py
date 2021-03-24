from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Sale
from django.contrib import messages
import json
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from party.models import Party



def search_sales(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        start_date = json.loads(request.body).get('startDate')
        end_date = json.loads(request.body).get('endDate')
        sales = None
        if search_str.isdigit():
            sales = Sale.objects.filter(amount__gte=float(search_str))
            sales = sales | Sale.objects.filter(name__icontains=search_str) | Sale.objects.filter(area__icontains = search_str) | Sale.objects.filter(bill_no__icontains = search_str)
        else:
            sales = Sale.objects.filter(name__icontains=search_str) | Sale.objects.filter(area__icontains = search_str) | Sale.objects.filter(bill_no__icontains = search_str)
        if start_date:
            sales = (sales.filter(date__month__gte=parse_date(start_date).month) & sales.filter(date__day__gte=parse_date(start_date).day) & sales.filter(date__year__gte=parse_date(start_date).year))
        if end_date:
            sales = (sales.filter(date__month__lte=parse_date(end_date).month) & sales.filter(date__day__lte=parse_date(end_date).day) & sales.filter(date__year__lte=parse_date(end_date).year))
            
        data = sales.values()
        return JsonResponse(list(data),safe=False)


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    sales = Sale.objects.all()
    context = {
        'sales' : sales
    }
    return render(request, 'sale/index.html', context)


def add_sale(request):
    party = Party.objects.all().order_by('name')
    context = {
        'values': request.POST,
        'parties' : party
    }
    if request.method == 'GET':
        return render(request, 'sale/add_sale.html', context=context)

    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        bill = request.POST['bill_no']
        amount = request.POST['amount']
        date = request.POST['sale_date']
        if not name:
            messages.error(request,'name is required')
            return render(request, 'sale/add_sale.html', context=context)
        if not amount:
            messages.error(request,'amount is required')
            return render(request, 'sale/add_sale.html', context=context)
        if not bill:
            messages.error(request,'bill no. is required')
            return render(request, 'sale/add_sale.html', context=context)
        if not date:
            Sale.objects.create(name=extracted_name, amount=amount, bill_no = bill, area=area)
        else:
            Sale.objects.create(name=extracted_name, amount=amount, bill_no = bill, area=area, date=date)
        messages.success(request, 'entry saved successfully')
        return redirect('sales')


def edit_sale(request, id):
    sale = Sale.objects.get(pk=id)
    party = Party.objects.all().order_by('name')
    context = {
        'expense': sale,
        'values' : sale,
        'parties' : party
    }
    if request.method == 'GET':
        return render(request, 'sale/edit_sale.html', context)
     
    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        bill = request.POST['bill_no']
        amount = request.POST['amount']
        date = request.POST['sale_date']
        if not name:
            messages.error(request,'name is required')
            return render(request, 'sale/edit_sale.html', context=context)
        if not amount:
            messages.error(request,'amount is required')
            return render(request, 'sale/edit_sale.html', context=context)
        if not bill:
            messages.error(request,'bill no. is required')
            return render(request, 'sale/edit_sale.html', context=context)
        
        sale.name = extracted_name
        sale.amount = amount
        sale.bill_no = bill
        sale.area = area
        if date:
            sale.date = date
        sale.save()
        messages.success(request, 'entry updated successfully')
        return redirect('sales')
    
def delete_sale(request, id):
    sale = Sale.objects.get(pk=id)
    sale.delete()
    messages.success(request, 'entry deleted')
    return redirect('sales')