from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from math import ceil
import json
from django.views.decorators.csrf import  csrf_exempt
# from justchola import Checksum
from justchola import keys
MERCHANT_KEY = keys.Secret_key




# Create your views here.

def home(request):
   return render(request, 'store/home.html')

# def about(request):
#    return render(request, 'store/about.html')

# def contactus(request):
#    return render(request, 'store/contactus.html')

def purchase(request):
    current_user = request.user
    print(current_user)
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request, 'store/purchase.html',params)
    


def nav(request):
    return render(request, 'store/nav.html')

# def flutterwave_redirect(request):
#     return render(request, 'store/flutterwave_redirect.html')



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('login')
    if request.method=="POST":

        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
         

        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        
        # PAYMENT INTERGRATION
        id = Order.order_id
        oid=str(id)+"JUSTCHOLA"
        oid=str(id)
        param_dict = {

            'MID': keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict = (param_dict, MERCHANT_KEY)
        return render(request, 'store/flutterwave_redirect.html', {'param_dict': param_dict})

    return render(request, 'store/checkout.html')


@csrf_exempt
def handlerequest(request):

    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = (response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("infykart","")
           
            print(rid)
            filter2= Orders.objects.filter(order_id=rid)
            filter2= Orders.objects.filter(order_id=a)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                post1.oid=a
                post1.amountpaid=b
                post1.paymentstatus="PAID"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

# def confirm_payment(request, pk):
#     cart = Cart.objects.get(id=pk)
#     cart.completed = True
#     cart.save()
#     messages.success(request, "Payment made successfully")
#     return redirect("index")

