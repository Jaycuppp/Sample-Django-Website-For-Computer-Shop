from .models import *
from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

# admin.site.unregister(Group)
# @admin.register(Group)
# class AnyName(ImportExportModelAdmin): == Starting Code For Mass Importing & Exporting the Data Models
#admin.site.register(Data_Model_Class_Name, Admin_Class_Name) == Ending Code For Mass Importing & Exporting the Data Models


# @admin.register(Pictures)
# class AdminPictures(admin.ModelAdmin):
class AdminPictures(ImportExportModelAdmin):
    DB_Fields = ('Name', 'Image', 'Custom_File')
    fields = DB_Fields
    list_display = ('Name',)
    search_fields = DB_Fields
    
# For Mass Importing & Exporting the Picture Data
admin.site.register(Pictures, AdminPictures)

# @admin.register(Customer)
# class AdminCustomer(admin.ModelAdmin):
class AdminCustomer(ImportExportModelAdmin):
    DB_Fields = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address', 'Username', 'Password')
    fields = DB_Fields
    list_display = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address',)
    search_fields = DB_Fields
    
admin.site.register(Customer, AdminCustomer)

# Register your models here.
class Admin_Customer_Shipping_To(ImportExportModelAdmin):
    DB_Fields = ('user', 'Shipping_First_Name', 'Shipping_Last_Name', 'Shipping_Email', 'Shipping_Address_Line_1', 'Shipping_Address_Line_2', 'Shipping_City', 'Shipping_State', 'Shipping_ZipCode', 'Shipping_Country')
    fields = DB_Fields
    list_filter = ('user',)
    list_display =  ('user',)
    ordering = ('user',)
    search_fields = DB_Fields

admin.site.register(Customer_Shipping, Admin_Customer_Shipping_To)


class Admin_Web_Profile(admin.StackedInline):
    model = WebsiteAccounts
    
class Admin_Web_User(admin.ModelAdmin):
    model = User
    inlines = [Admin_Web_Profile]
    
    DB_Fields = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined')
    
    fields = DB_Fields
    list_filter = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined',)
    list_display =  ('username', 'first_name', 'last_name', 'email',)
    ordering = ('username',)
    search_fields = DB_Fields
    
#Run this code to take down the current Admin Section of the Users DataSet
admin.site.unregister(User)

#Load Back up the newly created Admin Section of the Users Dataset
admin.site.register(User, Admin_Web_User)


# @admin.register(Category)
# class AdminCategory(admin.ModelAdmin):
class AdminCategory(ImportExportModelAdmin):
    DB_Fields = ('Name',)
    fields = DB_Fields
    list_display = ('Name',)
    search_fields = DB_Fields
    
# For Mass Importing & Exporting the Picture Data
admin.site.register(Category, AdminCategory)


# @admin.register(StoreProducts)
# class AdminProducts(admin.ModelAdmin):
class AdminProducts(ImportExportModelAdmin):
    DB_Fields = ('Name', 'Brand', "Category", "Price", "On_Sale", "Sale_Price", "SKU", "UPC", "Serial", "Stock", "Summary", "Key_Feat_1", "Key_Feat_2", "Key_Feat_3", "Key_Feat_4", "Key_Feat_5", "Key_Feat_6", "Key_Feat_7", "Key_Feat_8", "Key_Feat_9", "Key_Feat_10", "Picture", "Spec_Sheet", "Coupon", "Discontinued",)
    fields = DB_Fields
    list_filter = ('Brand', 'Name', 'Stock', 'Coupon',)
    list_display = ('Brand', 'Name', 'Summary', 'Key_Feat_1', 'Category')
    ordering = ('Name',)
    search_fields = DB_Fields

admin.site.register(StoreProducts, AdminProducts)


# @admin.register(StoreProducts)
# class AdminProducts(admin.ModelAdmin):
class AdminOrders(ImportExportModelAdmin):
    DB_Fields = ('Order_Number', 'Product', 'Customer', 'Quantity', 'Address', 'Email', 'Phone', 'Date', 'Status')
    fields = DB_Fields
    list_filter = ('Order_Number', 'Customer',)
    list_display = ('Order_Number', 'Product', 'Customer', 'Quantity', 'Address', 'Date', 'Status')
    ordering = ('Order_Number', 'Date')
    search_fields = DB_Fields

admin.site.register(Order, AdminOrders)


