
from backend.core.IarticleModule import IarticleModule

from models import Article
from backend.__init__ import si 

@si.register(name='articleModule')
class articleModule(IarticleModule):
    def getArticleByLioId(self, lioId: str) -> Article:
        return Article.objects.get(lioId = lioId)