# Necessary Website creation Libraries
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

# For Pagination Mainly for the Product Menu Pages
from django.core.paginator import Paginator

# To create those pop-up messages under a specific set of conditions
from django.contrib import messages

# For PDF support

#import i
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#For API Calls
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


#For Django Paypal Integration
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

# Connecting from other code files from the Customers Django App
from Customers.forms import *
from Customers.models import *
from Customers.views import *

# Connecting from other code files in same Django project
from .models import *
from .forms import *
from .api import *
from .cart import *

def HomePage(request):
    # Slide Show Images Being Pulled From the AWS S3 QT Bucket
    SS1 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_1.PNG"
    SS2 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_2.PNG"
    SS3 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_3.PNG"
    SS4 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_4.PNG"
    SS5 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_5.PNG"
    SS6 = "https://qt-bucket.s3.amazonaws.com/Images/Home_Page_Slide_Show_Pic_6.PNG"
    
    #BTC_Logo = Pictures.objects.get(pk=7)
    #ETH_Logo = Pictures.objects.get(pk=8)
    

    # For Fetching Crypto Data Using Coin Market Cap API
    Coin_Market_Cap_IDs = {
        "BTC": "1",
        "ETH": "1027",
        "USDT": "825",
        "SOL": "5426",
        "USDC": "3408",
        "DOGE": "74",
        "LTC": "2", 
        }

    BTC_PRICE = round(Home_Page_API.Crypto_Pricing_Data(Coin_ID=Coin_Market_Cap_IDs["BTC"], Currency="USD"), 2)
    ETH_PRICE = round(Home_Page_API.Crypto_Pricing_Data(Coin_ID=Coin_Market_Cap_IDs["ETH"], Currency="USD"), 2)
    USDT_PRICE = round(Home_Page_API.Crypto_Pricing_Data(Coin_ID=Coin_Market_Cap_IDs["USDT"], Currency="USD"), 2)
    SOL_PRICE = round(Home_Page_API.Crypto_Pricing_Data(Coin_ID=Coin_Market_Cap_IDs["SOL"], Currency="USD"), 2)

    return render(request, "Home_Page.html", {
        "SS1": SS1, "SS2": SS2, "SS3": SS3, "SS4": SS4, "SS5": SS5, "SS6": SS6, 
        "BTC_PRICE": BTC_PRICE, "ETH_PRICE": ETH_PRICE, "USDT_PRICE": USDT_PRICE, "SOL_PRICE": SOL_PRICE,
    })

def AboutUsPage(request):
    return render(request, "About_Us_Page.html", {

    })

def LocationsPage(request):
    Location = StoreLocations.objects.all().order_by('City')
    City_Temp = Location_Index_Page_API.Current_Weather_API("Burbank", "CA")
    
    return render(request, "Locations_Index_Page.html", {
        "Locations": Location,
        "CityTemp": City_Temp
    })


def ShowLocation(request, Location_ID):
    Location = StoreLocations.objects.get(pk=Location_ID)
    City_Temp = Location_Index_Page_API.Current_Weather_API(f"{Location.City}", "CA")

    return render(request, "Locations_Closer_View_Page.html", {
        "Location": Location,
        "CityTemp": City_Temp,
        })


def UpdateLocation(request, Location_ID):
    Location = StoreLocations.objects.get(pk=Location_ID)
    Form = LocationForm(request.POST or None, request.FILES or None, instance=Location)
    if Form.is_valid():
        Form.save()
        return redirect('LocationPages')
    
    return render(request, "Admin_Update_Location_Page.html", {
        "Location": Location,
        "LocationForm": Form
        })


def DeleteLocation(request, Location_ID):
    Location = StoreLocations.objects.get(pk=Location_ID)
    Location.delete()
    messages.success(request, 'Location deleted successfully!')
    return redirect('LocationPages')

