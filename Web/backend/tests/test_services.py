from django.test import TestCase
from backend.dataAccess.articleAccess import ArticleAccess
from backend.coremodels.article import Article
from backend.coremodels.compartment import Compartment
from backend.coremodels.storage import Storage 
from backend.coremodels.qr_code import QRCode
from backend.services.articleManagementService import ArticleManagementService
from backend.services.storageManagementService import StorageManagementService
import unittest
from unittest.mock import MagicMock

class ArticleManagementServiceTest(TestCase):
    def setUp(self):
        # First we create a stub of articleAccess (this is because the method we are testing is using this data access class)
        article_access_stub = ArticleAccess
        self.article_to_search_for = Article(lio_id="1") # Article to search for is created without being put in the database
        article_access_stub.get_article_by_lio_id = MagicMock(return_value = self.article_to_search_for) #A return value for a method of the stub is specified (this simulates that the stub is functional, so we can test the method we are testing individually)
        self.article_management_service : ArticleManagementService = ArticleManagementService(
            {
                "ArticleAccess": article_access_stub #The mocked dependency is injected into the article management service
            }   # NOTE: for this to work it is important that the class we are injecting into, takes *args as an input argument for the constructor (__init__) 
        )
    def test_get_article_by_lio_id_unittestversion(self):
        test_search = self.article_management_service.get_article_by_lio_id(lio_id="1")
        self.assertEqual(self.article_to_search_for, test_search)    

# class storageManagementServiceTest(TestCase):    
#     def setUp(self):                     
#         Article.objects.create(lioId="1")
#         storage.objects.create(id="1")
#         Storage.objects.create(id="1", storage_unit = Storage.objects.get(id="1"), article = Article.objects.get(lioId="1"))
            
#     # def test_getStorageById(self):
#     #     storage = Storage.objects.get(id="1")
#     #     self.assertEqual(storageManagementService.getStorageById(self,"1"), storage)
    
#     # def test_getStorageById(self):
#     #     compartment = Storage.objects.get(id="1")
#     #     self.assertEqual(storageManagementService.getStorageById(self,"1"), compartment)
    
    
    

    