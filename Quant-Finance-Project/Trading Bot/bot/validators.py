# Custom exception for input validation errors
class ValidationError(ValueError): 
    pass
        
def validate_side(side: str):
    capitalized_str = side.upper()
    valid_sides = ["BUY", "SELL"]
    
    if capitalized_str not in valid_sides:
        raise ValidationError(f"Side Type Out of Scope. Must be: {valid_sides}")
    
    return capitalized_str
    
def validate_order_type(order_type: str):
    capitalized_str = order_type.upper()
    valid_types = ["MARKET", "LIMIT", "STOP", "STOP_MARKET", "OCO"]
    
    if capitalized_str not in valid_types:
        raise ValidationError(f"Order Type Out of Scope. Must be: {valid_types}")
    
    return capitalized_str
    
def validate_quantity(quantity: str):
    try:
        order_quantity = float(quantity)
    except ValueError:
        raise ValidationError("Quantity must be a valid number.")
    
    if order_quantity <= 0:
        raise ValidationError("Invalid Quantity: Must be greater than 0.")
    
    return order_quantity

def validate_price(order_type: str, price: str = None):
    # Market orders don't need a limit price
    if order_type in ["MARKET", "STOP_MARKET"]:
        return None
        
    # Limit, Stop-Limit, and OCO orders DO need a limit price
    elif order_type in ["LIMIT", "STOP", "OCO"]:
        if price is None:
            raise ValidationError(f"For {order_type} Orders, Price cannot be None.")
        
        try:
            order_price = float(price)
        except ValueError:
            raise ValidationError("Price must be a valid number.")
            
        if order_price <= 0:
            raise ValidationError("Invalid Price: Must be greater than 0.")
            
        return order_price

def validate_stop_price(order_type: str, stop_price: str = None):
    # Only STOP and OCO orders use a stop price trigger
    if order_type not in ["STOP", "STOP_MARKET", "OCO"]:
        return None
        
    if stop_price is None:
        raise ValidationError(f"A stopPrice is required for {order_type} orders.")
    
    try:
        val = float(stop_price)
    except ValueError:
        raise ValidationError("Stop price must be a valid number.")
        
    if val <= 0:
        raise ValidationError("Invalid Stop Price: Must be greater than 0.")
        
    return val