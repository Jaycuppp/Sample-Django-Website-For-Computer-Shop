from django import forms
from django.forms import ModelForm
from .models import CustomerReviews, JobApplications, StoreProducts, StoreLocations, CustomerSupportTickets

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
            'ShoppingDate': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'What Month/Day/Year did you make a purchase?'}),
            'ReviewScore': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Rate Shopping Experience Between 0 to 5'}),
            'TotalReview': forms.Textarea(attrs={'class':'form-control', 'placeholder': '(Optional) Enter your shopping experience both the good and the bad'}),
        }

class ProductForm(ModelForm):
    class Meta:
        model = StoreProducts
        fields = ('Name', 'Brand', 'Price', 'Stock', 'Picture', 'Discontinued', 'Description', )

        labels = {
            'Name': 'Product Name',
            'Brand': 'Product Brand',
            'Price': 'Regular Selling Price',
            'Stock': 'Current Stock Amount',
            'Picture': 'Upload Product Image Here',
            'Discontinued': 'Mark if Product is Discontinued',
            'Description': 'Full Product Description',
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class':'form-control', 'id': 'Product_Form_Name', 'placeholder': 'Enter NEW Product Name'}),
            'Brand': forms.TextInput(attrs={"class":'form-control', 'id': 'Product_Form_Brand', 'placeholder': 'Enter NEW Product Brand'}),
            'Price': forms.NumberInput(attrs={'class':'form-control', 'id': 'Product_Form_Price', 'placeholder': 'Enter NEW Product Price'}),
            'Stock': forms.TextInput(attrs={'class':'form-control', 'id': 'Product_Form_Stock', 'placeholder': 'Enter CURRENT Stock Amount'}),
            'Description': forms.Textarea(attrs={'class':'form-control', 'id': 'Product_Form_Description', 'placeholder': 'Enter NEW Product Description'}),
            }

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
        fields = ('Email', 'Inquiry')
        
        labels = {
            'Email': '',
            'Inquiry': ''
        }
        
        widgets = {
            'Email': forms.EmailInput(attrs={'class':'form-control', 'id':'EmailSubmission', 'placeholder': 'Enter Email'}),
            'Inquiry': forms.Textarea(attrs={'class':'form-control', 'id':'QuestionSubmission', 'placeholder': 'Enter Question(s)'}),
        }
        
class JobApplicatioNSubmissions(ModelForm):
    class Meta:
        model = JobApplications
        fields = ('First_Name', 'Last_Name', 'Phone_Number', 'Email_Address', 'Resume', 'Cover_Letter')
        
        labels = {
            'First_Name': '',
            'Last_Name': '',
            'Phone_Number': '',
            'Email_Address': '',
            'Resume': 'Upload Resume',
            'Cover_Letter': 'Upload Cover Letter',
        }
        
        widgets = {
            'First_Name': forms.TextInput(attrs={"class":"form-control", 'id':'First_NameSubmission', 'placeholder': 'Enter Your First Name'}), 
            'Last_Name': forms.TextInput(attrs={"class":"form-control", 'id':'Last_NameSubmission', 'placeholder': 'Enter Your Last Name'}), 
            'Phone_Number': forms.TextInput(attrs={"class":"form-control", 'id':'Phone_NumberSubmission', 'placeholder': 'Enter Your Phone Number'}), 
            'Email_Address': forms.EmailInput(attrs={"class":"form-control", 'id':'Email_AddressSubmission', 'placeholder': 'Enter Your Email Address'}), 
            'Resume': forms.FileInput(attrs={"class":"form-control", 'id':'ResumeSubmission' }), 
            'Cover_Letter': forms.FileInput(attrs={"class":"form-control", 'id':'Cover_LetterSubmission'}), 
        }