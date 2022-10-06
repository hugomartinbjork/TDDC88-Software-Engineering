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

    def getArticleIdById(self, id: int) -> Order:
        try:
            article = Order.objects.get(id=id).ofArticle
            return article
        except:
            return None

    def getstorageSpaceIdById(self, id: int) -> Order:
        try:
            storageSpace = Order.objects.get(id=id).toStorageUnit
            return storageSpace
        except:
            return None

    def getAmountIdById(self, id: int) -> Order:
        try:
            amount = Order.objects.get(id=id).amount
            return amount
        except:
            return None

    def textFile(orderName, article_id, storage_unit, eta, timeOfArrival):
        utils.makeTextFile(orderName, article_id, storage_unit, eta, timeOfArrival)
