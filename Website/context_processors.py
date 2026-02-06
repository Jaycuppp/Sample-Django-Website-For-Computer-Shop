from .cart import *

def cart(request):
    # Makes the Cart work for All Web Pages using a Context Processor
    return {'cart': Cart(request)}