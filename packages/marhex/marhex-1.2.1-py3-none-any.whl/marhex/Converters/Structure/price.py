

def add_separators(price):

    valid_numbers = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'
    ]


    str_price = str(price)
    reversed_str_price = str_price[::-1]
    counter = 0
    len_price = len(str_price)
    reversed_str_price_new = ''
    for num in reversed_str_price:
        counter += 1
        remainder = counter%3
        if num in valid_numbers:
            if (counter != len_price) and (not remainder):
                reversed_str_price_new += num
                reversed_str_price_new += ','
            else:
                reversed_str_price_new += num
                
        else:
            raise ValueError('The entered [Price] must be entered in Persian or English numbers Without Separators.')
    final_price = reversed_str_price_new[::-1] 
    return final_price


def remove_separators(price):

    valid_numbers = [ ',',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'
    ]


    str_price = str(price)
    result = ''

    for num in str_price:
        if num in valid_numbers:
            if num != ',':
                result += num 
        else:
            raise ValueError('The entered [Price] must be entered in Persian or English numbers.')
    
    return result
    




