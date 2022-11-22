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
