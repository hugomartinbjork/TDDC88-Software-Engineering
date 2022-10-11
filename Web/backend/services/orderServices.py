from backend.coremodels.order import Order
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.centralStorageSpace import CentralStorageSpace
from backend.__init__ import si


@si.register(name='OrderService')
class OrderService():

    # Returns None if the order does not exist. Otherwise returns the order.
    def has_order(self, storage_unit_id, article_id) -> Order:
        order = Order.objects.filter(
            toStorageUnit=storage_unit_id, ofArticle=article_id).first()
        return order

    # Updates the storage space amount with the amount in the order.
    # If order_arrived returns None, return error 404 in view.
    def order_arrived(self, order_id) -> Order:
        order = Order.objects.filter(id=order_id).first()

        if order is None:
            return None
            

        # Checks if the order is already processesed so we dont process the same order twice.
        if order.hasArrived == False:
            return None

        storage_unit = StorageUnit.objects.get(id=order.toStorageUnit)
        storage_space = StorageSpace.objects.get(storage=storage_unit)

        storage_space.amount = + order.amount
        storage_space.save()

        order.hasArrived = True
        order.save()
        return order

    # Gets expected time for order to arrive from central storage. Returns 14 days if the article does not exist.
    def get_expected_wait(self, article_id, amount) -> int:
        central_storage_stock = self.has_stock(article_id)

        if central_storage_stock is None:
            central_storage_stock = 0

        if central_storage_stock > amount:
            return 2
        else:
            return 14

    # Creates an order, saves in in the database and then returns said order.
    # If the order can't be created None is returned.
    def place_order(self, storage_unit_id, article_id, amount):
        try:
            order = Order.objects.create(ofArticle=article_id, toStorageUnit=storage_unit_id,
                                         amount=amount, expectedWait=self.get_expected_wait())
            order.save()
        except:
            return None

        return order

    # Helper function to get amount from centralstorage. returns amount or None if the article does not exist.
    def has_stock(self, article_id):
        central_storage_space = CentralStorageSpace.objects.filter(
            id=article_id).first()
        return central_storage_space.amount
