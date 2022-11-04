# from datetime import timedelta
from backend.coremodels.article import Article
from backend.coremodels.transaction import Transaction
# from backend.coremodels.Compartment import Compartment
# from backend.coremodels.Storage import Storage
# from backend.coremodels.transaction import Transaction
# from backend.coremodels.article import Article
# from backend.coremodels.qr_code import QRCode
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.storage_unit import StorageUnit
# from backend.coremodels.transaction import Transaction
# from ..coremodels.order import Order
from ..__init__ import dataAccessInjector as di


@di.register(name="StorageAccess")
class StorageAccess():
    '''Storage acces.'''
    def get_storage(self, id: str) -> StorageUnit:
        '''Returns storage from id.'''
        try:
            storage = StorageUnit.objects.get(id=id)
            return storage
        except Exception:
            return None

    def get_compartment_by_id(self, id: str) -> StorageSpace:
        '''Returns compartmend (storage space) from id.'''
        try:
            storage = StorageSpace.objects.get(id=id)
            return storage
        except Exception:
            return None

    # TODO: This does not seem to do what it is supposed to do. Please review
    def set_storage_amount(self, compartment_id: str, amount: int) -> int:
        '''Sets amount in compartment.'''
        try:
            new_amount = amount
            return StorageSpace.objects.update(**{amount: new_amount})
        except Exception:
            return None

    # TODO: This does not seem to do what it is supposed to do. Please review
    def get_compartment_stock(self,
                              compartment_id: str, article_id: str) -> int:
        '''Returns stock of campartmend using article id.'''
        try:
            stock = int(StorageSpace.objects.get(
                id=compartment_id, article=article_id).amount)
            return stock
        except Exception:
            return None

    def get_storage_stock(self, storage_id: str) -> dict:
        '''Returns storage stock using storage id.'''
        try:
            return "article: {} amount: {}".format(
                        StorageSpace.objects.get(id=storage_id).article,
                        StorageSpace.objects.get(id=storage_id).amount)
        except Exception:
            return None

    def get_all_storage_units(self) -> dict:
        '''Returns every storage unit.'''
        try:
            all_storage_units = StorageUnit.objects.all().values()
            return all_storage_units
        except Exception:
            return None

    def get_article_in_storage_space(self, storage_space_id: str) -> Article:
        '''Return article in storage space using storage space id.'''
        try:
            storage_space = StorageSpace.objects.get(id=storage_space_id)
            article = Article.objects.get(id=storage_space.article)
            return article
        except Exception:
            return None

    def search_article_in_storage(self, storage_unit_id: str,
                                  article_id: str) -> int:
        '''Search for article in storage using storage unit id
        and article id.'''
        try:
            storage_unit = StorageUnit.objects.get(id=storage_unit_id)
            article = Article.objects.get(lio_id=article_id)
            storage_space = StorageSpace.objects.get(storage_unit=storage_unit,
                                                     article=article)
            return storage_space.amount
        except Exception:
            return None

    def get_compartments_by_storage(self, storage_id: str) -> int:
        '''Return compartments from storage id.'''
        try:
            return StorageSpace.objects.filter(storage_unit=storage_id)
        except Exception:
            return None

    def get_all_transactions(self) -> dict:
        '''Return every transaction.'''
        try:
            all_transactions = Transaction.objects.all().values()
            return all_transactions
        except Exception:
            return None

    def get_transaction_by_storage(self, storage_id: str) -> int:
        '''Return transaction from storage id.'''
        try:
            return Transaction.objects.filter(storage_unit=storage_id)
        except Exception:
            return None

    def get_storage_by_costcenter(self, cost_center: str) -> StorageUnit:
        '''Return storage using cost-center.'''
        try:
            storage = StorageUnit.objects.get(cost_center=cost_center)
            return storage
        except Exception:
            return None

#  FR 9.4.1 och FR 9.4.2 ##

    def create_compartment(self, storage_id: str, placement: str,
                           qr_code) -> StorageSpace:
        '''Create new compartment.'''
        storage = StorageUnit.objects.filter(id=storage_id).first()
        # article = Article.objects.get(lio_id='123')
        try:
            compartment = StorageSpace(
                id=qr_code,
                storage_unit=storage,
                placement=placement,)
            compartment.save()
            return compartment
        except Exception:
            return None

    def get_compartment_by_qr(self, qr_code: str) -> StorageSpace:
        '''Get compartment using qr code.'''
        try:
            compartment = StorageSpace.objects.get(id=qr_code)
            return compartment
        except Exception:
            return None

# #  FR 9.4.1 och FR 9.4.2
