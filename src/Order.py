import collections

class FifoDeque(collections.deque):
    '''|
    | collections.deque, a double-ended queue type that also ensures O(1) performance when 
    | used as a FIFO (using its append and popleft methods)
    |________'''
    pop = collections.deque.popleft

#-----------------------------------------------------------------------------------------------

class Order(object):
    '''|
    | Used to represent an active order in the book. Its data fields capture the information parsed from the input.
    | The same class is used for limit and iceberg orders. Therefore, there are 2 additional variables used, i.e.,
    | isIceberg denotes an iceberg order and reloadPeakSize is a variable used to keep the value of the visible part
    | (and to reload it after an execution) of an iceberg order. In case of iceberg orders, peakSize is used to keep track
    | on the remaining quantity of the order, which is visualized when printing the book state (the same as the limit orders).
    |________'''
    def __init__(self, isBuy, orderId, price, quantity, peakSize, isIceberg = None):
        self.isBuy          = isBuy                # True for buy orders
        self.isIceberg      = peakSize < quantity if isIceberg == None else isIceberg
        self.orderId        = orderId              # Unique number identifying an order
        self.price          = price                # Unsigned integer representing scaled decimal (with maximum 6 d.p. and not exceeding 10000.0)
        self.quantity       = quantity             # Total quantity
        self.peakSize       = peakSize             # Visible quantity


    def show(self):
        '''|
        | Used when visualizing the Book state (command s)
        |________'''
        bstr = 'B' if self.isBuy else 'S' # Ask/Bid
        istr = '*' if self.isIceberg else ''
        # TODO: price/price_scale; some allignment...
        print bstr, self.price, self.orderId, self.quantity, istr
#        print bstr, self.price, self.orderId, self.peakSize, self.quantity, istr
