# from datetime import timedelta
# from datetime import datetime
import string
from backend.dataAccess.centralStorageAccess import centralStorageAccess
from backend.coremodels.order import Order
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.centralStorageSpace import CentralStorageSpace
from backend.coremodels.article import Article
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di
from backend.Order_text_files.utils import makeTextFile
from backend.Order_text_files import utils
from ..dataAccess.orderAccess import orderAccess


@si.register(name='OrderService')
class OrderService():
    @di.inject
    def __init__(self, _deps, *args):
        self._orderAccess: orderAccess = _deps["orderAccess"]()
        self._centralStorageAccess: centralStorageAccess = _deps[
                                                    "centralStorageAccess"]()

# Returns None if the order does not exist. Otherwise returns the order.
    def has_order(self, storage_unit_id, article_id) -> Order:
        return self._orderAccess.get_order_by_article_and_storage(
            storage_unit_id=storage_unit_id, article_id=article_id)

    # Updates the storage space amount with the amount in the order.
    # If order_arrived returns None, return error 404 in view.
    def order_arrived(self, order_id) -> Order:
        order = self._orderAccess.get_order_by_id(id)

        if order is None:
            return None

        # Checks if the order is already processesed so we dont process
        #  the same order twice.
        if order.hasArrived:
            return None

        # TODO: this should use storageAccess
        storage_unit = StorageUnit.objects.get(id=order.toStorageUnit)
        storage_space = StorageSpace.objects.get(storage=storage_unit)

        storage_space.amount = + order.amount
        storage_space.save()

        order.hasArrived = True
        order.save()
        return order

    # Gets expected time for order to arrive from central storage. Returns 14
    # days if the article does not exist.
    def calculate_expected_wait(self, article_id, amount) -> int:
        central_storage_stock = self._centralStorageAccess.getStockByArticleId(
                                                        article_id=article_id)
        if central_storage_stock is None:
            central_storage_stock = 0
        if central_storage_stock > amount:
            return 2
        else:
            return 14

    def getETA(self, orderId):
        return self._orderAccess.get_eta(orderId)

    # Creates an order, saves in in the database and then returns said order.
    # If the order can't be created None is returned.
    def place_order(self, storage_unit_id, article_id, amount):
        expectedWait = OrderService.calculate_expected_wait(
            self, article_id=article_id, amount=amount)
        order = self._orderAccess.create_order(
            storageId=storage_unit_id, articleId=article_id,
            amount=amount, expectedWait=expectedWait)
        if order is not None:
            makeTextFile(order.id, article_id, storage_unit_id,
                         order.expectedWait, order.orderTime)
        return order

    # Places an order if there is no order of that article to that storage.
    # If there is, that order is returned
    def place_order_if_no_order(self, storage_unit_id: string,
                                article_id: string, amount: int) -> Order:
        current_order = self._orderAccess.get_order_by_article_and_storage(
            storage_unit_id=storage_unit_id, article_id=article_id)
        if (current_order is None):
            current_order = self._orderAccess.create_order(
                storageId=storage_unit_id, articleId=article_id, amount=amount
            )
        return current_order

    def getOrderById(self, id: int) -> Order:
        return self._orderAccess.get_order_by_id(id)

    def getArticleIdById(self, id: int) -> Article:
        return self._orderAccess.getOrderedArticle(id)

    def getStorageUnitIdById(self, id: int) -> StorageUnit:
        return self._orderAccess.getToStorageUnit(id)

    def getAmountIdById(self, id: int) -> int:
        return self._orderAccess.getAmount(id)

    def textFile(orderName, article_id, storage_unit, eta, timeOfArrival):
        utils.makeTextFile(orderName, article_id, storage_unit,
                           eta, timeOfArrival)
        article = Article.objects.filter(lioId=article_id).first()
        if CentralStorageSpace.objects.filter(
                        article=article).first() is not None:
            amount = CentralStorageSpace.objects.filter(
                                article=article).first().amount
            return amount
        else:
            return None
