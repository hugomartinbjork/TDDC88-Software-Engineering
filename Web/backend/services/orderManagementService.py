from backend.coremodels.order import Order
from backend.__init__ import serviceInjector as si 
from ..__init__ import dataAccessInjector as di
from backend.Order_text_files import utils
from ..dataAccess.orderAccess import orderAccess

@si.register(name = 'orderManagementService')
class orderManagementService():
    
    @di.inject
    def __init__(self, _deps, *args):
        self._orderAccess : orderAccess = _deps["orderAccess"]()

    def getOrderById(self, id: int) -> Order:
        return self._orderAccess.getOrderById(id)

    def textFile(orderName, article_id, storage_unit, eta, timeOfArrival):
        utils.makeTextFile(orderName, article_id, storage_unit, eta, timeOfArrival)
