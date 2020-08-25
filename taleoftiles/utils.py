
COUNTRY_LIST = (
    ('it',   'Italia'),
    ('sv',	'Svezia'),

) 

COMPLETION_STATUS = (
    ('s',   'Started'),
    ('i1',  'In Checkout 1'),
    ('i2',  'In Checkout 2'),
    ('c',   'Completed'),
    ('p',   'Payed'),
    ('ex',  'Expired'),
    ('cs',  'Closed by Staff'),
) 

ORDER_STATUS = (
    ('w', 'In Wait'),
    ('i', 'Received'),
    ('p', 'In Preparazione'),
    ('s', 'Spedito'),
    ('l', 'Lost'),
    ('r', 'Ricevuto'),
    ('c', 'Confermato'),
) 

ITEM_STATUS = (
    ('ok', 'ok'),
    ('ns', 'Not Samplable'),
    ('le', 'Limit Exceeded'),
    ('ru', 'Removed by User'),
    ('rs', 'Removed by Staff'),
    ('o', 'Others')
) 

def sfrido(self):
        return 0.10

def compute_price(quantity,has_frido, sm_price):
    tot_quantity = 0
    if has_frido:
        tot_quantity = math.ceil(sfrido() * quantity + quantity)
    else:
        tot_quantity = quantity

    return tot_quantity * sm_price
