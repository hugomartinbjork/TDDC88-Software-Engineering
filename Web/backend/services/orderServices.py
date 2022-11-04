# from datetime import timedelta
# from datetime import datetime
import string
from backend.dataAccess.centralStorageAccess import CentralStorageAccess
from backend.coremodels.order import Order
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.centralStorageSpace import CentralStorageSpace
from backend.coremodels.article import Article
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from backend.Order_text_files.utils import make_text_file
from backend.Order_text_files import utils
from ..dataAccess.orderAccess import OrderAccess


@si.register(name='OrderService')
class OrderService():
    @di.inject
    def __init__(self, _deps, *args):
        self.order_access: OrderAccess = _deps["OrderAccess"]()
        self.central_storage_access: CentralStorageAccess = _deps[
                                                    "CentralStorageAccess"]()

# Returns None if the order does not exist. Otherwise returns the order.
    def has_order(self, storage_unit_id, article_id) -> Order:
        return self.order_access.get_order_by_article_and_storage(
            storage_unit_id=storage_unit_id, article_id=article_id)

    # Updates the storage space amount with the amount in the order.
    # If order_arrived returns None, return error 404 in view.
    def order_arrived(self, order_id) -> Order:
        order = self.order_access.get_order_by_id(id)

        if order is None:
            return None

        # Checks if the order is already processesed so we dont process
        #  the same order twice.
        if order.has_arrived:
            return None

        # TODO: this should use StorageAccess
        storage_unit = StorageUnit.objects.get(id=order.to_storage_unit)
        storage_space = StorageSpace.objects.get(storage=storage_unit)

        storage_space.amount = + order.amount
        storage_space.save()

        order.has_arrived = True
        order.save()
        return order

    # Gets expected time for order to arrive from central storage. Returns 14
    # days if the article does not exist.
    def calculate_expected_wait(self, article_id, amount) -> int:
        central_storage_stock = (
                        self.central_storage_access.get_stock_by_article_id(
                            article_id=article_id))
        if central_storage_stock is None:
            central_storage_stock = 0
        if central_storage_stock > amount:
            return 2
        else:
            return 14

    def get_eta(self, order_id):
        return self.order_access.get_eta(order_id)

    # Creates an order, saves in in the database and then returns said order.
    # If the order can't be created None is returned.
    def place_order(self, storage_unit_id, article_id, amount):
        expected_wait = OrderService.calculate_expected_wait(
            self, article_id=article_id, amount=amount)
        order = self.order_access.create_order(
            storage_id=storage_unit_id, article_id=article_id,
            amount=amount, expected_wait=expected_wait)
        if order is not None:
            make_text_file(order.id, article_id, storage_unit_id,
                           order.expected_wait, order.order_time)
        return order

    # Places an order if there is no order of that article to that storage.
    # If there is, that order is returned
    def place_order_if_no_order(self, storage_unit_id: string,
                                article_id: string, amount: int) -> Order:
        current_order = self.order_access.get_order_by_article_and_storage(
            storage_unit_id=storage_unit_id, article_id=article_id)
        if (current_order is None):
            current_order = self.order_access.create_order(
                storage_id=storage_unit_id,
                article_id=article_id, amount=amount)
        return current_order

    def get_order_by_id(self, id: int) -> Order:
        return self.order_access.get_order_by_id(id)

    def get_article_id_by_id(self, id: int) -> Article:
        return self.order_access.get_ordered_article(id)

    def get_storage_unit_id_by_id(self, id: int) -> StorageUnit:
        return self.order_access.get_to_storage_unit(id)

    def get_amount_id_by_id(self, id: int) -> int:
        return self.order_access.get_amount(id)

    def text_file(order_name, article_id, storage_unit, eta, time_of_arrival):
        utils.make_text_file(order_name, article_id, storage_unit,
                             eta, time_of_arrival)
        article = Article.objects.filter(lio_id=article_id).first()
        if CentralStorageSpace.objects.filter(
                        article=article).first() is not None:
            amount = CentralStorageSpace.objects.filter(
                                article=article).first().amount
            return amount
        else:
            return None
