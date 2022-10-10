from backend.coremodels.article import Article

class IarticleManagementService():
    def getArticleByLioId(lioId: str) -> Article:
        pass