def LocationsPDF(request):
    # Generating a Bytesteam Buffer
    Buf = io.BytesIO()
    
    # Creating a Canvas with the Buf var
    Canvas = canvas.Canvas(Buf, pagesize=letter, bottomup=0)
    
    # Assigning the Beginning of the Canvas Variable to another Variable
    TextObject = Canvas.beginText()
    TextObject.setTextOrigin(inch, inch)
    TextObject.setFont("Helvetica", 14)
    
    Locations = StoreLocations.objects.all()
    
    lines = []
    
    # Adding all the Product Model data into an empty list
    for Location in Locations:
        lines.append(str(Location.Street))
        lines.append(f"{Location.City}, {Location.State} {Location.Zip}")
        lines.append(f"Phone: {Location.Phone}")
        lines.append(f"Opens @ {Location.Opens} am")
        lines.append(f"Closes @ {Location.Closes} pm")
        lines.append(f"")
        
    # Writing all the Data in the lines list onto the PDF canvas
    for line in lines:
        TextObject.textLine(line)
    
    # Drawing, showing, and Saving the Final PDF document
    Canvas.drawText(TextObject)
    Canvas.showPage()
    Canvas.save()
    Buf.seek(0)
    
    #Returning a FileResponse of the data filled PDF document
    return FileResponse(Buf, as_attachment=True, filename="Locations.pdf")


def ProductsPage(request):
    # Creating Pagination for 12 products per page
    Paginate = Paginator(StoreProducts.objects.all().order_by('Brand'), 12)
    Page = request.GET.get("page")
    Products = Paginate.get_page(Page)
    
    Numbers = "h" * Products.paginator.num_pages
    
    # Querying Shop Cart Data only for the User
    #User_Shop_Cart = ShoppingCart.objects.filter(User_id=request.user.id)
    #Total_Price = sum(Item.Product.Price * Item.Amount for Item in User_Shop_Cart)
    
    return render(request, "Product_Menu_Page.html", {
        "PaginatedProducts": Products,
        "Numbers": Numbers,
        #"User_Cart" : User_Shop_Cart,
        #"Total_Price" : Total_Price,
    })


def ShowProduct(request, Product_ID):
    SingleProduct = StoreProducts.objects.get(pk=Product_ID)
    return render(request, "Product_Closer_View_Page.html", {
        "SingleProduct": SingleProduct,
        })
    
def ProductAddPage(request):
    Product = StoreProducts.objects.all()
    
    # Logic for PROMO Pricing Calculation
    # MLG360_Promo = StoreProducts.objects.get("Price")
    
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product = form.save(commit=False)
            Product.save()
            messages.success(request, f'{Product.Name} Successfully Added!')
            return redirect('ProductsPage')
        
        else:
            form = ProductForm
            if 'submitted' in request.GET:
                submitted = True
                
    form = ProductForm
    return render(request, "Admin_Product_Add_Page.html", 
                {'ProductForm': form, 
                'submitted': submitted,
                })


def UpdateProduct(request, Product_ID):
    Product = StoreProducts.objects.get(pk=Product_ID)
    Form = ProductForm(request.POST or None, request.FILES or None, instance=Product)
    if Form.is_valid():
        Form.save()
        messages.success(request, f'{Product.Name} Updated successfully!')
        return redirect('ProductsPage')
    
    return render(request, "Admin_Product_Update_Page.html", {
        "Product": Product,
        "ProductForm": Form
        })

def DeleteProduct(request, Product_ID):
    Product = StoreProducts.objects.get(pk=Product_ID)
    Product.delete()
    messages.success(request, f'{Product.Name} Deleted Successfully!')
    return redirect('ProductsPage')


def ProductSearchPage(request):
    #Product_Brand = StoreProducts.objects.query("Brand")
    Product = StoreProducts.objects.all()
    if request.method == "POST":
        Searched = request.POST['Searched']
        SearchedProducts = StoreProducts.objects.filter(Name__icontains = Searched)
        SearchedBrands = StoreProducts.objects.filter(Brand__icontains = Searched)
        # SearchedKeywords = StoreProducts.objects.filter(Category__icontains = Searched)
        return render(request, "Product_Search_Result.html", {
            'Searched': Searched,
            'SearchProducts': SearchedProducts,
            'SearchedBrands': SearchedBrands,
            # 'SearchedKeywords': SearchedKeywords,
            'Product': Product,
            })
    else:
        return render(request, "Product_Search_Result.html", {
            'Product': Product,
            })
    
