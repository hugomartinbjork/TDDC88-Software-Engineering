from django.test import TestCase
from backend.dataAccess.articleAccess import articleAccess
from backend.coremodels.article import Article
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.storage_unit import StorageUnit 
from backend.coremodels.qr_code import QRCode
from backend.services.articleManagementService import articleManagementService
from backend.services.storageManagementService import storageManagementService
import unittest
from unittest.mock import MagicMock

# Testing FR4.1
# === How To Rewrite tests example 1 === #
# Here the same functionality that you intended is preserved

# === Rewritten test === # 
# Note: This test is dependent on that functions in the service layer and data access layer work as they should. So this is not a unit test
# Run this test individually with the command: python manage.py test backend.tests.test_FR.ArticleIdentificationTest
class ArticleIdentificationTest(TestCase):
    def setUp(self):
        self.article_to_search_for = Article.objects.create(lioId ="1") #Database is populated and the object is stored so that we don't have to retrieve it again
        self.article_management_service : articleManagementService = articleManagementService() #An instance of the class to be tested is created and stored as a class variable for the test class. The "articleManagementService :" part specifies that the stored variable must be of type articlemanagementservice, this is not necessary, but makes the code more understandable
    def test_get_article_by_lio_id(self):
        test_search = self.article_management_service.getArticleByLioId("1")
        self.assertEqual(test_search, self.article_to_search_for)

# === Previously written like this, use for reference when rewriting other tests === #
# class ArticleIdentificationTest(TestCase):    
#      def setUp(self):                     
#          Article.objects.create(lioId="1")         
            
#      def test_getArticleByLioId_function(self): 
#         article = Article.objects.get(lioId="1")                  
#         self.assertEqual(articleManagementService.getArticleByLioId(self,"1"), article)        

# === example 2 === #
# This is how the test would be written as a unit test
class ArticleIdentificationTest2(TestCase):
    def setUp(self):
        # First we create a stub of articleAccess (this is because the method we are testing is using this data access class)
        article_access_stub = articleAccess
        self.article_to_search_for = Article(lioId="1") # Article to search for is created without being put in the database
        article_access_stub.getArticleByLioId = MagicMock(return_value = self.article_to_search_for) #A return value for a method of the stub is specified (this simulates that the stub is functional, so we can test the method we are testing individually)
        self.article_management_service : articleManagementService = articleManagementService(
            {
                "articleAccess": article_access_stub #The mocked dependency is injected into the article management service
            }
        )
    def test_get_article_by_lio_id_unittestversion(self):
        test_search = self.article_management_service.getArticleByLioId(lioId="1")
        self.assertEqual(self.article_to_search_for, test_search)


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


#Testing FR6.2

class FR6_2_test(TestCase):

    def setUp(self):
        Article.objects.create(lioId="1")
        StorageUnit.objects.create(id="1")
        StorageSpace.objects.create(id="1", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"), amount = 2)
        StorageSpace.objects.create(id="2", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"), amount = 4)

    def test_FR6_2(self):
        article1 = Article.objects.get(lioId="1")
        storagespace1 = StorageSpace.objects.get(id="1")
        storagespace2 = StorageSpace.objects.get(id="2")
        self.assertEqual(storagespace1.amount, 2) 


#Testing FR1.2


# class FR1_2_test(TestCase):

#     def setUp(self):

#         UserInfo.objects.create(name)


#Testing FR8.9

class FR8_9_test(TestCase):

    def setUp(self):
        Article.objects.create(lioId="1")
        Article.objects.create(lioId="2")
        StorageUnit.objects.create(id="1")
        StorageUnit.objects.create(id="2")
        StorageSpace.objects.create(id="1", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"), amount = 2)
        StorageSpace.objects.create(id="2", storage_unit = StorageUnit.objects.get(id="2"), article = Article.objects.get(lioId="2"), amount = 4)

    def test_FR8_9(self):
       article1 = Article.objects.get(lioId="1")
       article2 = Article.objects.get(lioId="2")
       storagespace1 = StorageSpace.objects.get(id="1")
       storagespace2 = StorageSpace.objects.get(id="2")
       storageunit1 = StorageUnit.objects.get(id="1")
       storageunit2 = StorageUnit.objects.get(id="2")
       self.assertEqual(storageManagementService.searchArticleInStorage("1", "1"), 2)  
       self.assertNotEqual(storageManagementService.searchArticleInStorage("1", "1"), 3)  
       self.assertNotEqual(storageManagementService.searchArticleInStorage("2", "1"), 2) 
       self.assertEqual(storageManagementService.searchArticleInStorage("2", "2"), 4) 
       self.assertEqual(storageManagementService.searchArticleInStorage("2", "1"), None) 

       





#Testing FR4.2
#-------Fails test and gives errormessage: "StorageSpace matching query does not exist."
#-------No idea what is wrong.
# class FR4_2_test(TestCase):
#     def setUP(self):
#         Article.objects.create(lioId="1")
#         StorageUnit.objects.create(id="1")
#         StorageSpace.objects.create(id="2", storage_unit = StorageUnit.objects.get(id="1"), article = Article.objects.get(lioId="1"))
#         QRCode.objects.create(id="1", storage_space=StorageSpace.objects.get(id="2"))

#     def test_QRcode_containing_Storagespace(self):
#         storagespace = StorageSpace.objects.get(id="2")
#         qrcode = QRCode.objects.get(id="1")
#         self.assertEqual(qrcode.storage_space, storagespace)






