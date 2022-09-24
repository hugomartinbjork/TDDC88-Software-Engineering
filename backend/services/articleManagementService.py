from backend.services.IarticleManagementService import IarticleManagementService
from backend.coremodels.article import Article
from backend.__init__ import si 

@si.register(name = 'articleManagementService')
class articleManagementService(IarticleManagementService):
    def getArticleByLioId(self, lioId: str) -> Article:
        try:
            article = Article.objects.get(lioId=lioId)  
            return article
        except:
            return None