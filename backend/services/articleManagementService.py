from backend.services.IarticleManagementService import IarticleManagementService
from core import IarticleModule, articleModule
from core.models import Article

class articleManagementService(IarticleManagementService):

    def __init__(self, articleModule : IarticleModule):    
        self._articleModule = articleModule

    def getArticleByLioId(self, lioId: str) -> Article:
        return self._articleModule.getArticleByLioId(lioId)
