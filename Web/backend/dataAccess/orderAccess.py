from datetime import timedelta
import string

from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from ..coremodels.order import Order
from ..__init__ import dataAccessInjector as di


@di.register(name="orderAccess")
class orderAccess():
    def get_order_by_id(self, id: int) -> Order:
        try:
            order = Order.objects.get(id=id)
            return order
        except Exception:
            return None

    def get_order_by_article_and_storage(self,
                                         storage_unit_id, article_id) -> Order:
        order = Order.objects.filter(
            toStorageUnit=storage_unit_id, ofArticle=article_id).first()
        return order

    def getOrderedArticle(self, orderId: int) -> Article:
        try:
            article = self.get_order_by_id(orderId).ofArticle
            return article
        except Exception:
            return None

    def getToStorageUnit(self, orderId: int) -> StorageUnit:
        try:
            storageUnit = self.get_order_by_id(orderId).toStorageUnit
            return storageUnit
        except Exception:
            return None

    def getAmount(self, orderId: int) -> int:
        try:
            amount = self.get_order_by_id(orderId).amount
            return amount
        except Exception:
            return None

    # Gets the estimated time of arrival by adding the expected wait to the
    #  date the order was ordered.
    def get_eta(self, orderId):
        order = self.get_order_by_id(orderId)
        if order is None: 
            return None
        orderDate = order.orderTime
        days = order.expectedWait
        orderDate = orderDate + timedelta(days)
        return orderDate

    def create_order(self, storageId: string, articleId: string, amount: int,
                     expectedWait: int):
        article = Article.objects.filter(lioId=articleId).first()
        storageUnit = StorageUnit.objects.filter(id=storageId).first()
        try:
            order = Order(
                ofArticle=article, toStorageUnit=storageUnit,
                amount=amount, expectedWait=expectedWait)
            order.save()
        except Exception:
            return None

        return order
