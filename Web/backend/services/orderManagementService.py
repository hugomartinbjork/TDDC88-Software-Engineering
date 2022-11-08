from backend.coremodels.order import Order
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from backend.Order_text_files import utils
from ..dataAccess.orderAccess import OrderAccess


@si.register(name='OrderManagementService')
class OrderManagementService():
    '''Order management service.'''

    @di.inject
    def __init__(self, _deps, *args):
        self.order_access: OrderAccess = _deps["OrderAccess"]()

    def get_order_by_id(self, id: int) -> Order:
        '''Returns order using id.'''
        return self.order_access.get_order_by_id(id)

    def text_file(self, order_name, article_id, storage,
                  eta, time_of_arrival):
        '''Makes text file.'''
        utils.make_text_file(order_name, article_id, storage, eta,
                             time_of_arrival)
