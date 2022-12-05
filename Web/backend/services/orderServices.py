from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di

from ..dataAccess.centralStorageAccess import CentralStorageAccess
from ..dataAccess.orderAccess import OrderAccess
from ..dataAccess.storageAccess import StorageAccess

from backend.coremodels.order import Order
from backend.coremodels.storage import Storage
from backend.coremodels.compartment import Compartment
from backend.coremodels.centralStorageSpace import CentralStorageSpace
from backend.coremodels.article import Article
from datetime import datetime

from backend.Order_text_files.utils import make_text_file


@si.register(name='OrderService')
class OrderService():
    '''Order service class includes helper functions for all Order related endpoints.'''
    @di.inject
    def __init__(self, _deps, *args):
        self.order_access: OrderAccess = _deps["OrderAccess"]()
        self.central_storage_access: CentralStorageAccess = _deps[
            "CentralStorageAccess"]()
        self.storage_access: StorageAccess = _deps[
            "StorageAccess"]()

    def get_orders(self) -> Order:
        return self.order_access.get_orders()

    def delete_order(self, id, order_state):
        return self.order_access.delete_order(id=id, order_state=order_state)

# Returns None if the order does not exist. Otherwise returns the order.
    def has_order(self, storage_id, article_id) -> Order:
        '''Returns order from storage unit id and article id.'''
        return self.order_access.get_order_by_article_and_storage(
            storage_id=storage_id, article_id=article_id)

    def order_arrived(self, order_id) -> Order:
        '''Order arrived.'''
        order = self.order_access.get_order_by_id(order_id)

        if order is None:
            return None

        ordered_articles = OrderAccess.get_ordered_articles(order_id)

        if ordered_articles is None:
            return None

        # So we do not handle same order twice.
        if order.order_state == "delivered":
            return None

        # storage = Storage.objects.get(id=order.to_storage)
        storage = self.storage_access.get_storage(order.to_storage.id)
        for ordered_article in ordered_articles:
            compartment = Compartment.objects.get(
                storage=storage, article=ordered_article.article)

            if compartment == None:
                return None

            if ordered_article.unit == "output":
                compartment.amount += ordered_article.quantity
                compartment.save()
            elif ordered_article.unit == "input":
                article = Article.objects.filter(
                    lio_id=ordered_article.article.lio_id).first()
                compartment.amount += ordered_article.quantity * article.output_per_input
                compartment.save()

        order.order_state = "delivered"
        order.delivery_date = datetime.now()
        order.save()
        return order

    # Gets expected time for order to arrive from central storage. Returns 14
    # days if the article does not exist.
    def calculate_expected_wait(self, article_id, amount) -> int:
        '''Calculate expected wait.'''
        central_storage_stock = (
            CentralStorageAccess.get_stock_by_article_id(self,
                                                         article_id=article_id))
        if central_storage_stock is None:
            return None
        if central_storage_stock > amount:
            return 2
        else:
            return 14

    def get_eta(self, order_id):
        '''Return estimated time to arrival of order.'''
        return self.order_access.get_eta(order_id)

    def place_order(self, storage_id, estimated_delivery_date, ordered_articles):
        '''Creates an order, saves in in the database and then returns said order.
        If order can't be created, None is returned'''
        order = OrderAccess.create_order(
            storage_id=storage_id, estimated_delivery_date=estimated_delivery_date)
        if order is not None:
            make_text_file(order.id, storage_id, ordered_articles,
                           order.estimated_delivery_date, order.order_date)
        return order

    # Places an order if there is no order of that article to that storage.
    # If there is, that order is returned
    def place_order_if_no_order(self, storage_id: str,
                                article_id: str, amount: int) -> Order:
        '''Place order if no order.'''
        current_order = self.order_access.get_order_by_article_and_storage(
            storage_id=storage_id, article_id=article_id)
        if (current_order is None):
            current_order = self.order_access.create_order(
                storage_id=storage_id,
                article_id=article_id, amount=amount)
        return current_order

    def get_order_by_id(self, id: int) -> Order:
        '''Returns order using id.'''
        return self.order_access.get_order_by_id(id)

    def get_article_id_by_id(self, id: int) -> Article:
        '''Returns article using id.'''
        return self.order_access.get_ordered_article(id)

    def get_storage_id_by_id(self, id: int) -> Storage:
        '''Returns storage unit using id.'''
        return self.order_access.get_to_storage(id)

    def get_amount_id_by_id(self, id: int) -> int:
        '''Get amount id by id.'''
        return self.order_access.get_amount(id)

    def text_file(order_name, article_id, storage,
                  eta, time_of_arrival):
        '''Makes text file and returns amount.'''
        make_text_file(order_name, article_id, storage,
                       eta, time_of_arrival)
        article = Article.objects.filter(lio_id=article_id).first()
        if CentralStorageSpace.objects.filter(
                article=article).first() is not None:
            amount = CentralStorageSpace.objects.filter(
                article=article).first().amount
            return amount
        else:
            return None

    def create_ordered_article(lio_id, quantity, unit, order):
        CentralStorageAccess.update_central_storage_quantity(article_id=lio_id, quantity=quantity)
        '''Creates an ordered_article model'''
        return OrderAccess.create_ordered_article(lio_id, quantity, unit, order)

    def get_ordered_articles(self, order_id):
        '''returns article in the specified order'''
        return OrderAccess.get_ordered_articles(order_id)

    def get_all_ordered_articles(self):
        return OrderAccess.get_all_ordered_articles()
