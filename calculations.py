from decimal import Decimal, ROUND_HALF_UP

# Alias for brevity and readability
Q = Decimal  

def _to_decimal(x) -> Q:
    """Safely converts input to Decimal to ensure financial precision."""
    if isinstance(x, Decimal):
        return x
    return Q(str(x))

def calculate_unit_amount(uf_units, uf_value) -> Q:
    """Calculates the unit amount based on Fixed Units (UF) and its current value."""
    uf_units = _to_decimal(uf_units)
    uf_value = _to_decimal(uf_value)
    
    if uf_units < 0 or uf_value < 0:
        raise ValueError("UF units and UF value must be non-negative")
    
    # Using ROUND_HALF_UP for standard commercial/financial rounding
    return (uf_units * uf_value).quantize(Q("0.01"), rounding=ROUND_HALF_UP)

def calculate_subtotal(unit_amount, quantity) -> Q:
    """Calculates the subtotal for a specific item quantity."""
    unit_amount = _to_decimal(unit_amount)
    quantity = _to_decimal(quantity)
    
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    
    return (unit_amount * quantity).quantize(Q("0.01"), rounding=ROUND_HALF_UP)

def calculate_total(subtotals, index) -> Q:
    """Calculates the final total applying a dynamic index/multiplier."""
    index = _to_decimal(index)
    
    if index <= 0:
        raise ValueError("The index must be greater than 0")
    
    # Ensures all subtotals are Decimals before summing
    total_sum = sum((_to_decimal(s) for s in subtotals), Q("0"))
    
    return (total_sum * index).quantize(Q("0.01"), rounding=ROUND_HALF_UP)