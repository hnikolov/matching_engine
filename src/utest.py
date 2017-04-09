from Order import Order, FifoDeque
from Level import Level
from Book  import Book
from MatchingEngine import MatchingEngine

from utils import *

# TESTS --------------
def utest_CheckBooks():
    print '-- CheckBooks function --',
    book_1, book_2 = [ createBook() for _ in range(2) ]
    checkBooks( book_1, book_2 )
    print 'OK'
    

def utest_FifoDeque():
    print '-- FifoDeque --',
    f   = FifoDeque()
    ref = []
    
    for i in range(10): 
        f.append(i)
        ref.append(i)
    
    assert len(f) == 10, "Wrong FifoDeque len! Expected: 10"
    for d,r in zip(f,ref): assert d == r, "Wrong data"
        
    f.pop() # remove '0'
    assert len(f) == 9, "Wrong FifoDeque len! Expected: 9"
    assert 0 not in f,  "Expected element not removed"

    del f[0] # remove '1'
    assert len(f) == 8, "Wrong FifoDeque len! Expected: 8"
    assert 1 not in f,  "Expected element not removed"

    del f[3] # remove '5'
    assert len(f) == 7, "Wrong FifoDeque len! Expected: 7"
    assert 5 not in f,  "Expected element not removed"

    f.pop() # remove '2'
    assert len(f) == 6, "Wrong FifoDeque len! Expected: 6"
    assert 2 not in f,  "Expected element not removed"

    f.append(43)    
    assert len(f) == 7, "Wrong FifoDeque len! Expected: 7"
    assert 43 in f,  "Expected element not added"
    
    print 'OK'
    

def utest_Order():    
    print '-- Order --',
    o  = Order(    BID,         999, 123.45,  100, 100)
    checkOrder(o,  True, False, 999, 123.45,  100, 100, 100)

    o1 = Order(    BID,        9191,  32.54, 1000, 100) # iceberg
    checkOrder(o1, True, True, 9191,  32.54, 1000, 100, 100)

    o2 = Order(    ASK,          999, 123.45,  100, 100)
    checkOrder(o2, False, False, 999, 123.45,  100, 100, 100)

    o3 = Order(    ASK,         9191, 324,    1000, 100) # iceberg
    checkOrder(o3, False, True, 9191, 324,    1000, 100, 100)
    
    print 'OK'
    

def utest_Level():    
    print '-- Level --',
    bo, ao = createOrders()   
    
    l = Level()
    
    l.addOrder(bo)
    assert len(l.visible_orders) == 1, "Wrong Level len! Expected: 1"
    assert len(l.icebergs)       == 0, "Wrong Level len! Expected: 0"
    
    l.addOrder(ao)
    assert len(l.visible_orders) == 2, "Wrong Level len! Expected: 2"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"

    l.removeVisible(999)
    assert len(l.visible_orders) == 1, "Wrong Level len! Expected: 1"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"

    l.removeVisible(19191) # wrong orderId
    assert len(l.visible_orders) == 1, "Wrong Level len! Expected: 1"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"

    l.removeVisible(9191)
    assert len(l.visible_orders) == 0, "Wrong Level len! Expected: 0"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"

    l.removeIceberg(19191) # wrong orderId
    assert len(l.visible_orders) == 0, "Wrong Level len! Expected: 0"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"

    l.removeIceberg(9191)
    assert len(l.visible_orders) == 0, "Wrong Level len! Expected: 0"
    assert len(l.icebergs)       == 0, "Wrong Level len! Expected: 0"

    # Repeats from beginning
    bo, ao = createOrders()
    l.addOrder(bo)
    l.addOrder(ao)
    assert len(l.visible_orders) == 2, "Wrong Level len! Expected: 2"
    assert len(l.icebergs)       == 1, "Wrong Level len! Expected: 1"
    
    l.remove(9191)
    assert len(l.visible_orders) == 1, "Wrong Level len! Expected: 1"
    assert len(l.icebergs)       == 0, "Wrong Level len! Expected: 0"
    
    l.remove(999)
    assert l.isEmpty() == True, "Level is not empty!"
        
