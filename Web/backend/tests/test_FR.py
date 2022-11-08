from django.test import TestCase
from backend.dataAccess.storageAccess import StorageAccess
from backend.dataAccess.articleAccess import ArticleAccess
from backend.coremodels.article import Article
from backend.coremodels.compartment import Compartment
from backend.coremodels.storage import Storage 
from backend.coremodels.qr_code import QRCode
from backend.services.articleManagementService import ArticleManagementService
from backend.services.storageManagementService import StorageManagementService
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
        self.article_to_search_for = Article.objects.create(lio_id ="1") #Database is populated and the object is stored so that we don't have to retrieve it again
        self.article_management_service : ArticleManagementService = ArticleManagementService() #An instance of the class to be tested is created and stored as a class variable for the test class. The "articleManagementService :" part specifies that the stored variable must be of type articlemanagementservice, this is not necessary, but makes the code more understandable
    def test_get_article_by_lio_id(self):
        test_search = self.article_management_service.get_article_by_lio_id("1")
        self.assertEqual(test_search, self.article_to_search_for)

# === Previously written like this, use for reference when rewriting other tests === #
# class ArticleIdentificationTest(TestCase):    
#      def setUp(self):                     
#          Article.objects.create(lio_id="1")         
            
#      def test_get_article_by_lio_id_function(self): 
#         article = Article.objects.get(lio_id="1")                  
#         self.assertEqual(articleManagementService.get_article_by_lio_id(self,"1"), article)        


# Testing FR4.6
class CompartmentCreationTest(TestCase):    
     def setUp(self):                     
         self.article_in_compartment = Article.objects.create(lio_id="1")
         self.article_management_service : ArticleManagementService = ArticleManagementService()
         self.storage_in_compartment = Storage.objects.create(id="1")
         self.storage_management_service : StorageManagementService = StorageManagementService()
         self.compartment = Compartment.objects.create(id="1", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"))
            
     def test_storageManagementService(self):
        test_search_compartment = self.storage_management_service.get_compartment_by_id(id="1")
        test_search_article = self.article_management_service.get_article_by_lio_id(lio_id="1")
        test_search_storage = self.storage_management_service.get_storage_by_id(id="1")
        self.assertEqual(test_search_compartment, self.compartment)
        self.assertEqual(self.compartment.article, test_search_article)
        self.assertEqual(self.compartment.storage, test_search_storage)


# Testing FR4.3
class FR4_3_Test(TestCase):
    def setUp(self):
        #create 2 storage spaces in the same storage units containing the same article
        self.article_in_compartment = Article.objects.create(lio_id="1")
        self.storage_in_compartment = Storage.objects.create(id="1")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.compartment = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="1"))
        self.compartment = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="1"))
       

        #create a second article in third storage space but in same storage unit
        self.article_in_compartment = Article.objects.create(lio_id="2")
        self.compartment = Compartment.objects.create(id="3", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="2"))

    def test_FR4_3(self):

        #Test that we can find/have the same article in different storage spaces in the same unit
        storage = self.storage_management_service.get_storage_by_id(id="1")
        compartment1 = self.storage_management_service.get_compartment_by_id(id="1")
        compartment2 = self.storage_management_service.get_compartment_by_id(id="2")
        article1 = self.article_management_service.get_article_by_lio_id("1")
        self.assertEqual(compartment1.article, article1)
        self.assertEqual(compartment2.article, article1)
        self.assertEqual(compartment1.storage, storage)
        self.assertEqual(compartment2.storage, storage)


# Testing FR6.2 "In each storage space, the system shall record the number of a certain article based on the LIO-number"
# Not sure if this actually tests what it is inteded to test. Manages to return a positive test result but second argument in assertEqual maybe should not be just a number?

class FR6_2_test(TestCase):

    def setUp(self):
        self.article_in_compartment = Article.objects.create(lio_id="1")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.storage_in_compartment = Storage.objects.create(id="1")
        self.storageSpace1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount=2)


    def test_FR6_2(self):
        test_article1 = self.article_management_service.get_article_by_lio_id("1")
        test_search_compartment = self.storage_management_service.get_compartment_by_id("1")
        self.assertEqual(test_search_compartment.amount, 2) 
        self.assertNotEqual(test_search_compartment.amount, 3) 

# class FR6_2_test(TestCase):

#     def setUp(self):
#         Article.objects.create(lio_id="1")
#         Storage.objects.create(id="1")
#         Compartment.objects.create(id="1", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"), amount = 2)
#         Compartment.objects.create(id="2", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"), amount = 4)

#     def test_FR6_2(self):
#         article1 = Article.objects.get(lio_id="1")
#         compartment1 = Compartment.objects.get(id="1")
#         compartment2 = Compartment.objects.get(id="2")
#         self.assertEqual(compartment1.amount, 2) 


#Testing FR1.2


# class FR1_2_test(TestCase):

#     def setUp(self):

#         UserInfo.objects.create(name)


#Testing FR8.9

class FR8_9_test(TestCase): 
    def setUp(self):
        self.article1 = Article.objects.create(lio_id="1")
        self.article2 = Article.objects.create(lio_id="2")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.Storage1 = Storage.objects.create(id="1")
        self.Storage2 = Storage.objects.create(id="2")
        self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount=2)
        self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="2"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"), amount=4)

    def test_FR8_9(self):
        test_article1 = self.storage_management_service.search_article_in_storage("1", "1")
        test_article2 = self.storage_management_service.search_article_in_storage("2", "2")
        self.assertEqual(test_article1, 2)
        self.assertEqual(test_article2, 4)
        self.assertNotEqual(test_article2, 5)

#Testing FR4.2
# Desc: The system shall connect a QR code with a Compartment in the Storage.

class FR4_2_test(TestCase): 
    def setUp(self):
        # self.storage1 = Storage.objects.create(id="1")
        # self.storage_management_service : StorageManagementService = StorageManagementService()
        # self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"))

        storage_access_stub = StorageAccess
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.storage = Storage(id="1")
        storage_access_stub.get_storage = MagicMock(return_value = self.storage)
        self.compartment = Compartment(id="1", storage = storage_access_stub.get_storage(id="1"))
        storage_access_stub.get_compartment_by_qr = MagicMock(return_value = self.compartment)

    def test_FR4_2(self):
        test_compartment = self.storage_management_service.get_compartment_by_qr(qr_code="1")
        self.assertEqual(self.compartment, test_compartment)
        self.assertEqual(self.storage, test_compartment.storage)