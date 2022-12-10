from django.http import HttpResponse
from django.shortcuts import render
import random
import razorpay
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from myapp.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest



def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def coursedetails(request):
    return render(request,'course-details.html')
def courses(request):
    return render(request,'courses.html')
def events(request):
    return render(request,'events.html')
def pricing(request):
    return render(request,'pricing.html')
def trainers(request):
    return render(request,'trainers.html')
def registration(request):
    if request.method == 'GET':
        return render(request,'registration.html')
    else:
        if request.POST['password'] == request.POST['cpassword']:
            password = request.POST['password']
            global user_data
            user_data={
            'uname' : request.POST['name'],
            'uemail' : request.POST['email'],
            'upassword' : request.POST['password'],   
            'ucpassword' : request.POST['cpassword'],
            }
            #return render(request, 'registration.html')
            global otp
            otp = random.randint(1000,9999)
            subject = "Registration"
            message = f"Your OTP is {otp}."
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [request.POST['email']])
            return render(request, 'otp.html', {'msg':'Check Your Inbox!!'})
        else:
            return render(request, 'register.html', {'msg': 'akjsdklasjd'})
        
def otp(request):
    if request.method == 'POST':
            global otp
            if otp == int(request.POST['otp']):
                User.objects.create(
                name = user_data['uname'],
                email = user_data['uemail'],
                password = user_data['upassword'],
                cpassword = user_data['ucpassword']
            )
            return render(request, 'index.html', {'msg': 'Account Successfully created!!'})
    return render(request, 'login.html')
        
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            global user
            user_object = user = User.objects.get(email = request.POST['email'])
            if user_object.password == request.POST['password']:
                request.session['email'] = request.POST['email']

                return render(request, 'index.html',{'user_object':user_object})
            else:
                return render(request, 'login.html', {'msg' : 'Wrong password!!'})
        except:
            return render(request, 'login.html', {'msg': 'Email Does Not Exist!!'})
        
        
def buy(request):
    #payment
    #donation table row create
    #blog_object = user.objects.get()
    currency = 'INR'
    amount = 4500*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    global context
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    #context['single_blog'] = blog_object
    return render(request, 'buy.html', context = context)

       
       
        # authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 

 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(
            #     params_dict)
            # if result is not None:
            amount =4500*100  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'success.html')
            except:

                # if there is an error while capturing payment.
                return render(request, 'fail.html')
                
        # else:
 
            #     # if signature verification fails.
            #     return render(request, 'fail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

    