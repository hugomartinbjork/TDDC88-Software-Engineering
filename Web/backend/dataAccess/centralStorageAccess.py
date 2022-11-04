from ..coremodels.centralStorageSpace import CentralStorageSpace
from ..__init__ import dataAccessInjector as di


@di.register(name="centralStorageAccess")
class centralStorageAccess():
    def getStockByArticleId(self, article_id):
        central_storage_space = CentralStorageSpace.objects.filter(
                                                    id=article_id).first()
        return central_storage_space.amount
