from django import forms
from django.forms import ModelForm

# Connecting the models.py page with this forms.py page
from .models import *


from paypal.standard.forms import PayPalPaymentsForm

class ShoppingReview(ModelForm):
    class Meta:
        model = CustomerReviews
        fields = ('ShoppingDate', 'ReviewScore', 'TotalReview')
        labels = {
            'ShoppingDate': '',
            'ReviewScore': '',
            'TotalReview': '',
        }

        widgets = {
            'ShoppingDate': forms.DateInput(attrs={'class':'form-control', 'id': 'Shopping_Date', 'placeholder': 'What Month/Day/Year did you make a purchase?'}),
            'ReviewScore': forms.NumberInput(attrs={'class':'form-control', 'id': 'Review_Score', 'placeholder': 'Rate Shopping Experience Between 0 to 5'}),
            'TotalReview': forms.Textarea(attrs={'class':'form-control', 'id': 'Entire_Review', 'placeholder': '(Optional) Enter your shopping experience both the good and the bad'}),
        }

class ProductForm(ModelForm):
    class Meta:
        model = StoreProducts
        fields = ('Name', 'Brand', 'Price', 'Stock', 'Picture', 'Spec_Sheet', 'Discontinued', 'Summary', 'Key_Feat_1', 'Key_Feat_2', 'Key_Feat_3', 'Key_Feat_4',
                'Key_Feat_5', 'Key_Feat_6', 'Key_Feat_7', 'Key_Feat_8', 'Key_Feat_9', 'Key_Feat_10')

        labels = {
            'Name': '',
            'Brand': '',
            'Price': '',
            'Stock': '',
            'Picture': 'Upload Product Image Here',
            'Spec_Sheet': "(If Availabile) Upload Specification Sheet Here",
            'Discontinued': 'Mark if Product is Discontinued',
            'Summary': '',
            'Key_Feat_1': '',
            'Key_Feat_2': '',
            'Key_Feat_3': '',
            'Key_Feat_4': '',
            'Key_Feat_5': '',
            'Key_Feat_6': '',
            'Key_Feat_7': '',
            'Key_Feat_8': '',
            'Key_Feat_9': '',
            'Key_Feat_10': '',
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class':'form-control', 'id': 'Product_Form_Name', 'placeholder': 'Enter NEW Product Name'}),
            'Brand': forms.TextInput(attrs={"class":'form-control', 'id': 'Product_Form_Brand', 'placeholder': 'Enter NEW Product Brand'}),
            'Price': forms.NumberInput(attrs={'class':'form-control', 'id': 'Product_Form_Price', 'placeholder': 'Enter NEW Product Price'}),
            'Stock': forms.TextInput(attrs={'class':'form-control', 'id': 'Product_Form_Stock', 'placeholder': 'Enter CURRENT Stock Amount'}),
            'Summary': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Summary'}),
            'Key_Feat_1': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 1'}),
            'Key_Feat_2': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 2'}),
            'Key_Feat_3': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 3'}),
            'Key_Feat_4': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 4'}),
            'Key_Feat_5': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 5'}),
            'Key_Feat_6': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 6'}),
            'Key_Feat_7': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 7'}),
            'Key_Feat_8': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 8'}),
            'Key_Feat_9': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 9'}),
            'Key_Feat_10': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Key Feature 10'}),
            }
        
class Customer_Shipping_Form(forms.ModelForm):
    Shipping_First_Name = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "First Name"}), required=False)
    Shipping_Last_Name = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Last Name"}), required=False)
    Shipping_Email = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Email Address"}), required=False)
    Shipping_Address_Line_1 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Address 1"}), required=False)
    Shipping_Address_Line_2 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Address 2"}), required=False)
    Shipping_City = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "City"}), required=False)
    Shipping_State = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "State"}), required=False)
    Shipping_ZipCode = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Zipcode"}), required=False)
    Shipping_Country = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Country"}), required=False)

    class Meta:
        model = Customer_Shipping
        fields = ('Shipping_First_Name', 'Shipping_Last_Name', 'Shipping_Email', 'Shipping_Address_Line_1', 'Shipping_Address_Line_2', 'Shipping_City', 'Shipping_State', 'Shipping_ZipCode', 'Shipping_Country')
        exclude = ('user',)        