def AllPreOrder(request):
    No_Stock_Products = StoreProducts.objects.filter(Stock=0).order_by("Brand")
    
    return render(request, "Product_PreOrder_All.html", {
        "Products": No_Stock_Products,
    })
    
    
def AllPromotions(request):
    
    Promo_Products = StoreProducts.objects.exclude(Coupon=None).order_by("Brand")
    
    return render(request, "Product_OnPromos_Page.html", {
        "Products": Promo_Products,
    })


def ShopCart(request): 
    cart = Cart(request) # Bring in the Cart class from cart.py file
    
    cart_products = cart.view_cart #Get the Carted Products 
    cart_quants = cart.cart_amounts #Get the Qty of each Carted Product
    cart_total_price = cart.total_price
    
    
    return render(request, 'Shopping_Cart_Page.html', {'Cart_Summary': cart_products, "Cart_Amount" : cart_quants, "Cart_Total_Price" : cart_total_price,})
        

# For adding item(s) onto the Shopping Cart 
def ShoppingCartAdd(request):
    # Bring in the Cart class from cart.py file
    cart = Cart(request)
    #The Length of the current User Cookie Unique Shopping Cart
    cart_count = cart.__len__()

    # Check to see if the user is in the POST method when viewing the website
    if request.POST.get('action') == "post": #post action from the Ajax code
    
        product_id = int(request.POST.get("product_id")) #product_id from the Ajax code
        product_qty = int(request.POST.get("product_qty")) #product_qty from the Ajax code
        
        #Query for product in the database
        product = get_object_or_404(StoreProducts, pk=product_id)
        
    
        #Save the user queried product to a Session
        cart.add(product=product, quantity=product_qty)

        # Returns a JSON resonse of the Product`s name in our database
        #ProdNameresponse = JsonResponse({"Prod Name: ": product.Name})
        CartCountResponse = JsonResponse({"Quantity": cart_count})
        messages.success(request, "Item Has Been Added To The Cart!")
    
        return CartCountResponse

# # For Removing item(s) from the Shopping Cart
def ShoppingCartRemove(request):
    cart = Cart(request) # Bring in the Cart class from cart.py file
    
    # Check to see if the user is in the POST method when viewing the website
    if request.POST.get('action') == "post": #post action from the Ajax code
    
        product_id = str(request.POST.get("product_id")) #product_id from the Ajax code
    
        cart.delete(product=product_id)
        response = JsonResponse({"prod":product_id})
        messages.success(request, "Item Has Been Removed From Cart!")
        return response


# # For Removing item(s) from the Shopping Cart
def ShoppingCartUpdate(request):
    cart = Cart(request) # Bring in the Cart class from cart.py file
    
    # Check to see if the user is in the POST method when viewing the website
    if request.POST.get('action') == "post": #post action from the Ajax code
    
        product_id = int(request.POST.get("product_id")) #product_id from the Ajax code
        product_qty = int(request.POST.get("product_qty")) #product_qty from the Ajax code
    
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({"qty":product_qty})
        messages.success(request, "Cart Updated!")
        return response
    
        
        
def PayPal_Successfull_Payment(request):
    return render(request, "PayPal_Payment_Success_Page.html", {})


def PayPal_Failure_Payment(request):
    return render(request, "PayPal_Payment_Failure_Page.html", {})


def PayPal_IPN(request):
    return HttpResponse(status=200)


