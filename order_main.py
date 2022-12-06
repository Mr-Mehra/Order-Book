#we will parse the input as it comes 
# we maintain a map storing two corresponding priorty queues for each order book (key of map is book number)
# for each command we will see the corresponding book number ,and access the corresponding heaps 
# each order also has a order attribute which we will also store in a map
# if we get delete order type of command then we will see if particular order exsists in our heaps and remove it 
# if we get add order type of buy type then we add it in max heap of buy type 
# if we get add order type of sell type then we add it in min heap of sell type 
# now while the top of buy is greater than top of sell ,we remove the corresponding orders from the heaps (our order books)
# if we have received a buy order then at this step we would could have removed some orders from sell heap and updated the volume of a trade in sell book
# we just have to update the orders as described 
# .....
books = {
}
time = 0
import xml.etree.ElementTree as ET
tree = ET.parse('temp.xml')
root = tree.getroot()
class Book:
    def _init_(self, name):
        self.name = name
        self.sell_book = []
        self.buy_book = [] 
for child in root:
    book = child.attrib['book']
    price = float(child.attrib['price'])
    child.attrib['Time'] = time
    op = child.attrib['operation']
    vol = float(child.attrib['volume'])
    time += 1
    if book not in books:
        books[book] = Book(book)
    if child.tag == 'DeleteOrder':
        if child.attrib['operation'] == 'SELL':
            books[book].sell_book.remove(child.attrib['orderId'])
        else:
            books[book].buy_book.remove(child.attrib['orderId'])
    else:
        if child.attrib['operation'] == 'SELL':
            for order in books[book].buy_book:
                if float(order.attrib['price']) >= price:
                    if order.attrib['volume'] > vol:
                        order.attrib['volume'] -= vol
                        vol = 0
                    else:
                        books[book].buy_book.remove(order)
                        vol -= int(order.attrib['volume'])
                        books[book].buy_book.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                else:
                    break
            if vol > 0:
                books[book].sell_book.append(child)
                child.attrib['volume'] = vol
                books[book].sell_book.sort(key=lambda x: float(x.attrib['price']))
                break
        else:
            for order in books[book].sell_book:
                if float(order.attrib['price']) <= price:
                    if order.attrib['volume'] > vol:
                        order.attrib['volume'] -= vol
                        vol = 0
                    else:
                        vol -= int(order.attrib['volume'])
                        books[book].sell_book.remove(order)
                        books[book].sell_book.sort(key=lambda x: float(x.attrib['price']))
                else:
                    break
            if vol > 0:
                child.attrib['volume'] = vol
                books[book].buy_book.append(child)
                books[book].buy_book.sort(key=lambda x: float(x.attrib['price']), reverse=True)
                break
