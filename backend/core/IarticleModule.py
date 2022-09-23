import abc
from models import Article

class IarticleModule(metaclass=abc.ABCMeta):
    def getArticleByLioId(self, lioId: str) -> Article:
        pass 
    def getAllArticles(self) -> list[Article]:
        pass
    def addArticle(self, lioId: str, name: str):
        pass