class Admin_Online_Orders_Products_Inline(admin.StackedInline):
    model = Orderable_Products
    extra = 0

# @admin.register(StoreProducts)
# class AdminProducts(admin.ModelAdmin):
class AdminOnlineOrders(ImportExportModelAdmin):
    DB_Fields = ('user', 'First_Name', 'Last_Name', 'Email', 'Full_Address', 'Total_Amount', 'Shipment_Released', 'Shipment', 'Invoice', 'Paid')
    inlines = [Admin_Online_Orders_Products_Inline] 
    
    fields = DB_Fields
    list_filter = ('user', 'Email', 'Shipment_Released', 'Shipment',)
    list_display = ('OnlineOrderNumber', 'Invoice', 'user', 'Email', 'Total_Amount', 'Paid', 'Shipment_Released', 'Shipment',)
    ordering = ('Shipment_Released',)
    search_fields = DB_Fields

admin.site.register(Online_Orders, AdminOnlineOrders)




class AdminOrderablerProducts(ImportExportModelAdmin):
    DB_Fields = ('OrderID', 'Product', 'user', 'Quantity', 'Price')
    
    fields = DB_Fields
    list_filter = ('user',)
    list_display = ('OrderID', 'user', 'Quantity', 'Product', 'Price')
    ordering = ('OrderID',)
    search_fields = DB_Fields

admin.site.register(Orderable_Products, AdminOrderablerProducts)


#     User = models.ForeignKey(User, on_delete=models.CASCADE)
#     Product = models.ForeignKey(StoreProducts, null=True, blank=False, on_delete=models.CASCADE)
#     Amount = models.IntegerField(default=0)
#     Added_To_Cart = models.DateTimeField(auto_now_add=True)
#     Payment_Date = models.DateTimeField(auto_now_add=True)
#     Payment_Status = models.CharField(max_length=255, blank=True)
    
# class AdminShoppingCarts(ImportExportModelAdmin):
#     fields = ('User', 'Products', 'Amount', 'Added_To_Cart', 'Payment_Date', 'Payment_Status')
#     list_filter = ('User',)
#     list_display = ('User', 'Amount', 'Added_To_Cart', 'Payment_Date', 'Payment_Status')
#     ordering = ('User',)
#     search_fields = ('User', 'Products',)
    
# admin.site.register(ShoppingCart, AdminShoppingCarts)

# class AdminPayPalPayments(ImportExportModelAdmin):
#     fields = ('User', 'Amount', 'Payment_Status',)
#     list_filter = ('User', 'Payment_Status',)
#     list_display = ('User', 'Amount', 'Payment_Status',)
#     ordering = ('User',)
#     search_fields = ('User','Payment_Status',)
    
# admin.site.register(PayPalPayment, AdminPayPalPayments)



# @admin.register(StoreLocations)
# class AdminLocations(admin.ModelAdmin):
class AdminLocations(ImportExportModelAdmin):
    DB_Fields = ('Street', 'City', 'State', 'Zip', 'Phone', 'Opens', 'Closes', 'Store_Image')
    fields = DB_Fields
    list_display = ('Street', 'City', 'State', 'Zip')
    ordering = ('Street', )
    search_fields = DB_Fields
    
admin.site.register(StoreLocations, AdminLocations)


# @admin.register(CouponDiscount)
# class AdminCouponDiscount(admin.ModelAdmin):
class AdminCouponDiscount(ImportExportModelAdmin):
    DB_Fields = ('CouponName', 'Discount', 'Description', 'StartDate', 'EndDate', 'Promo_Code_Image')
    fields = DB_Fields
    list_display = ('CouponName', 'Discount')
    ordering = ('CouponName', )
    search_fields = DB_Fields
    
admin.site.register(CouponDiscount, AdminCouponDiscount)


# @admin.register(CustomerReviews)
# class AdminCustomerReviews(admin.ModelAdmin):
class AdminCustomerReviews(ImportExportModelAdmin):
    DB_Fields = ('ShoppingDate', 'ReviewScore', 'TotalReview',)
    fields = DB_Fields
    list_display = ('ShoppingDate', 'ReviewScore')
    ordering = ('-ReviewScore', )
    search_fields = DB_Fields

