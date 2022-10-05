from backend.coremodels.order import Order
from backend.coremodels.storageUnit import StorageUnit
import storageManagementService
from datetime import timedelta, datetime
from backend.__init__ import si


@si.register(name='OrderService')
class OrderService():

    def has_order(self, storage_unit_id, article_id) -> Order:
        order = Order.objects.get(
            toStorageUnit=storage_unit_id, ofArticle=article_id)
        return order

    def order_arrived(self, order_id):
        try:
            order = Order.objects.get(id=order_id)
            # Storage.addToStorage() We'll implement this when we can.
        except:
            print("Order has not arrived")

    # Talk with elias for clarification
    def get_expected_wait(self, storage_unit_id, article_id, amount) -> Order.expectedWait:
        amount = StorageUnit.objects.get()
        if amount == 0:
            # Should it be a timedelta or just an integer?
            expected_wait = timedelta.days(14)
        else:
            expected_wait = timedelta.days(2)
        return expected_wait

    # We need some clarification here as well
    def place_order(self, storage_unit_id, article_id, amount):
        # Should we query the amount from a particular storage unit? Where does the amount come from?
        if amount == 0:
            Order.objects.create(
                article_id, storage_unit_id, timedelta.days(14), datetime.now())
        else:
            Order.objects.create(
                article_id, storage_unit_id, timedelta.days(2), datetime.now())

    # Should be storage service and not order service
    def has_stock(self):
        pass
