from ..coremodels.centralStorageSpace import CentralStorageSpace
from ..__init__ import dataAccessInjector as di


@di.register(name="CentralStorageAccess")
class CentralStorageAccess():
    '''Central storage acces.'''

    def get_stock_by_article_id(self, article_id):
        '''Retrieve stock of and article with a specific id.'''
        try:
            central_storage_space = CentralStorageSpace.objects.filter(
                id=article_id).first()
            return central_storage_space.amount
        except Exception:
            return None

    def update_central_storage_quantity(article_id, quantity):
        '''Update central storage amount'''
        try:
            central_storage_space = CentralStorageSpace.objects.filter(
                id=article_id).first()
            central_storage_space.amount -= quantity
            central_storage_space.save()
            return central_storage_space.amount
        except Exception:
            return None