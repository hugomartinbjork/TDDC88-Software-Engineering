from datetime import timedelta
import string

from backend.coremodels.article import Article
from backend.coremodels.storage import Storage
from backend.coremodels.ordered_article import OrderedArticle
from ..coremodels.order import Order
from ..__init__ import dataAccessInjector as di


@di.register(name="OrderAccess")
class OrderAccess():
    '''Order Access.'''
    def get_order_by_id(self, id: int) -> Order:
        '''Get order by id.'''
        try:
            order = Order.objects.get(id=id)
            return order
        except Exception:
            return None

    def get_order_by_article_and_storage(self,
                                         storage_id, article_id) -> Order:
        '''Returns order using article and storage.'''
        order = Order.objects.filter(
            to_storage=storage_id, of_article=article_id).first()
        return order

    def get_ordered_article(self, order_id: int) -> Article:
        '''Retrieve article that has been ordered.'''
        try:
            article = self.get_order_by_id(order_id).of_article
            return article
        except Exception:
            return None

    def get_to_storage(self, order_id: int) -> Storage:
        '''Returns storage unit form order id.'''
        try:
            storage = self.get_order_by_id(order_id).to_storage
            return storage
        except Exception:
            return None

    def get_amount(self, order_id: int) -> int:
        '''Returns order amount from order id.'''
        try:
            amount = self.get_order_by_id(order_id).amount
            return amount
        except Exception:
            return None

    # Gets the estimated time of arrival by adding the expected wait to the
    #  date the order was ordered.
    def get_eta(self, order_id):
        '''Returns estimated time to arrival of order.'''
        order = self.get_order_by_id(order_id)
        if order is None:
            return None
        order_date = order.order_time
        days = order.expected_wait
        order_date = order_date + timedelta(days)
        return order_date

    def create_order(self, storage_id: string, estimated_delivery_date: int):
        '''Create new order.'''
        storage = Storage.objects.filter(id=storage_id).first()
        try:
            order = Order(to_storage=storage,
                          estimated_delivery_date=estimated_delivery_date)
            order.save()
        except Exception:
            return None
        return order

    def create_ordered_article(lio_id, quantity, unit, order):
        '''Creates an ordered_article model'''
        article = Article.objects.get(lio_id=lio_id)
        try:
            ordered_article = OrderedArticle(
                quantity=quantity, article=article, order=order, output_per_input=unit)
            ordered_article.save()
            return ordered_article
        except Exception:
            return None
