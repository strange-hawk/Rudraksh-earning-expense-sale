from django.shortcuts import render, redirect
from  .models import Party
from expense.models import Expense
from sale.models import Sale
from earning.models import Earning
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse, HttpResponse
import datetime
from weasyprint import HTML
from django.db.models import Sum
import tempfile
from django.template.loader import render_to_string
# Create your views here.

def search_parties(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        parties = None
        parties = Party.objects.filter(name__icontains=search_str) | Party.objects.filter(area__icontains=search_str) | Party.objects.filter(reference__icontains=search_str) | Party.objects.filter(contact__icontains=search_str)
        
        data = parties.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url = 'authentication/login')
def index(request):
    parties = Party.objects.all()
    context = {
        'parties' : parties
    }
    return render(request, 'party/index.html', context)


def add_party(request):
    context = {
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'party/add-party.html', context=context)

    if request.method == 'POST':
        name = request.POST['name']
        area = request.POST['area']
        reference = request.POST['reference']
        contact = request.POST['contact']
        if not name:
            messages.error(request,'name is required')
            return render(request, 'party/add-party.html', context=context)
        if not area:
            messages.error(request,'area is required')
            return render(request, 'party/add-party.html', context=context)
        if not reference : 
            messages.error(request,'reference is required')
            return render(request, 'party/add-party.html', context=context)
        if not contact : 
            messages.error(request,'contact is required')
            return render(request, 'party/add-party.html', context=context)
        if (not contact.isdigit()) or (len(contact)!=10):
            messages.error(request,'wrong contact')
            return render(request, 'party/add-party.html', context=context)
        Party.objects.create(name=name, area=area, reference=reference, contact=contact)
        messages.success(request, 'entry saved successfully')
        return redirect('party')
    
    
def edit_party(request, id):
    party = Party.objects.get(pk=id)
    context = {
        'expense': party,
        'values' : party,
    }
    if request.method == 'GET':
        return render(request, 'party/edit-party.html', context)
     
    if request.method == 'POST':
        name = request.POST['name']
        area = request.POST['area']
        reference = request.POST['reference']
        contact = request.POST['contact']
        if not name:
            messages.error(request,'name is required')
            return render(request, 'party/edit-party.html', context=context)
        if not area:
            messages.error(request,'area is required')
            return render(request, 'party/edit-party.html', context=context)
        if not reference : 
            messages.error(request,'reference is required')
            return render(request, 'party/edit-party.html', context=context)
        if not contact : 
            messages.error(request,'contact is required')
            return render(request, 'party/edit-party.html', context=context)
        if (not contact.isdigit()) or (len(contact)!=10):
            messages.error(request,'wrong contact')
            return render(request, 'party/edit-party.html', context=context)
         
        party.name = name
        party.area = area
        party.reference = reference
        party.contact = contact
        party.save()
        messages.success(request, 'entry updated successfully')
        return redirect('party')
    
    
def delete_party(request, id):
    party = Party.objects.get(pk=id)
    party.delete()
    messages.success(request, 'entry deleted')
    return redirect('party')

def export_pdf(request):
    response = HttpResponse(content_type= 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Report'+str(datetime.date.today().strftime('%d-%m-%Y'))+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    today = datetime.date.today()
    expense = Expense.objects.filter(date__month=today.month) & Expense.objects.filter(date__day=today.day) & Expense.objects.filter(date__year=today.year)
    earning = Earning.objects.filter(date__month=today.month) & Earning.objects.filter(date__day=today.day) & Earning.objects.filter(date__year=today.year)
    sale = Sale.objects.filter(date__month=today.month) & Sale.objects.filter(date__day=today.day) & Sale.objects.filter(date__year=today.year)
    today_date = 'Report       ' + str(today.day) + '-' + str(today.month) + '-' + str(today.year)
    html_string = render_to_string('party/pdf-output.html', {'expenses':expense, 'totalexpense' : round(expense.aggregate(Sum('amount'))['amount__sum'],2), 'earnings':earning, 'totalearning' : round(earning.aggregate(Sum('amount'))['amount__sum'],2), 'sales':sale, 'totalsale' : round(sale.aggregate(Sum('amount'))['amount__sum'],2), 'day':today.day, 'month': today.month, 'year' : today.year, 'today_date':today_date})
    
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    # today_date = today.day + '-' + today.month+1 + '-' + today.year
    return response
    # print(earning.aggregate(Sum('amount'))['amount__sum'])
    return render(request, 'party/pdf-output.html', {'expenses':expense, 'totalexpense' : round(expense.aggregate(Sum('amount'))['amount__sum'],2), 'earnings':earning, 'totalearning' : round(earning.aggregate(Sum('amount'))['amount__sum'],2), 'sales':sale, 'totalsale' : round(sale.aggregate(Sum('amount'))['amount__sum'],2), 'today_date':today_date})


# 'party/pdf-output.html', {'expenses':expense, 'totalexpense' : round(expense.aggregate(Sum('amount'))['amount__sum'],2), 'earnings':earning, 'totalearning' : round(earning.aggregate(Sum('amount'))['amount__sum'],2), 'sales':sale, 'totalsale' : round(sale.aggregate(Sum('amount'))['amount__sum'],2), 'today_date':today_date})
# 'party/pdf-output.html', {'expenses':expense, 'totalexpense' : round(expense.aggregate(Sum('amount'))['amount__sum'],2), 'earnings':earning, 'totalearning' : round(earning.aggregate(Sum('amount'))['amount__sum'],2), 'sales':sale, 'totalsale' : round(sale.aggregate(Sum('amount'))['amount__sum'],2), 'day':today.day, 'month': today.month, 'year' : today.year, 'today_date':today_date})