from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Earning
from sale.models import Sale
from django.contrib import messages
import json
from django.http import JsonResponse
from django.utils.dateparse import parse_date


def search_earnings(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        start_date = json.loads(request.body).get('startDate')
        end_date = json.loads(request.body).get('endDate')
        earnings = None
        if search_str.isdigit():
            earnings = Earning.objects.filter(amount__gte=float(search_str))
            earnings = earnings | Earning.objects.filter(name__icontains=search_str) | Earning.objects.filter(area__icontains = search_str) | Earning.objects.filter(mode__icontains = search_str)
        else:
            earnings = Earning.objects.filter(name__icontains=search_str) | Earning.objects.filter(area__icontains = search_str) | Earning.objects.filter(mode__icontains = search_str)
        if start_date:
            earnings = (earnings.filter(date__month__gte=parse_date(start_date).month) & earnings.filter(date__day__gte=parse_date(start_date).day) & earnings.filter(date__year__gte=parse_date(start_date).year))
        if end_date:
            earnings = (earnings.filter(date__month__lte=parse_date(end_date).month) & earnings.filter(date__day__lte=parse_date(end_date).day) & earnings.filter(date__year__lte=parse_date(end_date).year))
        data = earnings.values()
        return JsonResponse(list(data),safe=False)





# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    earning = Earning.objects.all()
    context = {
        'earnings' : earning
    }
    return render(request, 'earning/index.html', context)

def add_earning(request):
    sales = Sale.objects.all().order_by('name')
    context = {
        'values': request.POST,
        'sales' : sales
    }
    
    if request.method == 'GET':
        return render(request, 'earning/add_earning.html', context=context)
    
    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        mode = request.POST['mode']
        amount = request.POST['amount']
        date = request.POST['earning_date']
        name = request.POST['name']
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'earning/add_earning.html', context=context)
        if not date:
            Earning.objects.create(name=extracted_name, mode=mode, amount=amount, area = area)
        else:
            Earning.objects.create(name=extracted_name, mode=mode, amount=amount, area = area, date = date)
        messages.success(request, 'entry saved successfully')
        return redirect('earning')
    

        
            
def edit_earning(request, id):
    sales = Sale.objects.all()
    earning = Earning.objects.get(pk=id)
    context = {
        'expense': earning,
        'values' : earning,
        'sales':sales
    }
    if request.method == 'GET':
        return render(request, 'earning/edit_earning.html', context)
    
    if request.method == 'POST':
        name_area= str(request.POST['name'])
        name = name_area.split('#')[0]
        area = name_area.split('#')[1]
        extracted_name = name_area[:-len(area)-1]
        mode = request.POST['mode']
        amount = request.POST['amount']
        date = request.POST['earning_date']
        name = request.POST['name']
        
        earning.name = extracted_name
        earning.area = area
        earning.amount = amount
        earning.mode = mode
        if date:
            earning.date = date
        earning.save()
        messages.success(request, 'entry updated')
        return redirect('earning')
            

def delete_earning(request, id):
    earning = Earning.objects.get(pk=id)
    earning.delete()
    messages.success(request, 'entry deleted')
    return redirect('earning')