def ShopCart_CheckOut(request):
    
    # Creating a Cart Instance to acquire the  
    cart = Cart(request)
    cart_products = cart.view_cart
    cart_quantities = cart.cart_amounts
    cart_total_price = cart.total_price
        
    if request.user.is_authenticated: #As long as a logged in user is making a web request
        current_user_shipping = Customer_Shipping.objects.get(id=request.user.id) #Acquire the current logged in user`s shipping information
        ShippingForm = Customer_Shipping_Form(request.POST or None, instance=current_user_shipping)
        return render(request, "Shopping_Cart_Check_Out_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "ShippingForm": ShippingForm,})

    else:
        ShippingForm = Customer_Shipping_Form(request.POST or None)
        return render(request, "Shopping_Cart_Check_Out_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "ShippingForm": ShippingForm,})
            
def OnlineOrderShipped(request):
    #if request.user.is_authenticated and request.user.is_superuser:
    if request.user.is_authenticated:
        ShippedOrders = Online_Orders.objects.filter(Shipment_Released=True)

        if request.POST: #As long as the web user hasn't filled out any form
            Number = request.POST['Number']#Get the POST value from the Shipping_Status Hidden Input Field
            Right_Now_Date = datetime.datetime.now()
            ShippedOrders = Online_Orders.objects.filter(id=Number)
            ShippedOrders.update(Shipment_Released=False, Shipment= Right_Now_Date) #Update that Single Order`s Shipping Status to TRUE
            messages.success(request, "Shipping Status changed to ORDER SHIPMENT PENDING")
            return redirect("HomePage")
        
        else:
            return render(request, "Order_Shipped_Status_Page.html", {"Shipped": ShippedOrders, })
    
    else:
        messages.success(request, "Access Denied!")
        return redirect("HomePage")

def OnlineOrderNotShipped(request):
    if request.user.is_authenticated:
        PendingOrders = Online_Orders.objects.filter(Shipment_Released=False)
        
        if request.POST: #As long as the web user hasn't filled out any form
            Number = request.POST['Number']#Get the POST value from the Shipping_Status Hidden Input Field
            Right_Now_Date = datetime.datetime.now()
            PendingOrders = Online_Orders.objects.filter(id=Number)
            PendingOrders.update(Shipment_Released=True, Shipment= Right_Now_Date) #Update that Single Order`s Shipping Status to TRUE
            messages.success(request, "Shipping Status changed to ORDER HAS SHIPPED")  
            return redirect("HomePage")
        
        else:
            return render(request, "Order_Shipped_Not_Status_Page.html", {"Pending": PendingOrders, })

    else:
        messages.success(request, "Access Denied!")
        return redirect("HomePage")
    
def OnlineOrderProcessing(request):
    if request.POST: #If the web user POSTED data over from the Billing Info Form
        cart = Cart(request)
        cart_products = cart.view_cart
        cart_quantities = cart.cart_amounts
        cart_total_price = cart.total_price()
        
        Billing_Form = OnlineOrderPayments(request.POST or None)
        Processing_Session = request.session.get("Processing_Session")
        
        
        First_Name = Processing_Session['Shipping_First_Name']
        Last_Name = Processing_Session['Shipping_Last_Name']
        Email = Processing_Session['Shipping_Email']
        
        Ship_Address = f'''{Processing_Session['Shipping_Address_Line_1']}\n{Processing_Session['Shipping_Address_Line_2']}\n{Processing_Session['Shipping_City']}\n{Processing_Session['Shipping_State']}\n{Processing_Session['Shipping_ZipCode']}\n{Processing_Session['Shipping_Country']}\n'''
        Total_Amount = cart_total_price
        
        # Online Order Ticket Processing for a Logged In User
        if request.user.is_authenticated: #If the web user is logged in
            user = request.user #Save the Web user to database
            Create_User_Order = Online_Orders(user=user, First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount)
            Create_User_Order.save()
            
            User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
            for Product in cart_products():
                Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
                if Product.On_Sale:
                    Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
                else:
                    Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
                for key, val in cart_quantities().items():
                    if int(key) == Product_ID:
                        val #Carted Product Quantities Number Value
                        #Based on finding all the information above, Create an Orderable Item DB Table
                        Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)    
                        Create_Orderable_Item.save()
                    
            #Delete the Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                    
            #Remove Cart from the Database
            LoggedInUser = WebsiteAccounts.objects.filter(Web_User__id=request.user.id)
            LoggedInUser.update(Old_Cart="") #Replace current Key, Val pair with Nothing 
                    
            messages.success(request, "TEST Use LOG IN Order Has Been Placed!")
            return redirect("HomePage")
        
        # Online Order Ticket Processing for a Non-Logged In User
        else:
            Create_User_Order = Online_Orders(First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount)
            Create_User_Order.save()
            
            User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
            for Product in cart_products():
                Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
                if Product.On_Sale:
                    Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
                else:
                    Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
                for key, val in cart_quantities().items():
                    if int(key) == Product_ID:
                        val #Carted Product Quantities Number Value
                        #Based on finding all the information above, Create an Orderable Item DB Table
                        Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)      
                        Create_Orderable_Item.save()
                    
            #Delete the Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            messages.success(request, "TEST User LOG OUT Order Has Been Placed!")
            return redirect("HomePage")

    else:
        messages.success(request, "TEST Access Denied!")
        return redirect("HomePage")
    
