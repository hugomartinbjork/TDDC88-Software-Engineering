from backend.coremodels.order import Order
from backend.__init__ import si 
from backend.Order_text_files import utils

@si.register(name = 'orderManagementService')
class orderManagementService():
    def getOrderById(self, id: int) -> Order:
        try:
            article = Order.objects.get(id=id)  
            return article
        except:
            return None

    def textFile(orderName, article_id, storage_unit, eta, timeOfArrival):
        utils.makeTextFile(orderName, article_id, storage_unit, eta, timeOfArrival)
