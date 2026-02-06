from .models import *

class Cart():
    def __init__(self, request):
        self.session = request.session # For any instance define the session variable
        
        self.request = request # Creating the request variable within this Cart Class
        
        cart = self.session.get('session_key') # Acquires the session key from a returning user with an account
        
        if 'session_key' not in request.session: # For Users without an account,
            cart = self.session['session_key'] = {} #Care will be 
            
        self.cart = cart # Creates a Shopping Cart for Every Instance shell 
        
    def __len__(self):
        return len(self.cart) #Counts And Returns All Of the Items On the Cart
        
    def add(self, product, quantity):
        product_id = str(product.id) # Get the Product ID and turns it into a string
        product_qty = str(quantity) # Get the Product Qty and turns it into a string
        
        if product_id in self.cart:  # Check to see if the Product is in the Cart instance
            pass
        
        else: # If product not in cart then return the product`s price as a String
            #self.cart[product_id] = {'Price': str(product.Price)}
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True # After cross checking the carted products then set the Session as a Modified Session
        
        if self.request.user.is_authenticated: #As long as there is a logged in user
            current_user = WebsiteAccounts.objects.filter(Web_User__id=self.request.user.id) #Getting the Logged In User`s Web Profile
            ShopCart = str(self.cart) # Converting the Saved Python Dict value of the Shop Cart into a JSON readible Key Value pair
            ShopCart = ShopCart.replace("\'", "\"")
            current_user.update(Old_Cart=str(ShopCart))
        
        
    def remove(self, product):
        
        self.session.modified = True
        
    def update(self, product, quantity):
        product_id = str(product) # Get the product_id and turns it into a string value
        product_qty = int(quantity) # Get the product_qty  and turn it into an integer value
        
        Currnet_Cart = self.cart #Call upon the current Usere Shopping Cart Session
        Currnet_Cart[product_id] = product_qty #Overwrite the current qty of the 1 carted product_id with the product_qty
        
        self.session.modified = True # After cross checking the carted products then set the Session as a Modified Session
        
        if self.request.user.is_authenticated: #As long as there is a logged in user
            current_user = WebsiteAccounts.objects.filter(Web_User__id=self.request.user.id) #Getting the Logged In User`s Web Profile
            ShopCart = str(self.cart) # Converting the Saved Python Dict value of the Shop Cart into a JSON readible Key Value pair
            ShopCart = ShopCart.replace("\'", "\"")
            current_user.update(Old_Cart=str(ShopCart))
        
        return self.cart
    
    def delete(self, product):
        product_id = str(product) # Get the product_id and turns it into a string value
        
        if product_id in self.cart: #As long as there is a product that is carted
            del self.cart[product_id] #Remove that product from the cart
            
        self.session.modified = True
        
        if self.request.user.is_authenticated: #As long as there is a logged in user
            current_user = WebsiteAccounts.objects.filter(Web_User__id=self.request.user.id) #Getting the Logged In User`s Web Profile
            ShopCart = str(self.cart) # Converting the Saved Python Dict value of the Shop Cart into a JSON readible Key Value pair
            ShopCart = ShopCart.replace("\'", "\"")
            current_user.update(Old_Cart=str(ShopCart))
        
    def view_cart(self):
        Product_IDs = self.cart.keys() # Acquire the Python Dictionay ID Keys from the "Carted" Items
        Products = StoreProducts.objects.filter(id__in=Product_IDs) # Query the database for only the Product IDs that have been carted
        return Products
        
    def cart_amounts(self):
        qunatities  = self.cart
        return qunatities 
    
    def total_price(self):
        Cart = self.cart #Cart will look like {str('ProductID'), int(Product Quantity)}
        Product_IDs = self.cart.keys() #Getting just the Carted Product IDs
        Products = StoreProducts.objects.filter(id__in=Product_IDs) # Query the database for only the Product IDs that have been carted
        Total = 0 #Starting the Count at $0
        
        for ProductKey, ProductQuant in Cart.items(): #Loop through each dictionary in the cart
            ProductKey= int(ProductKey) #Convert ProductKey Iteration Var into an Integer Value
            for product in Products: #Iterate through the Filtered StoreProducts Database
                if product.id == ProductKey: #As long as the Cart Product 
                    if product.On_Sale: #If a carted item is currently under a sale
                        Total = Total + (product.Sale_Price * ProductQuant) #Calculates The Total Price of Carted On Sale Priced Products
                    else:
                        Total = Total + (product.Price * ProductQuant) #Calculates The Total Price of Carted Regular Priced Products

        return Total
    
    def data_base_add(self, product, quantity):
        product_id = str(product) #Get the String Data Version of the product DB ID
        product_qty = str(quantity) #Get the String Data Version of the product Stock
    
        if product_id in self.cart: # Check to see if the Product is in the Cart instance
            pass
        else: # If product not in User`s Cookies Session Cart
            self.cart[product_id] = int(product_qty) #self.cart[product_id] = {'Price': str(product.Price)}
    
        self.session.modified = True # After cross checking the carted products then set the Session as a Modified Session
    
        if self.request.user.is_authenticated: #As long as there is a logged in user
            current_user = WebsiteAccounts.objects.filter(Web_User__id=self.request.user.id) #Getting the Logged In User`s Web Profile
            ShopCart = str(self.cart) # Converting the Saved Python Dict value of the Shop Cart into a JSON readible Key Value pair
            ShopCart = ShopCart.replace("\'", "\"")
            current_user.update(Old_Cart=str(ShopCart))