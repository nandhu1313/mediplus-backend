import random
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from home.models import Product, User
from home.serializers import ProductSerializer, UserSerializer
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# pdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
import pyqrcode
import png
import os
from PIL import Image
# pdf end

# Create your views here.

@api_view()
def home(request):
    return Response({'message': "APIs for Vicodin Application"})


@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        email = serializer.data['email']
        password = serializer.data['password']
        queryset = User.objects.all()
        for user in queryset:
            if user.password == password:
                if user.email == email:
                    return Response({"message":"true", "user_id":user.id})
        return Response({"message":"false"})


@api_view(['GET','PUT','DELETE'])
def user(request, id):

    try:
        user = get_object_or_404(User, id=id) 
    except:
        pass

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def products(request):
    try:
        products = list(Product.objects.all().values() )
    except:
        pass

    if request.method == 'GET':
        return JsonResponse(products, safe=False)


@api_view(['GET'])
def product(request, id):
    try:
        product = get_object_or_404(Product, id=id) 
    except:
        pass

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

@api_view(['GET'])
def search(request, query):
    try:
        products = list(Product.objects.filter(title__contains=query).values() )
    except:
        pass

    if request.method == 'GET':
        return JsonResponse(products, safe=False)
    

@api_view(['POST'])
def buy(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        product_string = serializer.data['title']
        subtotal = serializer.data['mrp']
        user_id = int(serializer.data['category'])
        order_id = random.randint(100000, 999999)
        product_list = product_string.split(",")
        del product_list[-1]
        product_list_int = []
        for id in product_list:
            product_list_int.append(int(id))
        cart_items = Product.objects.filter(id__in=product_list_int)
        user = User.objects.get(id=user_id)

        # QR Code
        url = f'upi://pay?pa=9496671855@paytm&pn=Anandh&am={subtotal}.00&cu=INR&tn=Your Taste.it UPI Payment'
        qrcode = pyqrcode.create(url)
        qrcode.png('media/uploads/qr_code/'+str(order_id) +"upicode.png", scale=8)
        # QR Code End


         #library to get logo related information
        #convert the font so it is compatible
        pdfmetrics.registerFont(TTFont('Arial','Arial.ttf'))
        #import company's logo
        im = Image.open('media/uploads/qr_code/'+str(order_id) +'upicode.png')
        width, height = im.size
        ratio = width/height
        image_width = 400
        image_height = int(image_width / ratio)
        #import company's logo
        tasteit = Image.open('tasteit.png')
        width2, height2 = tasteit.size
        ratio2 = width2/height2
        image_width2 = 400
        image_height2 = int(image_width2 / ratio2)
        #Page information
        page_width = 2156
        page_height = 3050
        #Invoice variables
        location = 'Pathanamthitta'
        margin = 100
        #def function
        def create_bill():
            #Creating a pdf file and setting a naming convention
            pdf_name = str(order_id)+'.pdf'
            save_name = os.path.join(settings.BASE_DIR, "media/uploads/bills/", pdf_name)
            c = canvas.Canvas(save_name)
            c.setPageSize((page_width, page_height))                
            #Drawing the image
            c.drawImage("tasteit.png", 150,
                                2500,
                                image_width2, image_height2, mask='auto')
            #Invoice information
            c.setFont('Arial',80)
            text = 'E-BILL'
            text_width = stringWidth(text,'Arial',80)
            c.drawString((page_width-text_width)/2, page_height - image_height - margin, text)
            y = page_height - image_height - margin*4
            x = 2*margin
            x2 = x + 550
            c.setFont('Arial', 45)
            c.drawString(x, y, 'Sold by: ')
            c.drawString(x2,y, 'Vicodin - Online Medical Store')
            y -= margin
            c.drawString(x, y,'')
            c.drawString(x2, y+30, location)
            y -= margin
            c.drawString(x,y,'Issued to: ')
            c.drawString(x2,y, user.name )
            y -= margin
            c.drawString(x, y,'')
            c.drawString(x2, y+30, user.location)
            y -= margin 
            c.drawString(x, y,'')
            c.drawString(x2, y+60, user.location)
            y -= margin 
            c.drawString(x,y,'Order ID: ')
            c.drawString(x2,y, str(order_id))
            y -= margin
            c.drawString(x,y, 'Order Date: ')
            c.drawString(x2,y, '14-03-2023')
            y -= margin
            y -= margin *2 
            # Table head
            c.drawString(x,y, 'Sl No ')
            xx = x+200
            c.drawString(xx,y, 'Item Name ')
            xx = xx+400
            c.drawString(xx,y, 'MRP ')
            xx = xx+200
            c.drawString(xx,y, 'ORP ')
            xx = xx+200
            c.drawString(xx,y, 'Quantity ')
            xx = xx+250
            c.drawString(xx,y, 'Seller ')
            xx = xx+400
            c.drawString(xx,y, 'Total ')
            y -= 50
            c.line(margin+80, y, page_width-200, y)
            y -= margin-30

        # For loop
            # Table Body
            sl_no = 1
            sub_total = 0
            for item in cart_items:
                quantity = 0
                for id in product_list_int:
                    if int(item.id) == int(id):
                        quantity+=1
                total = quantity * item.mrp
                c.drawString(x,y, str(sl_no))
                xx = x+200
                c.drawString(xx,y, item.title)
                xx = xx+400
                c.drawString(xx,y, str(item.mrp))
                xx = xx+200
                c.drawString(xx,y, str(item.mrp))
                xx = xx+200
                c.drawString(xx,y, str(quantity))
                xx = xx+250
                c.drawString(xx,y, 'Vicodin')
                xx = xx+400
                c.drawString(xx,y, str(total))
                y -= 100
                sl_no+=1
                sub_total+=subtotal
            # Table Body End
        # For loop End
            
            c.line(margin+80, y, page_width-200, y)
            y -= margin
            c.drawString(xx,y, f'Rs. {sub_total}')
            y -= margin
            y -= margin*3      
            c.drawString(x,y,'Digitaly signed by Vicodin')
            y -= margin
            c.drawString(x,y,'Scan the QR Code to make the payment using UPI')
            y -= margin
            c.drawString(x,y,'In case of any questions, contact support@vicodin.com')    
            #Drawing the image
            c.drawInlineImage('media/uploads/qr_code/'+ str(order_id) +"upicode.png", 1600,
                                y-30,
                                image_width, image_height)

            #Saving the pdf file
            c.save()
        create_bill()

        user_email = user.email
        subject = 'Vicodin'
        message = f'Your order has been placed successfuly'
        print(user_email)
        recipient = user_email
        mail = EmailMessage(subject, message, to=[recipient])
        mail.attach_file('media/uploads/bills/'+str(order_id)+'.pdf')
        mail.send(fail_silently=False)

        return Response(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