# TODO Use checkLevels()
#    o1 = Order(ASK, 12,  32.54, 200, 100) # iceberg
#    l.addOrder(o1)
#
#    o1 = Order(ASK, 21,  67.89, 201, 100) # iceberg
#    l.addOrder(o1)

    print 'OK'

    
def utest_Book():    
    print '-- Book --',
    bo, ao = createOrders()
    b = Book()
    assert b.isEmpty()         == True,  "Book not empty!" 
    assert b.isPresent(999)    == False, "Order found in an empty book!"
        
    b.addOrder( order=bo )
    assert b.isBidEmpty()      == False, "Bid level is empty!" 
    assert b.isAskEmpty()      == True,  "Ask level not empty!"
    assert b.isEmpty()         == False, "Book is empty!" 
    assert b.isPresent(999)    == True,  "Order '999' not present!"

    b.addOrder( order=ao )
    assert b.isBidEmpty()      == False, "Bid level is empty!" 
    assert b.isAskEmpty()      == False, "Ask level is empty!"
    assert b.isEmpty()         == False, "Book is empty!" 
    assert b.isPresent(9191)   == True,  "Order '9191' not present!"
    
    assert b.removeOrder(999)  == True,  "Removing order '999' failed!"
    assert b.isBidEmpty()      == False, "Bid level is empty!" 
    assert b.isAskEmpty()      == False, "Ask level is empty!"
    assert b.isEmpty()         == False, "Book is empty!" 
        
    b.removeEmptyLevels()
    assert b.isBidEmpty()      == True,  "Bid level not empty!" 
    assert b.isAskEmpty()      == False, "Asklevel is empty!"
    assert b.isEmpty()         == False, "Book is empty!" 

    assert b.removeOrder(9191) == True,  "Removing order '9191' failed!"
    assert b.isBidEmpty()      == True,  "Bid level not empty!" 
    assert b.isAskEmpty()      == False, "Ask level is empty!"
    assert b.isEmpty()         == True,  "Book not empty!" 
    
    b.removeEmptyLevels()
    assert b.isBidEmpty()      == True,  "Bid level not empty!" 
    assert b.isAskEmpty()      == True,  "Ask levle not empty!"
    
    b.addOrder( order=bo )
    b.addOrder( order=ao )

    b.addOrder(BID, 199, 54.12, 1000, 100) # iceberg
    b.addOrder(BID, 111, 54.12,  100, 100)
    
    assert len(b.bid) == 2, "Wrong number of bid level! Expected: 2"
    
    prev_price = 1000*100
    for lprice, level in b.bid.iteritems():
        assert lprice < prev_price, "Order of levels not monotonically decending in price"
        prev_price = lprice

    b.addOrder(ASK, 191,  45.23,  100, 100)
    b.addOrder(ASK, 777,  32.54,  100, 100)
    b.addOrder(ASK, 991,  22.21,  100, 100)
    b.addOrder(ASK, 181, 222.22,  100, 100)
    b.addOrder(ASK, 888,  32.54,  100, 100)
    b.addOrder(ASK,  33,  25.18,  100, 100)
    b.addOrder(ASK, 111,  25.18,  100, 100)

    assert len(b.ask) == 5, "Wrong number of ask level! Expected: 5"

    prev_price = 0*100
    for lprice, level in b.ask.iteritems():
        assert lprice > prev_price, "Order of levels not monotonically increasing in price"
        prev_price = lprice
    
    b.clear()
    assert b.isEmpty() == True, "Book not empty!" 

    print 'OK'
    
# TODO: Verbose
def utest_MatchingEngine_1():    
    print '-- Matching Engine: Add orders, clear book --'
    m = MatchingEngine()
    assert m.myBook.isEmpty() == True,  "Book not empty!"

    m.addOrder(ASK, 191, 145.23,  100, 100)
    m.addOrder(BID, 199,  54.12, 1000, 100) # iceberg
    m.addOrder(BID, 111,  54.12,  100, 100)
    
    assert len(m.myBook.activeOrders) == 3, "Wrong number of active orders! Expected: 3"
        
    assert len(m.myBook.bid) == 1, "Wrong number of bid level! Expected: 1"
    assert len(m.myBook.ask) == 1, "Wrong number of ask level! Expected: 1"
    
    assert m.myBook.isEmpty() == False, "Book is empty!"

    m.myBook.clear()
    assert m.myBook.isEmpty() == True,  "Book not empty!"

