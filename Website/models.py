import datetime, uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import CharField
from django_resized import ResizedImageField
from storages.backends.s3boto3 import S3Boto3Storage

from .api import *

# For Overloading the Preset Size of Images
def ImageResize(Height, Width):
    return 0


# class AWS_Images(S3Boto3Storage):
#     location = "Images/"
#     default_acl = "public-read"
#     file_overwrite = False
#     custom_domain = False

class Pictures(models.Model):
    Name = models.CharField("Name of the Image Being Used", max_length=255)
    # Image = models.ImageField("The Image", null=True, blank=True, upload_to='Images/') #storage=AWS_Images()
    Image = ResizedImageField("The Image", size=[400, 400], null=True, blank=True, upload_to='Images/') #storage=AWS_Images()
    Custom_File = models.FileField("Any File", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Digital Images"
    
    def __str__(self):
        return self.Name


class CouponDiscount(models.Model):
    CouponName = models.CharField("Coupon Code", max_length=69)
    Description = models.TextField("Coupon Description", null=True, blank=True, max_length=500)
    StartDate = models.DateTimeField("When The Coupon Begins", null=True, blank=True)
    EndDate = models.DateTimeField("When The Coupon Ends", null=True, blank=True)
    Discount = models.FloatField("Discount Amount", blank=True)
    Promo_Code_Image = models.ImageField("Promo Code Picture", null=True, blank=True, upload_to='Images/') #storage=AWS_Images()
    
    
    class Meta:
        verbose_name_plural = "Product Discount Coupon"

    def __str__(self):
        return self.CouponName
    
class Customer(models.Model):
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Phone_Number = models.CharField(max_length=20)
    Email_Address = models.EmailField(max_length=100)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Customer"
    
    def __str__(self):
        return f'''{self.First_Name} {self.Last_Name}'''
    
    
class Customer_Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Shipping_First_Name = models.CharField(max_length=255, null=True, blank=True)
    Shipping_Last_Name = models.CharField(max_length=255, null=True, blank=True)
    Shipping_Email = models.CharField(max_length=255, null=True, blank=True)
    Shipping_Address_Line_1 = models.CharField(max_length=255, null=True, blank=True)
    Shipping_Address_Line_2 = models.CharField(max_length=255, null=True, blank=True)
    Shipping_City = models.CharField(max_length=255, null=True, blank=True)
    Shipping_State = models.CharField(max_length=255, null=True, blank=True)
    Shipping_ZipCode = models.CharField(max_length=255, null=True, blank=True)
    Shipping_Country = models.CharField(max_length=255, null=True, blank=True)
    
    @property
    def Shipping_Full_Name(self):
        return f"{self.Shipping_First_Name} {self.Shipping_Last_Name}"
    
    class Meta:
        verbose_name_plural = "Customer Shipping"
        
    def __str__(self) -> str:
        return f"Customer`s Shipping Address, ID: {self.id}"

#Function for Creating a Default Customer Shipping DataSet when a new Web User Account is Created
def Creating_New_Customer_Shipping(sender, instance, created, **kwargs):
    if created:
        Cus_Shipping = Customer_Shipping(user=instance)
        Cus_Shipping.save()
    

class WebsiteAccounts(models.Model):
    Web_User = models.OneToOneField(User, on_delete=models.CASCADE)
    Modify_Date = models.DateTimeField(User, auto_now_add=True)
    Phone_Number = models.CharField("Account`s Phone Number", max_length=50, blank=True)
    Address1 = models.CharField("Account`s Address Line 1", max_length=50, blank=True)
    Address2 = models.CharField("Account`s Address Line 2", max_length=50, blank=True)
    City = models.CharField("Account`s Adress City", max_length=50, blank=True)
    State = models.CharField("Account`s Adress State", max_length=50, blank=True)
    ZipCode = models.CharField("Account`s Adress Zipcode", max_length=50, blank=True)
    Country = models.CharField("Account`s Adress Country", max_length=50, blank=True)
    Old_Cart = models.CharField("Old Shopping Cart Key Value Pair", max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = "Online Website Accounts"

    def __str__(self) -> str:
        return f''' {self.Web_User}'''
    
#Function for Creating a User Profile when a new Web User Account is Created
def Creating_New_Profile(sender, instance, created, **kwargs):
    if created:
        Web_User = WebsiteAccounts(Web_User=instance)
        Web_User.save()

# Helps automatically create a WebSiteAccount Profile Object once the Web Account is created
post_save.connect(Creating_New_Profile, sender=User)

class Category(models.Model):
    Name = models.CharField(max_length=255, default="")
    
    class Meta:
        verbose_name_plural = "Product Category"
    
    def __str__(self):
        return self.Name

class StoreProducts(models.Model):
    Name = models.CharField("Product Name", max_length=255)
    Brand = models.CharField("Product Brand", max_length=999, null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    Price = models.DecimalField("Selling Price", default=0, decimal_places=2, max_digits=14)
    On_Sale = models.BooleanField("Is product on Sale?", default=False)
    Sale_Price = models.DecimalField("On Sale Price", default=0, decimal_places=2, max_digits=14)
    SKU = models.CharField("Product SKU", max_length=255, null=True, blank=True)
    UPC = models.CharField("Product UPC", max_length=255, null=True, blank=True)
    Serial = models.CharField("Product Serial Number", max_length=50, blank=True, null=True)
    Stock = models.IntegerField("Product Stock", null=True, blank=True, default=0)
    Summary = models.TextField("Product Summary", max_length=1000, null=True, blank=True, default="")
    Key_Feat_1 = models.CharField("Key Prod Feat # 1", max_length=255, null=True, blank=True)
    Key_Feat_2 = models.CharField("Key Prod Feat # 2", max_length=255, null=True, blank=True)
    Key_Feat_3 = models.CharField("Key Prod Feat # 3", max_length=255, null=True, blank=True)
    Key_Feat_4 = models.CharField("Key Prod Feat # 4", max_length=255, null=True, blank=True)
    Key_Feat_5 = models.CharField("Key Prod Feat # 5", max_length=255, null=True, blank=True)
    Key_Feat_6 = models.CharField("Key Prod Feat # 6", max_length=255, null=True, blank=True)
    Key_Feat_7 = models.CharField("Key Prod Feat # 7", max_length=255, null=True, blank=True)
    Key_Feat_8 = models.CharField("Key Prod Feat # 8", max_length=255, null=True, blank=True)
    Key_Feat_9 = models.CharField("Key Prod Feat # 9", max_length=255, null=True, blank=True)
    Key_Feat_10 = models.CharField("Key Prod Feat # 10", max_length=255, null=True, blank=True)
    Picture = models.ImageField("Product Picture", null=True, blank=True, upload_to='Images/') #storage=AWS_Images()
    Spec_Sheet = models.ImageField("Specification Sheet", null=True, blank=True, upload_to='Images/')
    Coupon = models.ForeignKey(CouponDiscount, null=True, blank=True, on_delete=models.CASCADE)
    Discontinued = models.BooleanField("EOL Product", default=False)
    

    class Meta:
        verbose_name_plural = "Product"
    
    def __str__(self):
        return f"{self.Brand} {self.Name}"


# class ShoppingCart(models.Model):
#     User = models.ForeignKey(User, on_delete=models.CASCADE)
#     Product = models.ForeignKey(StoreProducts, null=True, blank=False, on_delete=models.CASCADE)
#     Amount = models.IntegerField(default=0)
#     Added_To_Cart = models.DateTimeField("Date of Product(s) added to Shop Cart", null=True, blank=True)  #auto_now_add=True
#     Payment_Date = models.DateTimeField("Payment Submission Date", null=True, blank=True) #auto_now_add=True
#     Payment_Status = models.CharField("Current Status of the Payment", max_length=255, blank=True)
#     Payment_Made = models.BooleanField("Has the Customer Made the Payment", default=False)
    
#     def __str__(self):
#         return f'''{self.User}`s Online Shopping Cart'''

class Order(models.Model):
    Order_Number = models.CharField("Unique Order Number", max_length=255, default=uuid.uuid4)
    Product = models.ForeignKey(StoreProducts, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    Address = models.CharField("Address to Ship the Order to", max_length=100, default="", blank=True, null=True)
    Email = models.EmailField("Order Reciever`s Contact Email Address", max_length=100, blank=True, null=True)
    Phone = models.CharField("Order Reciever`s Contact Phone Number", max_length=50, default="", blank=True, null=True)
    Date = models.DateField("Date of Placing the Order", default=datetime.datetime.today)
    Status = models.BooleanField("Has Order Been Shipped?", default=False)
    
    class Meta:
        verbose_name_plural = "Customer Orders"
    
    def __str__(self):
        return f"{self.Customer}`s Order with Order Number {self.Order_Number}"


class Online_Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    First_Name = models.CharField(max_length=255, null=True, blank=True)
    Last_Name = models.CharField(max_length=255, null=True, blank=True)
    Email = models.EmailField(max_length=255, null=True, blank=True)
    Full_Address = models.TextField(max_length=255, null=True, blank=True)
    Total_Amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    Shipment_Released = models.BooleanField("Has the Order Shipped?", default=False)
    Shipment = models.DateTimeField("Order Shipment Date", default=datetime.datetime.now())
    Invoice = models.CharField(max_length=255, null=True, blank=True)
    Paid = models.BooleanField("Has the Order Been Paid?", default=False)
    
    @property
    def Shipping_Full_Name(self):
        return f"{self.First_Name} {self.Last_Name}"
    
    @property
    def OnlineOrderNumber(self):
        return f"Online Order Number: {self.id}"
    
    class Meta:
        verbose_name_plural = "Online Customer Orders"
        
    def __str__(self) -> str:
        return f"Order ID:{self.id}"
    
@receiver(pre_save, sender=Online_Orders)
def OO_Shipment_Date_Update(sender, instance, **kwargs):
    if instance.pk:
        Present_Time_And_Date = datetime.datetime.now()
        Objectt = sender._default_manager.get(pk=instance.pk) #Acquiring the Sender Class Instance for the Online Orders Sender
        if instance.Shipment_Released and not Objectt.Shipment_Released: #As long as the current instance is marked as Shipped
            instance.Shipment = Present_Time_And_Date #Set the DateTime of whatever the Present Date & Time is 

    
class Orderable_Products(models.Model):
    OrderID = models.ForeignKey(Online_Orders, on_delete=models.CASCADE, null=True)
    Product = models.ForeignKey(StoreProducts, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.PositiveBigIntegerField(default=1)
    Price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Orderable Products"
    
    def __str__(self) -> str:
        return f"Order Product ID: {self.id}"
    
    
# class PayPalPayment(models.Model):
#     User = models.ForeignKey(User, on_delete=models.CASCADE)
#     Amount = models.IntegerField(default=ShoppingCart.Amount)
#     Payment_Date = models.DateTimeField(auto_now_add=True)
#     Payment_Status = models.CharField(max_length=255, blank=True)
    
#     def __str__(self):
#         f''' {User.username}'s Payment Status '''
    
    
class StoreLocations(models.Model):
    Street = models.CharField("Location Street Address", max_length=500)
    City = models.CharField("Location City", max_length=100)
    State = models.CharField("Location State", max_length=20)
    Zip = models.IntegerField("Location Zipcode Address")
    Phone = models.CharField("Location Phone Number", max_length=20)
    Opens = models.TimeField("When The Store Opens")
    Closes = models.TimeField("When The Store Closes")
    Store_Image = models.ImageField("Picture of the Computer Store", null=True, blank=True, upload_to='Images/') #storage=AWS_Images()    
    
    @property
    def City_State_Zip(self):
        return f"{self.City}, {self.State} {self.Zip}"
    
    @property
    def Full_Location(self):
        return f"{self.Street}, {self.City}, {self.State}, {self.Zip}"
    
    @property
    def City_Weather(self):
        return Location_Index_Page_API.Current_Weather_API(self.City, self.State)

    def __str__(self):
        return self.City + " Location"
    

class CustomerReviews(models.Model):
    ShoppingDate = models.DateField("Date Customer Shopped", auto_now=False, auto_now_add=False)
    ReviewScore = models.FloatField("Total Score out of 5")
    TotalReview = models.TextField("Customer Review", blank=True)
    
    # Data Field for Days Past from the Date of the Customer Review
    @property
    def DaysPast(self):
        Days_That_Have_Past = self.ShoppingDate - date.today()
        Str_Date = str(Days_That_Have_Past).split(".", 1)[0]
        return Str_Date

    def __str__(self):
        return f"Review # {self.pk}"
    
    
class CustomerTestimonials(models.Model):
    About = models.CharField("What the Testimonial is for", max_length=255)
    First_Name = models.CharField("First Name", blank=True, max_length=255)
    Testimonial = models.TextField("The Entire Testimonial", blank=True)
    
    def __str__(self):
        return f"{self.About} #{self.pk}"
    
    
class CustomerSupportTickets(models.Model):
    Email = models.EmailField("Customer Email")
    Inquiry = models.TextField("Customer Technical Question(s)", blank=True)
    Answered = models.BooleanField("Has Support Ticket Been Answered", default=False)
    Submission = models.DateTimeField(default=datetime.datetime.now())
    
    # @property
    # def TimeOfSubmission(self):
    #     DT = datetime.now()
    #     Hour0 = DT.hour 
    #     Minute = DT.minute
    #     Second = DT.second
        
    #     if Hour0 > 12:
    #         Hour1 = Hour0 - 12
    #         AM_PM = "PM"
    #     elif Hour0 < 12:
    #         Hour1 = Hour0
    #         AM_PM = "AM"
    #     else:
    #         Hour1 = Hour0
    #         AM_PM = "PM"
            
    #     ActualTimeOfSubmission = f"{Hour1}:{Minute}:{Second} {AM_PM}"
        
    #     return ActualTimeOfSubmission
    
    def __str__(self):
        return f"{self.Email}'s Support Ticket"
    
    
class FAQ(models.Model):
    Question_Type = models.TextField("The Category this FAQ Tech Question Falls Under", blank=True, max_length=255)
    Question = models.TextField("Technical Question")
    Answer = models.TextField("Technical Answer to the Technical Question", blank=True)
    
    def __str__(self):
        return "Frequently Asked Question And Answer"
    
    
class ReusableData(models.Model):
    Title = models.CharField("Purpose of Data", max_length=255, blank=True, null=True)
    EEOS = models.TextField("Equal Employment Opportunity Statement", blank=True, null=True)
    First_Benefit = models.TextField("Job Benefits # 1", blank=True, null=True)
    Second_Benefit = models.TextField("Job Benefits # 2", blank=True, null=True)
    Third_Benefit = models.TextField("Job Benefits # 3", blank=True, null=True)
    
    def __str__(self):
        return self.Title
    

class Key_Respons(models.Model):
    Job = models.CharField("The Job This is For", max_length=255, null=True, blank=True)
    First = models.TextField("1st Key Responsibility", max_length=255, null=True, blank=True)
    Second = models.TextField("2nd Key Responsibility", max_length=255, null=True, blank=True)
    Third = models.TextField("3rd Key Responsibility", max_length=255, null=True, blank=True)
    Fourth = models.TextField("4th Key Responsibility", max_length=255, null=True, blank=True)
    Fifth = models.TextField("5th Key Responsibility", max_length=255, null=True, blank=True)
    Sixth = models.TextField("6th Key Responsibility", max_length=255, null=True, blank=True)
    Seventh = models.TextField("7th Key Responsibility", max_length=255, null=True, blank=True)
    Eighth = models.TextField("8th Key Responsibility", max_length=255, null=True, blank=True)
    Ninth = models.TextField("9th Key Responsibility", max_length=255, null=True, blank=True)
    Tenth = models.TextField("10th Key Responsibility", max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Quansh Tech {self.Job}"
    
    
class Employment(models.Model):
    Title = models.CharField("Job Title", max_length=255)
    Description = models.TextField("Full Job Description", blank=True, null=True)
    Key_Responsibilities = models.ForeignKey(Key_Respons, null=True, blank=True, on_delete=models.CASCADE)
    Salary = models.CharField("Annual Salary For Job", max_length=255,  blank=True, null=True)
    Location_Type = models.CharField("Remote, Hybrid, or On-Site", max_length=255, blank=True, null=True)
    Store_Location = models.ForeignKey(StoreLocations, null=True, blank=True, on_delete=models.CASCADE)
    EEOS_And_Benefits = models.ForeignKey(ReusableData, null=True, blank=True, on_delete=models.CASCADE)
    Filled = models.BooleanField("Has This Position Been Filled?", default=False)
    
    def __str__(self):
        return f"Quansh Tech {self.Title}"
    
    
class EmergencyContact(models.Model):
    First_Name = models.CharField("First Name of Emergency Contact", max_length=255)
    Last_Name = models.CharField("Last Name of Emergency Contact", blank=True, max_length=255)
    Phone_Number = models.CharField("Phone Number of Emergency Contact", max_length=255)
    Email_Address = models.EmailField("Email Address of Emergency Contact")
    
    def __str__(self):
        return f"{self.First_Name} {self.Last_Name}"
    
    
class CurrentEmployees(models.Model):
    First_Name = models.CharField("First Name of Employee", blank=True, max_length=255)
    Last_Name = models.CharField("Last Name of Employee", blank=True, max_length=255)
    Job = models.ForeignKey(Employment, null=True, blank=True, on_delete=models.CASCADE)
    Date_Of_Birth = models.DateField("Employee's Birthday", blank=True)
    Social_Security = models.CharField("Social Security Number", blank=True, max_length=255)
    Street_Address = models.CharField("Street Address of Employee", blank=True, max_length=255)
    City_Address = models.CharField("City Address of Employee", blank=True, max_length=255)
    State_Address = models.CharField("State Address of Employee", blank=True, max_length=255)
    Zipcode_Address = models.CharField("Zipcode Address of Employee", blank=True, max_length=255)
    W2_Tax_Information = models.FileField("Employee's W2 Form", blank=True)
    Emergency_Contact = models.ForeignKey(EmergencyContact, null=True, blank=True, on_delete=models.CASCADE)
    Employment_Contract = models.FileField("Current Work Contract for Employee", blank=True)
        
    def __str__(self):
        return f"{self.First_Name} ({self.Job})"
    
    
class JobApplications(models.Model):
    First_Name = models.CharField("Applicant's First Name", max_length=255)
    Last_Name = models.CharField("Applicant's Last Name", max_length=255)
    DesiredJob = models.CharField("Applicant's Desired Job", max_length=255)
    Phone_Number = models.CharField("Applicant's Phone Number", max_length=255)
    Email_Address = models.EmailField("Applicant's Email Address", max_length=255)
    Resume = models.FileField("Applicant's Resume", blank=True)
    Cover_Letter = models.FileField("Applicant's Cover Letter", blank=True)
    Submission = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return f"{self.First_Name}'s Job Application"
    
# class OnlineCustomers(models.Model):
#     First_Name = models.CharField("First Name", max_length=255)
#     Last_Name = models.CharField("Last Name", blank=True, max_length=255)
#     Email = models.EmailField("Online Customers Email", max_length=255)
#     Phone_Number = models.CharField("Customer's Phone Number", blank=True)
#     Birthday = models.DateField("Customer's Birthday", blank=True)