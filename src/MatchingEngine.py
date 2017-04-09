from Order import Order
from Book  import Book

class MatchingEngine(object):
    '''| TODO
    |
    |________''' 

    def __init__(self):
        self.myBook = Book()

        
    def addOrder(self, isBid, orderId, price, qty, peakSize):
        '''| TODO 
        | price is an integer number, i.e. divide by 100 to get the actual price
        |________'''
		
        if self.myBook.isPresent( orderId ):
            print "Order with the same Id (", orderId, ") found! Order will not be added to the Book!"
        else:
            self.matchOrder(isBid, orderId, price, qty, peakSize)
        

    def removeOrder(self, orderId):
        '''| TODO 
        | Called as a result of command X (remove order)
        |________'''
        if self.myBook.removeOrder(orderId):
            print "Order removed:", orderId
            self.myBook.removeEmptyLevels()
        else:
            print "Order not found:", orderId


    def showBook(self):
        '''| TODO 
        | Called as a result of command s (show book state)
        |________'''
        myBook.show()

# TODO: Verbose or log i.s.o. print?
    def matchOrder(self, isBid, orderId, price, quantity, peakSize):
        '''|
        | Match a bid/ask order against the orders of the ask/bid depth of the book starting from the best ask/bid price level
        |________'''
        
        matching_side = self.myBook.ask if isBid else self.myBook.bid

        if len(matching_side) != 0:
            # Iterating over the different price levels
            for lprice, level in matching_side.iteritems():
                match = lprice <= int(price*100) if isBid else lprice >= int(price*100) 
# Note:                 best ask price <= bid price            best bid price >= ask price
                if match: 
                    # Check complete or partial fills against visible and iceberg orders
                    quantity = self.checkExecution(level, quantity, orderId)
                    
                    # Remove filled orders, update iceberg orders - visible and invisible part
                    self.updateLevel(level)
                                  
                    # Continue with the next price level (if needed)
                    # Exit the loop if the incoming order is completely filled or the matching side of the book becomes empty
                    if quantity == 0:
                        break
                else:
                    break
                
            # Clean the book from levels containing only filled orders; in this way - set the next best price
            self.myBook.removeEmptyLevels();

        # Add an order (also, if not filled completely)
        if quantity > 0: 
            if peakSize > quantity:
                peakSize = quantity
            self.myBook.addOrder(isBid, orderId, price, quantity, peakSize)
            str_o = "B" if isBid else "A"
            print "A:",  str_o, orderId, price, quantity, peakSize



    def checkFill(self, level, myQty, orderId):
        for order in level:
            if order.quantity >= myQty: # complete fill of incoming order
                # E <incoming order id> <matched order id> <price> <matched quantity>
                print "E1", orderId, "with", order.orderId, order.price, myQty
                order.quantity -= myQty # update order
                myQty = 0               # all matched
                return myQty
            
            else: # partial fill of incoming order (order.quantity < myQty)
                print "E2", orderId, "with", order.orderId, order.price, order.peakSize
                myQty -= order.quantity # matched quantity
                order.quantity = 0      # marked to be removed
                
        return myQty


    def checkExecution(self, level, myQty, orderId):
        '''|
        | First check visible orders, then icebergs
        | Returns remaining quantity
        |________'''
        remQty                = self.checkFill(level.visible_orders,  myQty, orderId)
        if remQty > 0: remQty = self.checkFill(level.icebergs,       remQty, orderId)
        return remQty
    

    def updateLevel(self, level):
        '''| TODO 
        | Matched orders from the book are marked as 'peakSize=0'. This indicates that they have to be removed from the level
        | The visible part of iceberg orders is replenished with a 'reload' value <= peakSize and moved back to the queue of visible orders
        | If a hidden part of an iceberg does not have a remaining quantity anymore, it is removed from the level.
        |________'''
        
        for order in list(level.visible_orders): # Note: list() due to RuntimeError: deque mutated during iteration
            if order.quantity == 0:
                # Remove filled limit orders from the book
                orderId = order.orderId
                # From the particular level
                level.removeVisible( orderId )
                # Remove the order from the map of active orders
                self.myBook.removeActiveOrder( orderId ) # TODO: Check isIceberg and not remove if True?
                print "Removed (visible) Id:", orderId
                
        for order in list(level.icebergs): # Note: list() due to RuntimeError: deque mutated during iteration
            
            if order.quantity == 0: # Complete fill
                self.myBook.removeOrder( order.orderId )

            else: # replanish visible part 
                if order.peakSize < order.quantity: # update the quantity accordingly
                    order.quantity -= order.peakSize 

                else: # order.peakSize >= quantity
                    order.peakSize = order.quantity
                    # Remove the invisible part of the iceberg because its quantity is consumed
                    level.removeIceberg( orderId )
                    print "Iceberg removed", orderId

                # Replenish the visible part of the order
                myOrder = Order(order.isBuy, order.orderId, order.price, order.peakSize, order.peakSize)
                myOrder.isIceberg = True # peakSize can be == quantity

                # Add the visible part of the order at the end of the queue of visible orders
                self.myBook.addOrder( order = myOrder )
                
                print "Replanished", order.orderId
