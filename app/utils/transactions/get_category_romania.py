from app.utils.transactions.merchants_romania import ROMANIAN_MERCHANT_CATEGORIES


async def get_category_romanian(company: str, description: str, amount: str):
    """Ultra-fast Romanian merchant categorization"""
    
    # Combine company and description for analysis
    text = f"{company} {description}".lower().strip()
    
    # Check Romanian merchants first (fastest lookup)
    for merchant, category in ROMANIAN_MERCHANT_CATEGORIES.items():
        if merchant in text:
            return category
    
    # Romanian-specific patterns
    if any(word in text for word in ["srl", "sa", "pfa", "ii", "magazin"]):
        if any(word in text for word in ["alimentar", "market", "shop"]):
            return "Groceries"
        elif any(word in text for word in ["restaurant", "pizzerie", "crama"]):
            return "Restaurants"
        elif any(word in text for word in ["magazin", "boutique", "fashion"]):
            return "Shopping"
    
    # Amount-based categorization for Romanian context
    try:
        amount_val = float(amount) if amount else 0
        
        if amount_val > 0:
            if amount_val > 5000:  # Large income (RON)
                return "Salary"
            else:
                return "Income"
        else:
            amount_val = abs(amount_val)
            if amount_val > 2000:  # Rent in major Romanian cities
                return "Housing"
            elif amount_val > 500:
                return "Bills"
            elif amount_val > 100:
                return "Shopping"
            elif amount_val > 20:
                return "Food"
            else:
                return "Small Purchase"
    except:
        return "Unknown"
      
   