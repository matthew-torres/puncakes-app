from db import db

def consolidate_cart(cart):
    '''
    Consolidate indentical items into one cart entry
    Params:
        cart: list of dictionaries
    Returns:
        result: consolidated list of dictionaries
    '''
    result = []
    for d in cart:
        found = False
        for i in range(len(result)):
            if result[i]['id'] == d['id']:
                result[i]['quantity'] += d['quantity']
                found = True
                break
        if not found:
            result.append(d)
    return result

def update_order_status(orders):
    for order in orders:
        db.update_order_status(order['oid'])
    return True
