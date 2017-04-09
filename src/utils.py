from Order import Order
from Book  import Book

BID = 1
ASK = 0

def createOrders():
    o  = Order(BID,  999, 123.45,  100, 100)
    o1 = Order(ASK, 9191,  32.54, 1000, 100) # iceberg
    return o, o1

    
def checkOrder(order, isBuy, isIceberg, orderId, price, quantity, peakSize, reloadPeakSize):
    assert order.isBuy          == isBuy,              "Wrong isBuy value"
    assert order.isIceberg      == isIceberg,          "Wrong isIceberg value"
    assert order.orderId        == orderId,            "Wrong orderId value"
    assert order.price          == price,              "Wrong price value" 
    assert order.quantity       == quantity,           "Wrong quantity value"
    assert order.peakSize       == peakSize,           "Wrong peakSize value"

    
def checkOrders( order_1, order_2 ):
    assert order_1.isBuy        == order_2.isBuy,      "Wrong isBuy value"
    assert order_1.isIceberg    == order_2.isIceberg,  "Wrong isIceberg value"
    assert order_1.orderId      == order_2.orderId,    "Wrong orderId value"
    assert order_1.price        == order_2.price,      "Wrong price value" 
    assert order_1.quantity     == order_2.quantity,   "Wrong quantity value"
    assert order_1.peakSize     == order_2.peakSize,   "Wrong peakSize value"

    
def checkLevels( level_1, level_2 ):
    assert len(level_1.visible_orders) == len(level_2.visible_orders), "Wrong Level len (visible orders)!"
    for order_1, order_2 in zip(level_1.visible_orders, level_2.visible_orders):
        checkOrders( order_1, order_2 )
    
    assert len(level_1.icebergs) == len(level_2.icebergs), "Wrong Level len (icebergs orders)!"
    for order_1, order_2 in zip(level_1.icebergs, level_2.icebergs):
        checkOrders( order_1, order_2 )


def checkSides( side_1, side_2):
    assert len(side_1) == len(side_2), "Wrong number of levels in the side!"

    for (price_1, level_1), (price_2, level_2) in zip(side_1.iteritems(), side_2.iteritems()):
        assert price_1 == price_2,      "Wrong Level price"        
        checkLevels( level_1, level_2 )
                
    
def checkBooks( book_1, book_2 ):
    checkSides( book_1.bid, book_2.bid )
    checkSides( book_1.ask, book_2.ask )


def createBook():
    bo, ao = createOrders()
    b = Book()

    b.addOrder( order=bo )
    b.addOrder( order=ao )

    b.addOrder(BID, 199, 54.12, 1000, 100) # iceberg
    b.addOrder(BID, 111, 54.12,  100, 100)
    
    b.addOrder(ASK, 191,  45.23,  100, 100)
    b.addOrder(ASK, 777,  32.54,  100, 100)
    b.addOrder(ASK, 991,  22.21,  100, 100)
    b.addOrder(ASK, 181, 222.22,  200, 100) # iceberg
    b.addOrder(ASK, 888,  32.54,  100, 100)
    b.addOrder(ASK,  33,  25.18,  100, 100)
    b.addOrder(ASK, 111,  25.18,  100, 100)

    return b
