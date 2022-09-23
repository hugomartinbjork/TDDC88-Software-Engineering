from backend.services.IarticleManagementService import IarticleManagementService
from backend.models import Article
from backend.__init__ import si 

@si.register()
class articleManagementService(IarticleManagementService):
    @si.inject
    def __init__(self, _deps):  
        articleModule = _deps['articleModule']
        self._articleModule = articleModule()

    def getArticleByLioId(self, lioId: str) -> Article:
        return self._articleModule.getArticleByLioId(lioId)
