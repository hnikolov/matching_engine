from Order            import Order
from Level            import Level
from sortedcontainers import SortedDict
from operator         import neg

class Book(object):
    '''| TODO
    | Keep track of the active orders. It is constructed by using unordered_map, map, and vector data-structures.
    | Unordered map is used to keep pointers to all active orders. In this implementation, it is used to check whether an order already
    | exists in the book. Sorted maps are used to represent the bid and ask depths of the book using the price as a key. For efficiency,
    | the price is represented as (scaled) uint64_t. The insert operation inserts the element at the correct place implementing the
    | price priority in the book. Each element of the maps is a price level (see Level.hpp). Note that the best bid is the last element, i.e.,
    | the last price level, of the bid map; best ask is the first element (price level) of the ask map.
    |________''' 

    def __init__(self):
        self.bid = SortedDict( neg ) # Key is price as int, value is Level (in descending order)
        self.ask = SortedDict()      # Key is price as int, value is Level
       
        # Uniqueness of the keys is guaranteed only for active orders, i.e., if an order is removed, another order with the same key can be added 
        self.activeOrders = {} # Unordered map of active orders; Key is order Id, value is Order. Used for quick search of orders. 
        # Otherwise, we need to iterate over the levels (bid and ask) and to check the orders for the orderId in question
        
    def isBidEmpty( self ):
        return len(self.bid) == 0
        
    def isAskEmpty( self ):
        return len(self.ask) == 0
        
    def isEmpty( self ):
        return len(self.activeOrders) == 0
        
    def isPresent(self, anOrderId):
        return anOrderId in self.activeOrders
        
            
    def addOrder(self, isBuy=None, orderId=None, price=None, qty=None, peakSize=None, order=None):
        '''| TODO 
        | Creates and adds an order to the map of orders. In addition, pointer to the order is added to the proper map (bid/ask) and
        | vector (price level). The maps are ordered, therefore, inserting elements with price as keys, automatically builds a correct
        | depth of the book.
        | Note: best bid is the last element (price level) of the bid map; best ask is the first element (price level) of the ask map.
        |________''' 
        
        # Already checked that an order with the same Id is not present in the book
        myOrder = Order(isBuy, orderId, price, qty, peakSize) if order == None else order
        
        self.activeOrders[ myOrder.orderId ] = myOrder
        
        # TODO: Where do we deal with int*100 price as keys?
        key_price = int(myOrder.price*100)
        
        level = self.bid if myOrder.isBuy else self.ask
        
        if key_price not in level:
            level[ key_price ] = Level()

        level[ key_price ].addOrder( myOrder )
                    
    
    def removeOrder(self, orderId):
        '''| TODO 
        | Removes an active order from the book if present (return false if order not found).
        | In case of icebergs, removes both the visible and hidden parts.
        |________'''
        if orderId in self.activeOrders:
            isBuy     = self.activeOrders[orderId].isBuy
            key_price = int(self.activeOrders[orderId].price*100)
            
            level = self.bid if isBuy else self.ask
            level[ key_price ].remove( orderId )
                            
            del self.activeOrders[ orderId ] 
            return True
            
        return False

    def removeActiveOrder(self, orderId):
        '''| TODO 
        |________'''
        if orderId in self.activeOrders:                            
            del self.activeOrders[ orderId ] 
            return True
            
        return False


    def removeEmptyLevels(self):
        '''| TODO 
        | If an incoming order executes and matches with all active orders of the best level
        | including visible and invisible part of the orders, the level is considered empty
        | and the matching continues with the next price level. After the execution, before
        | adding an order and processing a new incoming order, this function is used to remove
        | all empty levels. The book state is updated with new best (bid/ask) levels.
        |________'''
        for price in self.bid.keys():
            if self.bid[price].isEmpty():
                del self.bid[ price ]
        
        for price in self.ask.keys():
            if self.ask[price].isEmpty():
                del self.ask[ price ]
        
    def clear(self):
        self.activeOrders.clear()
        self.bid.clear()
        self.ask.clear()
        
    def show(self):
        '''| TODO 
        | Called as a result of command 's'
        | Since the best price is listed first, and the maps used to store the levels are ordered,
        | this function outputs the bid levels by traversing the bid map in reverse (highest price first)
        |________'''
        
        if self.isEmpty():
            print "Book --- EMPTY ---"
        
        else:    
            if len( self.bid ) == 0:
                print "Bid depth --- EMPTY ---"
            else:
                print "Bid depth (highest priority at top):"
                print "Price     ", "Order Id  ", "Quantity  ", "Iceberg"
                
                # Highest price first
                for _, level in self.bid.iteritems():
                    level.show()
                print

            if len( self.ask ) == 0:
                print "Ask depth --- EMPTY ---"
            else:
                print "Ask depth (highest priority at top):"
                print "Price     ", "Order Id  ", "Quantity  ", "Iceberg"
                
                # Lowest price first
                for _, level in self.ask.iteritems():
                    level.show()
        print