def OnlineOrderSingle(request, PrimeKey):
    if request.user.is_superuser:
        SingleOrder = Online_Orders.objects.get(id=PrimeKey)
        SingleOrderedProducts = Orderable_Products.objects.filter(OrderID=PrimeKey)
        
        if request.POST: #As long as the web user hasn't filled out any forms
            ShippingStatus = request.POST['Shipping_Status'] #Get the POST value from the Shipping_Status Hidden Input Field
            
            if ShippingStatus == "true": #As long as the Ship Status field displays the value 'true'
                SingleOrder = Online_Orders.objects.filter(id=PrimeKey) #Grbbing the Shipped Single Order
                
                Right_Now_Date = datetime.datetime.now()
                
                SingleOrder.update(Shipment_Released=True, Shipment=Right_Now_Date, ) #Update that Single Order`s Shipping Status to TRUE
                messages.success(request, "Shipping Status changed to ORDER HAS SHIPPED")  
                return redirect("HomePage")
                
            else: #As long as the Ship Status field displays the value 'false'
                SingleOrder = Online_Orders.objects.filter(id=PrimeKey) #Grbbing the Shipped Single Order
                SingleOrder.update(Shipment_Released=False) #Update that Single Order`s Shipping Status to FALSE
                messages.success(request, "Shipping Status changed to ORDER AWAITING SHIPMENT")  
                return redirect("HomePage") 
            
        return render(request, "Order_Single_Page.html", {"Order": SingleOrder, "OrderItem": SingleOrderedProducts,})
    
    else:
        messages.success(request, "Access Denied!")
        return redirect("HomePage")
    
    
# def ShopCartBilling(request):
#     if request.POST:  #If the web user POSTED data over from the Forms on the CheckOut Page
#         cart = Cart(request)
#         cart_products = cart.view_cart
#         cart_quantities = cart.cart_amounts
#         cart_total_price = cart.total_price()
    
#         #Creating a User Session For The Order Processing Logic
#         Processing_Session = request.POST
#         request.session["Processing_Session"] = Processing_Session
        
#         Billing_Form = OnlineOrderPayments(request.POST or None)
        
#         First_Name = Processing_Session['Shipping_First_Name']
#         Last_Name = Processing_Session['Shipping_Last_Name']
#         Email = Processing_Session['Shipping_Email']
        
#         Ship_Address = f'''{Processing_Session['Shipping_Address_Line_1']}\n{Processing_Session['Shipping_Address_Line_2']}\n{Processing_Session['Shipping_City']}\n{Processing_Session['Shipping_State']}\n{Processing_Session['Shipping_ZipCode']}\n{Processing_Session['Shipping_Country']}\n'''
        
#         Total_Amount = cart_total_price
        
#         #Acquire the Host Url
#         Host = request.get_host()
        
#         InvoiceNUM = str(uuid.uuid4())
        
#         # Paypal Dictionary Key Value Pairs Below
#         # https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/Appx-websitestandard-htmlvariables/
#         PayPal_Hash_Map = {
#             "business": settings.PAYPAL_RECEIVER_EMAIL, #The merchant account reciving patment
#             "amount": cart_total_price,
#             "item_name": "Some Item Name(s)",
#             "invoice": InvoiceNUM,
#             "notify_url": f"http://{Host}{reverse('paypal-ipn')}",
#             "return":  f"http://{Host}{reverse('PayPalPaymentSuccess')}",
#             "cancel_return": f"http://{Host}{reverse('PayPalPaymentFail')}",
#             #"rm": 2,
#             # "Custom": "Premium_Plan",
#         }

#         PayPalForm = PayPalPaymentsForm(initial=PayPal_Hash_Map)
            
#         if request.user.is_authenticated: #If the web user is logged in
#             Billing_Form = OnlineOrderPayments()
#             user = request.user #Save the Web user to database
            
#             Create_User_Order = Online_Orders(user=user, First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount, Invoice=InvoiceNUM)
#             Create_User_Order.save()
            