admin.site.register(CustomerReviews, AdminCustomerReviews)
    
    
# @admin.register(FAQ)
# class AdminFAQ(admin.ModelAdmin):
class AdminFAQ(ImportExportModelAdmin):
    # resource_class = AdminFAQImports
    DB_Fields = ('Question_Type', 'Question', 'Answer')
    fields = DB_Fields
    list_display = ('Question_Type', 'Question', 'Answer',)
    search_fields = DB_Fields
    
admin.site.register(FAQ, AdminFAQ)
    
    
# @admin.register(CustomerSupportTickets)
# class AdminCustomerSupportTickets(admin.ModelAdmin):
class AdminCustomerSupportTickets(ImportExportModelAdmin):
    DB_Fields = ('Email', 'Inquiry', 'Answered', 'Submission_Time')
    fields = DB_Fields
    list_display = ('Email', 'Answered')
    ordering = ('Answered',)
    search_fields = DB_Fields
    
admin.site.register(CustomerSupportTickets, AdminCustomerSupportTickets)
    
    
# @admin.register(CustomerTestimonials)
# class AdminCustomerTestimonials(admin.ModelAdmin):
class AdminCustomerTestimonials(ImportExportModelAdmin):
    DB_Fields = ('First_Name', 'About', 'Testimonial')
    fields = DB_Fields
    list_display = ('About',)
    search_fields = DB_Fields
    
admin.site.register(CustomerTestimonials, AdminCustomerTestimonials)
    
    
# @admin.register(ReusableData)
# class AdminConstEmploymentData(admin.ModelAdmin):
class AdminKeyRespons(ImportExportModelAdmin):
    DB_Fields = ('Title', 'EEOS', 'First_Benefit', 'Second_Benefit', 'Third_Benefit')
    fields = DB_Fields
    list_display = ('Title',)
    search_fields = DB_Fields
    
admin.site.register(ReusableData, AdminKeyRespons)    

# @admin.register(Key_Respons)
# class AdminKeyRespons(admin.ModelAdmin):
class AdminKeyRespons(ImportExportModelAdmin):
    DB_Fields = ('Job', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth')
    fields = DB_Fields
    list_display = ('Job',)
    ordering = ('Job',)
    search_fields = DB_Fields

admin.site.register(Key_Respons, AdminKeyRespons)
    
# @admin.register(JobApplications)
# class AdminJobApplications(admin.ModelAdmin):
class AdminJobApplications(ImportExportModelAdmin):
    DB_Fields = ('First_Name', 'Last_Name', 'DesiredJob', 'Phone_Number', 'Email_Address', 'Resume', 'Cover_Letter', 'Submission')
    fields = DB_Fields
    list_display = ('First_Name', 'Last_Name', 'Email_Address',)
    ordering = ('First_Name',)
    search_fields = DB_Fields
    
admin.site.register(JobApplications, AdminJobApplications)
    
# @admin.register(Employment)
# class AdminEmployment(admin.ModelAdmin):
class AdminEmployment(ImportExportModelAdmin):
    DB_Fields = ('Title', 'Description', 'EEOS_And_Benefits', 'Key_Responsibilities', 'Salary', 'Location_Type', 'Store_Location', 'Filled')
    fields = DB_Fields
    list_display = ('Title', 'Filled', 'Location_Type', 'Store_Location')
    ordering = ('Filled',)
    search_fields = DB_Fields

admin.site.register(Employment, AdminEmployment)
    
    
# @admin.register(EmergencyContact)
# class AdminEmergencyContacts(admin.ModelAdmin):
class AdminEmergencyContacts(ImportExportModelAdmin):
    DB_Fields = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address')
    fields = DB_Fields
    list_display = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address')
    ordering = ('First_Name',)
    search_fields = DB_Fields

    
admin.site.register(EmergencyContact, AdminEmergencyContacts)

# @admin.register(CurrentEmployees)
# class AdminCurrentEmployees(admin.ModelAdmin):
class AdminCurrentEmployees(ImportExportModelAdmin):
    DB_Fields = ('First_Name', 'Last_Name', 'Job', 'Date_Of_Birth', 'Social_Security', 'Street_Address', 'City_Address', 'State_Address', 'W2_Tax_Information', 'Emergency_Contact', 'Employment_Contract')
    fields = DB_Fields
    list_display = ('First_Name', 'Last_Name', 'Job',)
    ordering = ('First_Name',)
    search_fields = DB_Fields
    
admin.site.register(CurrentEmployees, AdminCurrentEmployees)
