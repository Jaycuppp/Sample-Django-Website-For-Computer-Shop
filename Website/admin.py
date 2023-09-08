from click import Group
from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

#admin.site.unregister(Group)
@admin.register(StoreProducts)
class AdminProducts(admin.ModelAdmin):
    fields = ('Name', 'Brand', 'Price', 'UPC', 'SKU', 'Stock', 'Description', 'Picture', 'Coupon', 'Discontinued')
    list_filter = ('Brand', 'Name', 'Stock', 'Coupon',)
    list_display = ('Brand', 'Name', 'Price', 'Stock')
    ordering = ('Name',)
    search_fields = ('Name', 'Stock')

@admin.register(StoreLocations)
class AdminLocations(admin.ModelAdmin):
    fields = ('Street', 'City', 'State', 'Zip', 'Phone', 'Opens', 'Closes', 'Store_Image')
    list_display = ('Street', 'City', 'State', 'Zip')
    ordering = ('Street', )

@admin.register(CouponDiscount)
class AdminCouponDiscount(admin.ModelAdmin):
    fields = ('CouponName', 'Discount', 'Description', 'StartDate', 'EndDate', 'Promo_Code_Image')
    list_display = ('CouponName', 'Discount')
    ordering = ('CouponName', )

@admin.register(CustomerReviews)
class AdminCustomerReviews(admin.ModelAdmin):
    fields = ('ShoppingDate', 'ReviewScore', 'TotalReview',)
    list_display = ('ShoppingDate', 'ReviewScore')
    ordering = ('-ReviewScore', )
    
@admin.register(FAQ)
class AdminFAQ(admin.ModelAdmin):
    fields = ('Question', 'Answer')
    list_display = ('Question',)
    
@admin.register(CustomerSupportTickets)
class AdminCustomerSupportTickets(admin.ModelAdmin):
    fields = ('Email', 'Inquiry', 'Answered')
    list_display = ('Email', 'Answered')
    ordering = ('Answered',)
    
@admin.register(CustomerTestimonials)
class AdminCustomerTestimonials(admin.ModelAdmin):
    fields = ('First_Name', 'About', 'Testimonial')
    list_display = ('About',)
    
@admin.register(ReusableData)
class AdminConstEmploymentData(admin.ModelAdmin):
    fields = ('Title', 'EEOS', 'First_Benefit', 'Second_Benefit', 'Third_Benefit')
    list_display = ('Title',)
    
@admin.register(Key_Respons)
class AdminKeyRespons(admin.ModelAdmin):
    fields = ('Job', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eighth', 'Ninth', 'Tenth')
    list_display = ('Job',)
    ordering = ('Job',)
    
@admin.register(JobApplications)
class AdminJobApplications(admin.ModelAdmin):
    fields = ('First_Name', 'Last_Name', 'DesiredJob', 'Phone_Number', 'Email_Address', 'Resume', 'Cover_Letter')
    list_display = ('First_Name', 'Last_Name', 'Email_Address',)
    ordering = ('First_Name',)
    
@admin.register(Employment)
class AdminEmployment(admin.ModelAdmin):
    fields = ('Title', 'Description', 'EEOS_And_Benefits', 'Key_Responsibilities', 'Salary', 'Location_Type', 'Store_Location', 'Filled')
    list_display = ('Title', 'Filled', 'Location_Type', 'Store_Location')
    ordering = ('Filled',)
    
@admin.register(EmergencyContact)
class AdminEmergencyContacts(admin.ModelAdmin):
    fields = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address')
    list_display = ('First_Name', 'Phone_Number', 'Email_Address')
    ordering = ('First_Name',)
    
@admin.register(CurrentEmployees)
class AdminCurrentEmployees(admin.ModelAdmin):
    fields = ('First_Name', 'Last_Name', 'Job', 'Date_Of_Birth', 'Social_Security', 'Street_Address', 'City_Address', 'State_Address', 'W2_Tax_Information', 'Emergency_Contact', 'Employment_Contract')
    list_display = ('First_Name', 'Last_Name', 'Job',)
    ordering = ('First_Name',)

