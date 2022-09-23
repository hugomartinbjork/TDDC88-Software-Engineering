
from backend.core.IarticleModule import IarticleModule

from models import Article

class articleModule(IarticleModule):
    def getArticleByLioId(self, lioId: str) -> Article:
        return Article.objects.get(lioId = lioId)