from Order import Order, FifoDeque

class Level(object):
    '''|
    | Represents a price level of the order book. Consists of 2 vectors of pointers to orders, i.e.,
    | visible orders (limit and icebergs) and hidden part of iceberg orders. Using 2 vectors allows for
    | easier management of the execution and the priority of iceberg orders. The time priority of the
    | orders is easily achieved by adding new orders at the end of the vector; and always read from the
    | beginning during the evaluation. The visible part of iceberg orders loose their priority after an
    | execution. Therefore they are moved to the back to the visible orders, just before the hidden
    | parts of all iceberg orders. This behavior is easily achieved by using separate vectors.
    |________'''    
    # TODO: level.price???
    def __init__(self):
        self.visible_orders = FifoDeque()
        self.icebergs       = FifoDeque()

    def isEmpty(self):
        return len(self.visible_orders) == 0 and len(self.icebergs) == 0


    def addOrder(self, anOrder):
        '''|
        | Adding an element at the end and reading from the beginning of the vector implements time priority.
        | Behaves like a FIFO queue, however, allows for random access and search of elements to be removed.
        |________'''
        if anOrder.isIceberg and (anOrder.quantity - anOrder.peakSize > 0): 
            iceberg = Order( anOrder.isBuy
                           , anOrder.orderId
                           , anOrder.price
                           , anOrder.quantity - anOrder.peakSize
                           , anOrder.peakSize
                           , isIceberg = True)
    
            # add at the end of the vector, read from the beginning -> implements time priority
            self.icebergs.append( iceberg )
            # Update the visible part of the order
            anOrder.quantity = anOrder.peakSize 
        
        self.visible_orders.append( anOrder )

                
    def removeVisible(self, anOrderId):
        for idx, order in enumerate(self.visible_orders):
            if order.orderId == anOrderId:
                del self.visible_orders[idx]
                return

    def removeIceberg(self, anOrderId):
        for idx, iceberg in enumerate(self.icebergs):
            if iceberg.orderId == anOrderId:
                del self.icebergs[idx]
                return

    def remove(self, anOrderId):
        self.removeVisible( anOrderId )
        self.removeIceberg( anOrderId )
        
    def show(self):
        '''|
        | Called as a result of command 's'.
        | First the visible orders are listed, then the invisible part of the iceberg orders.
        | Since the orders are added always at the back of the lists, the order with the
        | highest (time) priority is printed first.
        |________'''
        
        for order in self.visible_orders:
            order.show()

        for iceberg in self.icebergs:
            iceberg.show()
