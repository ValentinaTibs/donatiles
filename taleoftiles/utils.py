import math  

COUNTRY_LIST = (
    ('it', 'Italia'),
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
    ('p', 'In Preparation'),
    ('s', 'Sent'),
    ('l', 'Lost'),
    ('r', 'Received'),
    ('c', 'Confermato'),
) 

ITEM_STATUS = (
    ('ok', 'Ok'),
    ('ns', 'Not Samplable'),
    ('le', 'Limit Exceeded'),
    ('ru', 'Removed by User'),
    ('rs', 'Removed by Staff'),
    ('o',  'Others')
) 

ech_weight = (150,300,550,650,1000)
#ech_price = (145,172,272,295,371)
ech_price = (72,81,100,114,125)
#ech_price = (72,144,264,312,480)

costo_m2_ship = 5

def sfrido(self):
    return 0.10

def compute_single_price(quantity,has_frido, sm_price, sm_per_box):
    return 0

def max_price(m2_price, m2_box, weight_box):
    # to_print = False
    # max_price =  ech_price[0]
    # weight_max_price = ech_weight[ech_price.index(max_price)]
    # num_box = weight_max_price / weight_box
    # tot_m2 = num_box * m2_box
    # max_price_sm = (max_price + max_price * IVA) / tot_m2
    # if to_print:
    #     print("num_box")
    #     print(num_box)        
    #     print("tot_m2")
    #     print(tot_m2)
    #     print("max_price_sm")
    #     print(max_price_sm)
    #     print("max_price_sm + m2_price")
    #     print(max_price_sm + m2_price)
    # return max_price_sm + m2_price
    return int(costo_m2_ship + m2_price)

def compute_num_boxes(quantity, has_frido, sm_price, sm_per_box, weight_box):
    to_print = False

    quantity = int(quantity)
    sm_price = float(sm_price)
    sm_per_box = float(sm_per_box)
    weight_box = float(weight_box)

    if has_frido == 'true':
        num_boxes = math.ceil((0.10 * quantity + quantity)/sm_per_box)
    else:
        num_boxes = math.ceil(quantity /  sm_per_box)
    
    if to_print:
        print("has_frido")
        print(has_frido)
        print("sm_price")
        print(sm_price)
        print("sm_per_box")
        print(sm_per_box)
        print("weight_box")
        print(weight_box)
        print("num_boxes")
        print(num_boxes)

    return num_boxes

def min_price(m2_price, m2_box, weight_box):
    # to_print = False
    # min_price =  ech_price[-1]
    # weight_min_price = ech_weight[ech_price.index(min_price)]
    # num_box = weight_min_price / weight_box
    # tot_m2 = num_box * m2_box
    # min_price_sm = (min_price + min_price * IVA) / tot_m2
    # if to_print:
    #     print("num_box")
    #     print(num_box)        
    #     print("tot_m2")
    #     print(tot_m2)
    #     print("min_price_sm")
    #     print(min_price_sm)
    #     print("min_price_sm + m2_price")
    #     print(min_price_sm + m2_price)
    # return min_price_sm + m2_price
    return int(costo_m2_ship + m2_price)



def compute_sm_price(quantity, has_frido, sm_price, sm_per_box,weight_box):

    # to_print = False
    # num_boxes = compute_num_boxes(quantity,has_frido, sm_price, sm_per_box,weight_box)
                
    # tot_price_shipping = 0
    # tot_quantity    = sm_per_box * num_boxes
    # residual_weight = weight_box * num_boxes
    # tot_weight      = weight_box * num_boxes
    # if to_print:
    #     print("tot_quantity")
    #     print(tot_quantity)
    #     print("residual_weight")
    #     print(residual_weight)
    #     print("tot_weight")
    #     print(tot_weight)
    # while residual_weight > 0 :
    #     min_val_weight = next((x for x in ech_weight if x > residual_weight), ech_weight[len(ech_weight)-1])
    #     idx_min = ech_weight.index(min_val_weight)
    #     tot_price_shipping += ech_price[idx_min]+ ech_price[idx_min]*IVA
    #     residual_weight -= ech_weight[idx_min]
    
    # return int(tot_price_shipping + (sm_price * tot_quantity))
    price = min_price(sm_price,0,0)
    qtyt = 0
    if has_frido == 'true':
        qtyt = float(quantity) + float(quantity) * 0.1
    else:
        qtyt = float(quantity)

    return math.ceil( qtyt * price ) 

# compute_sm_price(20,False,33.2,0.96,22.49)
# compute_sm_price(100,False,33.2,0.96,22.49)
# compute_sm_price(24,False,33.2,0.96,22.49) 
# compute_sm_price(69,False,33.2,0.96,22.49)
