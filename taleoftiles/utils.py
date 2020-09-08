
COUNTRY_LIST = (
    ('it',   'Italia'),
    ('sv',	'Sverige'),
) 
#Italia - Svezia - Germania - Belgio - Olanda - Finlandia - Danimarca - Francia - Lussemburgo

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

ech_weight = (100,300,600,1000)
ech_price = (41,80,200,100)

def sfrido(self):
        return 0.10

def compute_single_price(quantity,has_frido, sm_price, sm_per_box):
    return 0

def max_price(m2_price, m2_box, weight_box):
    max_price = max(ech_price)
    weight_max_price = ech_weight[ech_price.index(max(ech_price))]
    num_box_max_price = weight_max_price / weight_box
    max_cost_box_shipp = max_price / num_box_max_price
    max_cost_m2_shipp = max_cost_box_shipp / m2_box 
    max_cost_m2 = max_cost_m2_shipp + m2_price
    return max_cost_m2

def min_price(m2_price, m2_box, weight_box):
    min_price = min(ech_price)
    weight_min_price = ech_weight[ech_price.index(min(ech_price))]
    num_box_min_price = weight_min_price / weight_box
    min_cost_box_shipp = min_price / num_box_min_price
    min_cost_m2_shipp = min_cost_box_shipp / m2_box 
    min_cost_m2 = min_cost_m2_shipp + m2_price
    return min_cost_m2

def compute_sm_price(quantity,has_frido, sm_price, sm_per_box,weight_box):
    tot_quantity = 0
    num_boxes = 0

    if has_frido:
        num_boxes = math.ceil(sfrido() * quantity + quantity)
    else:
        num_boxes = math.ceil(quantity)

    tot_quantity = sm_per_box * num_boxes
    
    return tot_quantity * max_price(sm_price, sm_per_box, weight_box)