#             User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
#             for Product in cart_products():
#                 Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
#                 if Product.On_Sale:
#                     Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
#                 else:
#                     Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
#                 for key, val in cart_quantities().items():
#                     if int(key) == Product_ID:
#                         val #Carted Product Quantities Number Value
#                         #Based on finding all the information above, Create an Orderable Item DB Table
#                         Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)    
#                         Create_Orderable_Item.save()
                    
#                 #Remove Cart from the Database
#                 LoggedInUser = WebsiteAccounts.objects.filter(Web_User__id=request.user.id)
#                 LoggedInUser.update(Old_Cart="") #Replace current Key, Val pair with Nothing 
                    
#                 return render(request, "Shopping_Cart_Billing_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "Billing_Form": Billing_Form, "PayPalForm": PayPalForm, "Shipping_Information": request.POST, })
        
#         else:
#             Billing_Form = OnlineOrderPayments()
            
#             Create_User_Order = Online_Orders(First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount, Invoice=InvoiceNUM)
#             Create_User_Order.save()
            
#             User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
#             for Product in cart_products():
#                 Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
#                 if Product.On_Sale:
#                     Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
#                 else:
#                     Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
#                 for key, val in cart_quantities().items():
#                     if int(key) == Product_ID:
#                         val #Carted Product Quantities Number Value
#                         #Based on finding all the information above, Create an Orderable Item DB Table
#                         Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)      
#                         Create_Orderable_Item.save()
                        
#                 return render(request, "Shopping_Cart_Billing_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "Billing_Form": Billing_Form, "PayPalForm": PayPalForm, "Shipping_Information": request.POST, })
    
#     else:
#         messages.success(request, "Access Denied!")
#         return redirect("HomePage")
        
