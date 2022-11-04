from datetime import timedelta
import string

from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from ..coremodels.order import Order
from ..__init__ import dataAccessInjector as di


@di.register(name="OrderAccess")
class OrderAccess():
    def get_order_by_id(self, id: int) -> Order:
        try:
            order = Order.objects.get(id=id)
            return order
        except Exception:
            return None

    def get_order_by_article_and_storage(self,
                                         storage_unit_id, article_id) -> Order:
        order = Order.objects.filter(
            to_storage_unit=storage_unit_id, of_article=article_id).first()
        return order

    def get_ordered_article(self, order_id: int) -> Article:
        try:
            article = self.get_order_by_id(order_id).of_article
            return article
        except Exception:
            return None

    def get_to_storage_unit(self, order_id: int) -> StorageUnit:
        try:
            storage_unit = self.get_order_by_id(order_id).to_storage_unit
            return storage_unit
        except Exception:
            return None

    def get_amount(self, order_id: int) -> int:
        try:
            amount = self.get_order_by_id(order_id).amount
            return amount
        except Exception:
            return None

    # Gets the estimated time of arrival by adding the expected wait to the
    #  date the order was ordered.
    def get_eta(self, order_id):
        order = self.get_order_by_id(order_id)
        if order is None:
            return None
        order_date = order.order_time
        days = order.expected_wait
        order_date = order_date + timedelta(days)
        return order_date

    def create_order(self, storage_id: string, article_id: string, amount: int,
                     expected_wait: int):
        article = Article.objects.filter(lio_id=article_id).first()
        storage_unit = StorageUnit.objects.filter(id=storage_id).first()
        try:
            order = Order(
                of_article=article, to_storage_unit=storage_unit,
                amount=amount, expected_wait=expected_wait)
            order.save()
        except Exception:
            return None

        return order