class OnlineOrderPayments(forms.Form):
    Card_Holder_First_Name = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "First Name of Card Holder"}), required=False)
    Card_Holder_Last_Name = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Lirst Name of Card Holder"}), required=False)
    Card_Number = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Card Number"}), required=False)
    Card_Expiration_Date = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'Card Expiration Date (mm/yy)'}), required=False)
    Card_CVV = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Card CVV Code"}), required=False)
    Card_Billing_Address1 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address Line 1"}), required=False)
    Card_Billing_Address2 = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address Line 2"}), required=False)
    Card_Billing_City = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address City"}), required=False)
    Card_Billing_State = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address State"}), required=False)
    Card_Billing_Zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address Zipcode"}), required=False) 
    Card_Billing_Country = forms.CharField(label="", widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': "Billing Address Country"}), required=False)


# class PayPalPayForm(PayPalPaymentsForm):
#     def HTML_Sunmit_Elemet(self):
#         return ''' <button type="submit"> Continue on PayPal website </button> '''

class LocationForm(ModelForm):
    class Meta:
        model = StoreLocations
        fields = ('Street', 'City', 'State', 'Zip', 'Phone', 'Opens', 'Closes', 'Store_Image')

        labels = {
            'Street': 'Street Address',
            'City': 'City',
            'State': 'State',
            'Zip': 'Zipcode',
            'Phone': 'Phone Number',
            'Opens': 'Opening Time',
            'Closes': 'Closing Time',
            'Store_Image': 'Picture of Store',
        }

        widgets = {
            'Street': forms.TextInput(attrs={'class':'form-control', 'id': 'Store_Street', 'placeholder': 'Enter Street'}),
            'City': forms.TextInput(attrs={'class':'form-control', 'id': 'Store_City', 'placeholder': 'Enter City'}),
            'State': forms.TextInput(attrs={'class':'form-control', 'id': 'Store_State', 'placeholder': 'Enter State'}),
            'Zip': forms.NumberInput(attrs={'class':'form-control', 'id': 'Store_Zip', 'placeholder': 'Enter Zip'}),
            'Phone': forms.TextInput(attrs={'class':'form-control', 'id': 'Store_Phone', 'placeholder': 'Enter Phone'}),
            'Opens': forms.TimeInput(attrs={'class':'form-control', 'id': 'Store_Opening_Time', 'placeholder': 'Enter Opening Time'}),
            'Closes': forms.TimeInput(attrs={'class':'form-control', 'id': 'Store_Closing_Time', 'placeholder': 'Enter Opening Time'}),
        }
        
class CustomerSubmissions(ModelForm):
    class Meta:
        model = CustomerSupportTickets
        fields = ('Email', 'Inquiry',)
        
        labels = {
            'Email': '',
            'Inquiry': '',
        }
        
        widgets = {
            'Email': forms.EmailInput(attrs={'class':'form-control', 'id':'EmailSubmission', 'placeholder': 'Enter Email'}),
            'Inquiry': forms.Textarea(attrs={'class':'form-control', 'id':'QuestionSubmission', 'placeholder': 'Enter Question(s)'}),
        }
        
class CSRUpdateForm(ModelForm):
    class Meta:
        model = CustomerSupportTickets
        fields = ('Answered',)
        
class JobApplicatioNSubmissions(ModelForm):
    class Meta:
        model = JobApplications
        fields = ('First_Name', 'Last_Name', 'DesiredJob', 'Phone_Number', 'Email_Address', 'Resume', 'Cover_Letter')
        
        labels = {
            'First_Name': '',
            'Last_Name': '',
            'DesiredJob': '',
            'Phone_Number': '',
            'Email_Address': '',
            'Resume': 'Upload Resume',
            'Cover_Letter': 'Upload Cover Letter',
        }
        
        widgets = {
            'First_Name': forms.TextInput(attrs={"class":"form-control", 'id':'First_Name_Submission', 'placeholder': 'Enter Your First Name'}), 
            'Last_Name': forms.TextInput(attrs={"class":"form-control", 'id':'Last_Name_Submission', 'placeholder': 'Enter Your Last Name'}), 
            'DesiredJob': forms.TextInput(attrs={"class":"form-control", 'id':'Desired_Job_Submission', 'placeholder': 'Enter the Position You Are Applying For (Copy Paste the Blue Text Above the Annual Salary)'}), 
            'Phone_Number': forms.TextInput(attrs={"class":"form-control", 'id':'Phone_Number_Submission', 'placeholder': 'Enter Your Phone Number'}), 
            'Email_Address': forms.EmailInput(attrs={"class":"form-control", 'id':'Email_Address_Submission', 'placeholder': 'Enter Your Email Address'}), 
            'Resume': forms.FileInput(attrs={"class":"form-control", 'id':'Resume_Submission' }), 
            'Cover_Letter': forms.FileInput(attrs={"class":"form-control", 'id':'Cover_Letter_Submission'}), 
        }