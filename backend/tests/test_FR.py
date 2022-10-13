from django.test import TestCase
from backend.coremodels.article import *
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.storage_unit import StorageUnit 
from backend.services.articleManagementService import *
from backend.services.storageManagementService import storageManagementService

# Testing FR4.1
class ArticleIdentificationTest(TestCase):    
     def setUp(self):                     
         Article.objects.create(lioId="1")         
            
     def test_getArticleByLioId_function(self): 
        article = Article.objects.get(lioId="1")                  
        self.assertEqual(articleManagementService.getArticleByLioId(self,"1"), article)        

# Testing FR4.6
class StorageSpaceCreationTest(TestCase):    
     def setUp(self):                     
         Article.objects.create(lioId="1")
         StorageUnit.objects.create(id="1")
         StorageSpace.objects.create(id="1", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"))
            
     def test_storageManagementService(self):
        storageunit = StorageUnit.objects.get(id="1")
        storagespace = StorageSpace.objects.get(id="1")
        article1 = Article.objects.get(lioId="1")
        self.assertEqual(articleManagementService.getArticleByLioId(self,"1"), article1)
        self.assertEqual(storageManagementService.getStorageUnitById(self,"1"), storageunit)
        self.assertEqual(storageManagementService.getStorageSpaceById(self,"1"), storagespace)
        self.assertEqual(storagespace.article, article1)
        self.assertEqual(storagespace.storage_unit, storageunit) 


# Testing FR4.3
class FR4_3_Test(TestCase):
    def setUp(self):
        Article.objects.create(lioId="1")
        StorageUnit.objects.create(id="1")
        StorageSpace.objects.create(id="1", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"))
        StorageSpace.objects.create(id="2", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"))

    def test_FR4_3(self):
        storageunit = StorageUnit.objects.get(id="1")
        storagespace1 = StorageSpace.objects.get(id="1")
        storagespace2 = StorageSpace.objects.get(id="2")
        article1 = Article.objects.get(lioId="1")
        self.assertEqual(storagespace1.article, article1)
        self.assertEqual(storagespace2.article, article1)
        self.assertEqual(storagespace1.storage_unit, storageunit)
        self.assertEqual(storagespace2.storage_unit, storageunit)







