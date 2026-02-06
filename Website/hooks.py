from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from django.apps import AppConfig
from django.dispatch import receiver
from django.conf import settings

import time

from .models import *

#Paypal IPN and PDT Variables
#https://developer.paypal.com/api/nvp-soap/ipn/IPNandPDTVariables/

@receiver(valid_ipn_received)
def PayPalPaymentReciev(sender, **kwargs):
    # Implement a 3 Second Pause on Grabbing the IPN Information
    time.sleep(10)

    #Collect the PayPal IPN Information
    PayPalObject = sender

    #Collect the Generated Invoice Number
    MyInvoice = str(PayPalObject.invoice)

    # Exact Match the Paypal Invoice Num with the RANDOM Order Invoice Num
    OnlineOrder = Online_Orders.objects.get(Invoice=MyInvoice)
    
    
    if PayPalObject.payment_status == "Completed":
        # Set the PAID Status to True for the Online Order
        OnlineOrder.Paid = True
        # Now Save the PAID status of the Order
        OnlineOrder.save()
        
    else:
        OnlineOrder.Paid = False
        OnlineOrder.save()
        
    #print(PayPalObject)
    #print(f"Amount Paid: ${PayPalObject.mc_gross}")