def ShopCartBilling(request):
    if request.POST:  #If the web user POSTED data over from the Forms on the CheckOut Page
        cart = Cart(request)
        cart_products = cart.view_cart
        cart_quantities = cart.cart_amounts
        cart_total_price = cart.total_price()
    
        #Creating a User Session For The Order Processing Logic
        Processing_Session = request.POST
        request.session["Processing_Session"] = Processing_Session
        
        Billing_Form = OnlineOrderPayments(request.POST or None)
        
        First_Name = Processing_Session['Shipping_First_Name']
        Last_Name = Processing_Session['Shipping_Last_Name']
        Email = Processing_Session['Shipping_Email']
        
        Ship_Address = f'''{Processing_Session['Shipping_Address_Line_1']}\n{Processing_Session['Shipping_Address_Line_2']}\n{Processing_Session['Shipping_City']}\n{Processing_Session['Shipping_State']}\n{Processing_Session['Shipping_ZipCode']}\n{Processing_Session['Shipping_Country']}\n'''
        
        Total_Amount = cart_total_price
        
        #Acquire the Host Url
        Host = request.get_host()
        
        InvoiceNUM = str(uuid.uuid4())
        
        # Paypal Dictionary Key Value Pairs Below
        # https://developer.paypal.com/api/nvp-soap/paypal-payments-standard/integration-guide/Appx-websitestandard-htmlvariables/
        PayPal_Hash_Map = {
            "business": settings.PAYPAL_RECEIVER_EMAIL, #The merchant account reciving patment
            "amount": cart_total_price,
            "item_name": "Some Item Name(s)",
            "invoice": InvoiceNUM,
            "notify_url": f"http://{Host}{reverse('paypal-ipn')}",
            "return":  f"http://{Host}{reverse('PayPalPaymentSuccess')}",
            "cancel_return": f"http://{Host}{reverse('PayPalPaymentFail')}",
            #"rm": 2,
            # "Custom": "Premium_Plan",
        }

        PayPalForm = PayPalPaymentsForm(initial=PayPal_Hash_Map)
            
        # Online Order Ticket Processing for a Logged In User
        if request.user.is_authenticated: #If the web user is logged in
            user = request.user #Save the Web user to database
            Create_User_Order = Online_Orders(user=user, First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount, Invoice=InvoiceNUM)
            Create_User_Order.save()
            
            User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
            for Product in cart_products():
                Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
                if Product.On_Sale:
                    Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
                else:
                    Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
                for key, val in cart_quantities().items():
                    if int(key) == Product_ID:
                        val #Carted Product Quantities Number Value
                        #Based on finding all the information above, Create an Orderable Item DB Table
                        Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)    
                        Create_Orderable_Item.save()
                    
            #Delete the Cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                    
            #Remove Cart from the Database
            LoggedInUser = WebsiteAccounts.objects.filter(Web_User__id=request.user.id)
            LoggedInUser.update(Old_Cart="") #Replace current Key, Val pair with Nothing 
                    
            return render(request, "Shopping_Cart_Billing_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "Billing_Form": Billing_Form, "PayPalForm": PayPalForm, "Shipping_Information": request.POST, })
        
        # Online Order Ticket Processing for a Non-Logged In User
        else:
            Create_User_Order = Online_Orders(First_Name=First_Name, Last_Name=Last_Name, Email=Email, Full_Address=Ship_Address, Total_Amount=Total_Amount, Invoice=InvoiceNUM)
            Create_User_Order.save()
            
            User_Order_ID = Create_User_Order.pk #Grabbing the Generate User_Order DB ID#
            
            for Product in cart_products():
                Product_ID = Product.id #Secure the Product ID from the Carted Product(s)
                
                if Product.On_Sale:
                    Price = Product.On_Sale #Secure the Product Sale Price from the Carted Product(s)
                    
                else:
                    Price = Product.Price #Secure the Product Price from the Carted Product(s)
                    
                for key, val in cart_quantities().items():
                    if int(key) == Product_ID:
                        val #Carted Product Quantities Number Value
                        #Based on finding all the information above, Create an Orderable Item DB Table
                        Create_Orderable_Item = Orderable_Products(OrderID_id=User_Order_ID, Product_id=Product_ID, user_id=user.id, Quantity=val, Price=Price)      
                        Create_Orderable_Item.save()
                
                return render(request, "Shopping_Cart_Billing_Page.html", {"Cart_Summary": cart_products, "Cart_Amount" : cart_quantities, "Cart_Total_Price" : cart_total_price, "Billing_Form": Billing_Form, "PayPalForm": PayPalForm, "Shipping_Information": request.POST, })
    else:
        messages.success(request, "Access Denied!")
        return redirect("HomePage")

def Services_TechConsultation(request):
    Testimonials = CustomerTestimonials.objects.all()
    
    return render(request, "Services_Tech_Consultation_Page.html", {"Testi": Testimonials, })
    
def Services_Careers(request):
    Jobs = Employment.objects.all().order_by("Title")
    
    return render(request, "Services_Careers_Page.html", {
        "Jobs": Jobs
    })
    
def Services_Careers_Applying(request, Job_ID):
    Job = Employment.objects.get(pk=Job_ID)
    
    submitted = False
    if request.method == "POST":
        form = JobApplicatioNSubmissions(request.POST, request.FILES)
        if form.is_valid():
            Application = form.save(commit=False)
            Application.save()
            messages.success(request, f''' You Have Successfully Submitted Your Application for the Quansh Tech {Job.Title} Position! ''')
            return (redirect("Careers"))

        else:
            form = JobApplicatioNSubmissions
            if 'submitted' in request.GET:
                submitted = True
                
    form = JobApplicatioNSubmissions
    
    return render(request, "Services_Careers_User_Apply.html", 
                {
                "Job": Job,
                'Form': form, 
                'submitted': submitted,
                })

    
def Services_Laboratory(request):
    return render(request, "Services_Laboratory_Page.html", {
        
    })
    
def Services_TechSupport(request):
    FAQs = FAQ.objects.all()

    submitted = False
    if request.method == "POST":
        form = CustomerSubmissions(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('TechSupport?submitted=True')
        
    else:
        form = CustomerSubmissions
        if 'submitted' in request.GET:
            submitted = True
            
    form = CustomerSubmissions
    
    return render(request, "Services_Tech_Support_Page.html", {
        "FAQ" : FAQs,
        'Form': form,
        "submitted" : submitted
        
    })

def AdminDashECommerce(request):
    PromoCodes = CouponDiscount.objects.all()
    AllProducts = StoreProducts.objects.all()
    
    Paginate = Paginator(StoreProducts.objects.all().order_by('Brand'), 21)
    Page = request.GET.get("page")
    Products = Paginate.get_page(Page)

    Numbers = "h" * Products.paginator.num_pages
    
    return render(request, "Admin_Dashboard_ECommerce_Page.html", {"PaginatedProducts": Products, "Numbers": Numbers, "Promo": PromoCodes,"AllProducts": AllProducts, })
    
def AdminDashRetailStores(request):
    Stores = StoreLocations.objects.all()
    
    return render(request, "Admin_Dashboard_Retail_Stores_Page.html", {"Store": Stores,})
    
def AdminDashCustomerSupport(request):
    Customer_Support_Tickets = CustomerSupportTickets.objects.all()
    # Answered = CustomerSupportTickets.objects.get(Answered=True)
    # Pending = CustomerSupportTickets.objects.get(Answered=False)
    # Form = CSRUpdateForm(request.POST or None, all=Customer_Support_Tickets)
    
    # if Form.is_valid():
    #     Form.save()
    #     return redirect('AdminDashCustomerSupport')
    
    return render(request, "Admin_Dashboard_Customer_Support_Page.html", {
        "CSR": Customer_Support_Tickets,
        # "Answered": Answered,
        # "Pending": Pending,
        # "Status_Update": Form
    })
    
def AdminCustomerSupportUpdate(request, Ticket_ID):
    Customer_Support_Single_Ticket = CustomerSupportTickets.objects.get(pk=Ticket_ID)
    Form = CSRUpdateForm(request.POST or None, instance=Customer_Support_Single_Ticket)
    
    if Form.is_valid():
        Form.save()
        return redirect('AdminDashCustomerSupport')
    
    return render(request, "Admin_Update_Support_Ticket_Page.html", {
        "Single_CSR_Ticket": Customer_Support_Single_Ticket,
        "Support_Form": Form
    })

def AdminHumanResources(request):
    Jobs = Employment.objects.all()
    Human_Resources = JobApplications.objects.all()
    Staff_Members = CurrentEmployees.objects.all()
    
    return render(request, "Admin_Dashboard_HR_Page.html", {
        "HR" : Human_Resources,
        "Jobs" : Jobs,
        "Staff" : Staff_Members
    })
    
def AdminCustomerReviews(request):
    Reviews = CustomerReviews.objects.order_by('-ShoppingDate')
    
    return render(request, "Admin_Dashboard_Shopping_Reviews_List.html", {
        "Reviews" : Reviews
    })

def CustomerReviewFormPage(request):
    submitted = False
    if request.method == "POST":
        form = ShoppingReview(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('ReviewForm?submitted=True')
    else:
        form = ShoppingReview
        if 'submitted' in request.GET:
            submitted = True

    form = ShoppingReview
    Reviews = CustomerReviews.objects.all()
    
    return render(request, "Shopping_Review_Input_Page.html", 
                    {'form': form, 
                    'submitted': submitted,
                    'CustomerReviews': Reviews })
    
def ReportsPage(request):
    return render(request, "Admin_Website_Reports_Page.html", {})
    
def ProductText(response):
    # Initializing the response Variable for a .TXT file
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=EveryProduct.txt'
    
    Products = StoreProducts.objects.all()

    lines = []
    
    # Pulling the Data from Models file to append each part of data onto the empty array above
    for Product in Products:
        lines.append(f'{Product.Name}\n{Product.Price}\n{Product.Stock}\n{Product.Summary}\n{Product.Coupon}\n\n')

    # Writting the orgainzed data onto the lines array
    response.writelines(lines)
    return response


def ProductCSV(response):
    # Initializing the response Variable for a .CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=EveryProduct.csv'
    
    Products = StoreProducts.objects.all()

    # Creating a CSV Writer
    writer = csv.writer(response)
    
    # Instructing the Writer on what to write for each row
    writer.writerow(['Product Name', 'Selling Price', 'Total Stock', 'Product Summary', 'Image URL Link', 'Applicable Coupon'])

    # Pulling the Data from Models file to write each part in the writerow method
    for Product in Products:
        writer.writerow([Product.Name, Product.Price, Product.Stock, Product.Summary, Product.Coupon])
    return response
