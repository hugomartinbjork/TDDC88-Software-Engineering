from django.test import TestCase
from backend.coremodels.article import Article
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.storage_unit import StorageUnit 
from backend.services.articleManagementService import articleManagementService
from backend.services.storageManagementService import storageManagementService

class articleManagementServiceTest(TestCase):    
    def setUp(self):                     
         Article.objects.create(lioId="1")         
            
    def test_getArticleByLioId_function(self): 
        article = Article.objects.get(lioId="1")                  
        self.assertEqual(articleManagementService.getArticleByLioId(self,"1"), article)        

class storageManagementServiceTest(TestCase):    
    def setUp(self):                     
        Article.objects.create(lioId="1")
        StorageUnit.objects.create(id="1")
        StorageSpace.objects.create(id="1", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"))
            
    def test_getStorageUnitById(self):
        storageunit = StorageUnit.objects.get(id="1")
        self.assertEqual(storageManagementService.getStorageUnitById(self,"1"), storageunit)
    
    def test_getStorageSpaceById(self):
        storagespace = StorageSpace.objects.get(id="1")
        self.assertEqual(storageManagementService.getStorageSpaceById(self,"1"), storagespace)
    
    
    

    