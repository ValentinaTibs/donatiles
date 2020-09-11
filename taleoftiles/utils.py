import math  

COUNTRY_LIST = (
    ('it', 'Italia'),
    ('sv', 'Sverige'),
    ('dk', 'Danmark'),
    ('at', 'Österreich'),
    ('fr', 'France'),
    ('de', 'Deutscheland'),
    ('be', 'Belgique'),
    ('nl', 'Nederland'),
    ('lu', 'Lëtzebuerg'),
) 

COUNTRY_LIST_COMPLETED = (
    ('it', 'Italia','xxxxx',['07','08','09','90','91','92','93','94','95','96','97','98']),
    ('sv', 'Sverige','xxxxx',['80','81','82','83','84','85','86','87','88','89','70','71','72','73','74','75','76','77','78','79','90','91','92','93','94','95','96','97','98']),
    ('dk', 'Danmark','xxxx',[]),
    ('at', 'Österreich','xxxx',[]),
    ('fr', 'France','xxxxx',['20']),
    ('de', 'Deutscheland','xxxxx',[]),
    ('be', 'Belgique','xxxx',[]),
    ('nl', 'Nederland','xxxx',[]),
    ('lu', 'Lëtzebuerg','xxxx',[]),
) 
COMPLETION_STATUS = (
    ('s',   'Started'),
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

ech_weight = (150,300,550,650,1000)
ech_price = (145,172,272,295,371)
IVA = 0.22

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
    if has_frido:
        num_boxes = math.floor((0.10 * quantity + quantity)/sm_per_box)
    else:
        num_boxes = math.ceil(quantity /  sm_per_box)
    tot_price_shipping = 0
    tot_quantity    = sm_per_box * num_boxes
    residual_weight = weight_box * num_boxes
    tot_weight      = weight_box * num_boxes
    while residual_weight > 0 :
        min_val_weight = next((x for x in ech_weight if x > residual_weight), ech_weight[len(ech_weight)-1])
        idx_min = ech_weight.index(min_val_weight)
        tot_price_shipping += ech_price[idx_min]+ ech_price[idx_min]*IVA
        residual_weight -= ech_weight[idx_min]
    return int(tot_price_shipping + (sm_price * tot_quantity))


# compute_sm_price(20,False,33.2,0.96,22.49)
# compute_sm_price(100,False,33.2,0.96,22.49)
# compute_sm_price(24,False,33.2,0.96,22.49) 
# compute_sm_price(69,False,33.2,0.96,22.49)