def utest_MatchingEngine_2():    
    print '-- Matching Engine: Remove order --'
    m = MatchingEngine()

    m.addOrder(BID,  111,  54.12,  100, 100)
    assert m.myBook.isEmpty() == False, "Book is empty!"
    m.removeOrder(111)
    assert m.myBook.isEmpty() == True,  "Book not empty!"

    m.addOrder(BID,  199,  54.12, 1000, 100) # iceberg
    assert m.myBook.isEmpty() == False, "Book is empty!"
    m.removeOrder(199)
    assert m.myBook.isEmpty() == True,  "Book not empty!"

def utest_MatchingEngine_3():    
    print '-- Matching Engine: Complete fills, no icebergs --'
    m = MatchingEngine()
    
    m.addOrder(ASK, 191,  145.23,  100, 100)
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    m.addOrder(ASK, 191,  145.23,  100, 100) # Should not be added
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    
    m.addOrder(BID,  222,  145.23,  100, 100) # Complete fill
    m.myBook.show()
    assert m.myBook.isEmpty() == True,  "Book not empty!"

    m.addOrder(BID,  222,  145.23,  100, 100)
    m.addOrder(ASK, 191,  145.23,  100, 100) # Complete fill
    assert m.myBook.isEmpty() == True,  "Book not empty!"

def utest_MatchingEngine_4():    
    print '-- Matching Engine: Complete fills, Icebergs --'
    m = MatchingEngine()
    
    m.addOrder(ASK, 191,  145.23,  500, 100) # iceberg
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    m.addOrder(ASK, 191,  145.23,  500, 100) # Should not be added
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    
    m.addOrder(BID,  222,  145.23,  500, 500) # Complete fill
    assert m.myBook.isEmpty() == True,  "Book not empty!"

    m.addOrder(BID, 222,  145.23,  1000, 100) # iceberg
    m.myBook.show()
    m.addOrder(ASK, 191,  145.23,  1000, 100) # Complete fill
    assert m.myBook.isEmpty() == True,  "Book not empty!"

def utest_MatchingEngine_5():    
    print '-- Matching Engine: Partial fill of resting iceberg --'
    m = MatchingEngine()
        
    m.addOrder(BID, 222,  145.23,  1000, 100) # iceberg
    m.myBook.show()
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    m.addOrder(ASK, 191,  145.23,  300, 300) # Partial fill of resting iceberg
    m.myBook.show()
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    m.addOrder(ASK, 192,  145.23,  300, 100) # Partial fill of resting iceberg
    m.myBook.show()
    assert len(m.myBook.activeOrders) == 1, "Wrong number of active orders! Expected: 1"
    m.addOrder(ASK, 193,  145.23,  350, 350) # Partial fill of resting iceberg, only visible part left
    m.myBook.show()
    m.addOrder(ASK, 194,  145.23,   50,  50) # Complete fill
    assert m.myBook.isEmpty() == True,  "Book not empty!"

def utest_MatchingEngine_14():    
    print '-- Matching Engine --'
    m = MatchingEngine()

# Example:
    m.addOrder(ASK, 1, 56.5,  9000,  2000) 
    m.addOrder(ASK, 2, 56.5,  3000,  3000) 
    m.addOrder(ASK, 3, 56.6, 20000, 20000) 
    m.myBook.show()
    
    m.addOrder(BID, 4, 56.6, 8000, 8000) 
    m.myBook.show()
    
    b = Book()
    b.addOrder(ASK, 1, 56.5,  4000,  2000)
    b.addOrder(ASK, 3, 56.6, 20000, 20000) 
#    b.show()
    checkBooks( m.myBook, b )
    
# Another Example: TODO
    
    print 'OK'
    
if __name__ == '__main__':

    utest_FifoDeque()
    utest_Order()
    utest_Level()
    utest_Book()
    utest_CheckBooks()
    utest_MatchingEngine_1()
    utest_MatchingEngine_2()
    utest_MatchingEngine_3()
    utest_MatchingEngine_4()
    utest_MatchingEngine_5()
    utest_MatchingEngine_14()
    