from django.test import TestCase
from backend.dataAccess.storageAccess import StorageAccess
from backend.dataAccess.articleAccess import ArticleAccess
from backend.coremodels.article import Article
from backend.coremodels.group import GroupInfo
from backend.coremodels.compartment import Compartment
from backend.coremodels.cost_center import CostCenter
from backend.coremodels.storage import Storage 
from backend.coremodels.user_info import UserInfo
from backend.coremodels.order import Order
from backend.coremodels.ordered_article import OrderedArticle
from backend.services.articleManagementService import ArticleManagementService
from backend.services.storageManagementService import StorageManagementService
from backend.services.userService import UserService
from backend.services.orderManagementService import OrderManagementService
from backend.services.orderServices import OrderService
from backend.coremodels.transaction import Transaction
import unittest
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from unittest.mock import MagicMock
from unittest.mock import MagicMock, Mock
from ..services.orderServices import OrderService
from ..dataAccess.centralStorageAccess import CentralStorageAccess
from ..dataAccess.storageAccess import StorageAccess
from ..dataAccess.userAccess import UserAccess
from ..dataAccess.orderAccess import OrderAccess
from .testObjectFactory.dependencyFactory import DependencyFactory
from .testObjectFactory.coremodelFactory import create_article
from .testObjectFactory.coremodelFactory import create_storage
from .testObjectFactory.coremodelFactory import create_transaction
from .testObjectFactory.coremodelFactory import create_costcenter
from datetime import datetime
import datetime
dependency_factory = DependencyFactory()

# Testing FR 1.1 The system shall support three different user types: medical employee, inventory employee, and MIV employee.
class SupportDifferentUsers(TestCase):
    def setUp(self):
        #create 3 mock users and info about them
        self.user_service : UserService = UserService()
        cost_center1 = CostCenter.objects.create(id="123")
        self.user1 = User.objects.create(username="MIV-Employee", password="TDDC88")
        self.user_info1 = UserInfo.objects.create(user = self.user1)
        self.user2 = User.objects.create(username="Medical Employee", password="TDDC88")
        self.user_info2 = UserInfo.objects.create(user = self.user2)
        self.user3 = User.objects.create(username="Inventory Employee", password="TDDC88")
        self.user_info3 = UserInfo.objects.create(user = self.user3)
        self.user_info1.cost_center.add(cost_center1)
        self.user_info2.cost_center.add(cost_center1)
        self.user_info3.cost_center.add(cost_center1)

    def test_setup_users(self):
        #By getting info from database we can verify that we it was created.
        test_user_creation1 = self.user_service.get_user_info(self.user1)
        self.assertEqual(test_user_creation1, self.user_info1)
        test_user_creation2 = self.user_service.get_user_info(self.user2)
        self.assertEqual(test_user_creation2, self.user_info2)
        test_user_creation3 = self.user_service.get_user_info(self.user3)
        self.assertEqual(test_user_creation3, self.user_info3)

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
        test_search_compartment = self.storage_management_service.get_compartment_by_qr("1")
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
        compartment1 = self.storage_management_service.get_compartment_by_qr("1")
        compartment2 = self.storage_management_service.get_compartment_by_qr("2")
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
        test_search_compartment = self.storage_management_service.get_compartment_by_qr("1")
        self.assertEqual(test_search_compartment.amount, 2) 
        self.assertNotEqual(test_search_compartment.amount, 3) 


#Testing FR8.9
# Desc: The system shall allow users to choose which storage unit to search within.
# Sytemtest later instead??

# class FR8_9_test(TestCase): 
#     def setUp(self):
#         self.article1 = Article.objects.create(lio_id="1")
#         self.article2 = Article.objects.create(lio_id="2")
#         self.article_management_service : ArticleManagementService = ArticleManagementService()
#         self.storage_management_service : StorageManagementService = StorageManagementService()
#         self.Storage1 = Storage.objects.create(id="1")
#         self.Storage2 = Storage.objects.create(id="2")
#         self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount=2)
#         self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="2"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"), amount=4)

#     def test_FR8_9(self):
#         test_article1 = self.storage_management_service.search_article_in_storage("1", "1")
#         test_article2 = self.storage_management_service.search_article_in_storage("2", "2")
#         self.assertEqual(test_article1, 2)
#         self.assertEqual(test_article2, 4)
#         self.assertNotEqual(test_article2, 5)

# Testing 4.2
# Desc: The system shall connect a QR code with a Compartment in the Storage.

class FR4_2_test(TestCase): 
    def setUp(self):
        # self.storage = Storage.objects.create(id="1")
        # self.storage_management_service : StorageManagementService = StorageManagementService()
        # self.compartment = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"))
        self.get_storage = StorageAccess.get_storage
        self.get_compartment_by_qr = StorageAccess.get_compartment_by_qr
        
        storage_access_mock = StorageAccess
        self.storage = Storage(id="1")
        storage_access_mock.get_storage = MagicMock(return_value = self.storage)
        self.compartment = Compartment(id="1", storage = storage_access_mock.get_storage(id="1"))
        storage_access_mock.get_compartment_by_qr = MagicMock(return_value = self.compartment)

        mocked_dependencies = (
            dependency_factory.complete_dependency_dictionary(
                {"StorageAccess": storage_access_mock}))

        self.storage_management_service = StorageManagementService(mocked_dependencies)

    def tearDown(self) :
        StorageAccess.get_storage = self.get_storage
        StorageAccess.get_compartment_by_qr = self.get_compartment_by_qr

    def test_FR4_2(self):
        test_compartment = self.storage_management_service.get_compartment_by_qr(qr_code="1")
        self.assertEqual(self.compartment, test_compartment)
        self.assertEqual(self.storage, test_compartment.storage)
       


#Testing transactions, user connected to cost centers, initiated cost centers, storage links to cost center and vice versa
#and test of fr9.7 that all transaction of a user should be stored and accesasable
#tests fr 5.9 as well
# class test_transaction_takeout_and_withdrawal(TestCase): 
#     def setUp(self):
#         #create 2 articles witha certain price and a cost center
#         self.article1 = Article.objects.create(lio_id="1", price = 10)
#         self.article2 = Article.objects.create(lio_id="2", price = 30)
#         self.article_management_service : ArticleManagementService = ArticleManagementService()
#         self.storage_management_service : StorageManagementService = StorageManagementService()
#         self.order_service : UserService = UserService()
#         cost_center1 = CostCenter.objects.create(id="123")
#         self.Storage1 = Storage.objects.create(id="99", cost_center = cost_center1)
        
#         #create 2 mock users
#         self.user1 = User.objects.create(username="userOne", password="TDDC88")
#         self.use_info1 = UserInfo.objects.create(user = self.user1, cost_center = cost_center1)
#         self.user2 = User.objects.create(username="userTwo", password="TDDC88")
#         self.use_info2 = UserInfo.objects.create(user = self.user2, cost_center = cost_center1)

#         self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"))
#         self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"))

#         #transactions in 2000
#         #takeout article 1; amount =2 i.e cost +20
#         self.transaction1 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="1"),
#                                                     amount=2, operation=1, by_user = self.user1,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2000, 2, 15))
#         #takeout article 2; amount =2 i.e. cost +60
#         self.transaction2 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="2"),
#                                                     amount=2, operation=1, by_user = self.user1,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2000, 5, 15))   
#         #takeout article 1; amount =1 i.e. +10
#         self.transaction3 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="1"),
#                                                     amount=1, operation=1, by_user = self.user2,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2000, 9, 15))   

#         #transactions 2021    
#         #replenish 12 of article 1 i.e. cost = -120                                 
#         self.transaction4 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="1"),
#                                                     amount=12, operation=3, by_user = self.user1,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2001, 8, 15))

#         #takeout article 2, amount 5 i.e. cost =+150
#         self.transaction5 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="2"),
#                                                     amount=5, operation=1, by_user = self.user1,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2001, 8, 23))

#         #return article 2, amount 4 i.e. cost =-120
#         self.transaction6 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="2"),
#                                                     amount=4, operation=2, by_user = self.user1,
#                                                     storage= self.storage_management_service.get_storage_by_id(id="99"),
#                                                     time_of_transaction=
#                                                     datetime.date(2001, 8, 25))

       


# #     def test_FR11_1(self):
# #         #testtransaction cost for the time period where we had 3 takeouts (totalt of 3 takesouts of article 1 and 2 of aticle 2 = total cost of 90)
# #         storage1_cost = self.storage_management_service.get_storage_cost("99", "2000-01-07","2000-12-07")
# #         self.assertEqual(storage1_cost, 90)

# #         #test time period of year 2001
# #         storage2_cost = self.storage_management_service.get_storage_cost("99", "2001-01-07","2001-12-07")
# #         self.assertEqual(storage2_cost, 30) #bör vara 30!! ändrade bara tillfälligt för att det ska funka. 

#         #test 5.9  For each transaction, the system shall register the LIO-number of the article taken out of storage, 
#         # who performed the transaction, from which storage unit the transaction was performed, 
#         # the time of the transaction and the number of articles taken from the storage unit.
#         self.assertEqual(self.transaction1.article.lio_id, self.article1.lio_id)
#         self.assertEqual(self.transaction1.by_user, self.user1)
#         self.assertEqual(self.transaction1.storage, self.Storage1)
#         self.assertEqual(self.transaction1.amount, 2)
       

        
#         #transaction_user1 = self.order_service.get_all_transactions_by_user(self.user1)  
#         #self.assertEqual(transaction_user1, [self.transaction1, self.transaction2, self.transaction4, self.transaction5, self.transaction6])    


class FR11_1_Test(TestCase): 
    def setUp(self):
        #create 2 articles witha certain price and a cost center
        self.article1 = Article.objects.create(lio_id="1", price = 10)
        self.article2 = Article.objects.create(lio_id="2", price = 30)
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        cost_center1 = CostCenter.objects.create(id="123")
        self.Storage1 = Storage.objects.create(id="99", cost_center = cost_center1)
        self.Storage2 = Storage.objects.create(id="34", cost_center = cost_center1)
        
        #add compartments in storage 1 with articles and a certain amount of articles
        self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount = 2)
        self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"), amount = 3)                                    
        #add compartments in storage 2 with articles and a certain amount of articles
        self.compartment2 = Compartment.objects.create(id="3", storage = self.storage_management_service.get_storage_by_id(id="34"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"), amount = 3)        
    def test_FR11_1(self):
        storage1_value = self.storage_management_service.get_storage_value("99")
        storage2_value = self.storage_management_service.get_storage_value("34")
        self.assertEqual(storage1_value, 110)
        self.assertEqual(storage2_value, 90)
       


# Testing FR 5.7 
# Desc: The system shall display the estimated time of arrival of articles not in stock
# OBS: Tests the functionality of returning the estimated time of arrival, not that it actually displays it. 
class FR_5_7(TestCase):
    '''Test case to calculate estimated time to arrival.'''
    def setUp(self):
        self.get_stock_by_article_id = CentralStorageAccess.get_stock_by_article_id
        central_storage_mock = CentralStorageAccess

        central_storage_mock.get_stock_by_article_id = MagicMock(
                                                return_value=100)

        mocked_dependencies = (
            dependency_factory.complete_dependency_dictionary(
                {"CentralStorageAccess": central_storage_mock}))

        self.order_service = OrderService(mocked_dependencies)

    def tearDown(self):
        CentralStorageAccess.get_stock_by_article_id = self.get_stock_by_article_id

    def test_order_less_than_in_stock(self):
        '''Test.'''
        calculated_wait_time = (
            self.order_service.calculate_expected_wait("123", 10))
        # When we have enough in the central storage,
        # the wait time is supposed to be 2 days
        self.assertEqual(calculated_wait_time, 2)

    def test_order_more_than_in_stock(self):
        '''Test.'''
        calculated_wait_time = (
            self.order_service.calculate_expected_wait("123", 101))
        # When we don't have enough in the central
        # storage, the wait time is 14 days
        self.assertEqual(calculated_wait_time, 14)

# class FR1_2_Test(TestCase): 
#     def setUp(self):

#         #create User service instance & a cost center
#         self.order_service : UserService = UserService()
#         cost_center1 = CostCenter.objects.create(id="1234")
#         cost_center2 = CostCenter.objects.create(id="12345")
       
        
#         #create 2 mock users with 2 different roles

#         #2 roles one "manager-role" & one "nurse-role"
#         self.role1 = Group.objects.create(name = "manager")
#         self.role2 = Group.objects.create(name = "nurse")

#         #create one user with cost-center with id "1234" and the role as "manager"
#         self.user1 = User.objects.create(username="userOne", password="TDDC88")
#         self.use_info1 = UserInfo.objects.create(user = self.user1, group = self.role1)
#         self.use_info1.cost_center.add(cost_center1)

#         #create one user with cost-center with id "12345" and the role as "nurse"
#         self.user2 = User.objects.create(username="userTwo", password="TDDC88")
#         self.use_info2 = UserInfo.objects.create(user = self.user2, group = self.role2)
#         self.use_info2.cost_center.add(cost_center2)
          
#     def test_FR1_2(self):
#         test_user1 = self.use_info1
#         test_user2 = self.use_info2
#         #test that a user have a  a role, username, password, cost-center
#         self.assertEqual(self.use_info1.group, self.role1)
#         self.assertEqual(self.use_info1.user.username, "userOne")
#         self.assertNotEqual(self.use_info1.user.username, "userTwo")
#         self.assertEqual(self.use_info1.user.password, "TDDC88")
#         self.assertNotEqual(self.use_info1.user.password, "TDDC888")
#         self.assertEqual(self.use_info1.cost_center, test_user1)
#         self.assertNotEqual(self.use_info1.cost_center, test_user2)


#Testing API endpoint requirement: Get order by ID (Task 15.3.1.)
#Also testing "API endpoint requirement: Get orders. (Not in our SRS, new functionality)"
class API_GetOrderByID(TestCase):

    def setUp(self):
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.order_management_service : OrderManagementService = OrderManagementService()
        self.order_services : OrderService = OrderService()


        #create instances of article to order
        self.article1 = Article.objects.create(lio_id="1", name = "Plasthandskar", input = "ml", output = "ml", output_per_input = 1)
        self.article2 = Article.objects.create(lio_id="2", name = "Mask", input = "pieces", output = "pieces", output_per_input = 1)
        #create a storage
        self.storage_in_compartment = Storage.objects.create(id="Forrad 1")

        #create an order1
        self.order1 = Order.objects.create(id="77", to_storage = self.storage_management_service.get_storage_by_id(id="Forrad 1"), estimated_delivery_date = "2022-11-19 23:16:31.285209+00:00", 
        order_date ="2022-11-17 23:16:31.286527+00:00", order_state = "delivered")

        #create an order2
        self.order2 = Order.objects.create(id="88", to_storage = self.storage_management_service.get_storage_by_id(id="Forrad 1"), estimated_delivery_date = "2022-11-19 23:16:31.285209+00:00", 
        order_date ="2022-08-17 23:16:31.286527+00:00", order_state = "delivered")

        

        #create a ordered article for "plaskhanskar" connected to our "order1"
        self.ordered_article1 = OrderedArticle.objects.create(id="25", quantity = 3, article = self.article1, order = self.order1, unit = "input")

        #create a ordered article for "plaskhanskar" connected to our "order2"
        self.ordered_article1 = OrderedArticle.objects.create(id="26", quantity = 3, article = self.article1, order = self.order2, unit = "input")
        #create a ordered article for "mask" connected to our "order2"
        self.ordered_article1 = OrderedArticle.objects.create(id="27", quantity = 3, article = self.article2, order = self.order2, unit = "input")

    def test_get_order_by_ID(self):
        order77 = self.order1
        order88 = self.order2

        storage1 = self.storage_in_compartment

        #test we can get the order we want and not the wrong
        self.assertEqual(order77, self.order_management_service.get_order_by_id("77"))
        self.assertEqual(order77.to_storage, storage1)

        #test we can can an order with 2 ordered articles
        self.assertEqual(order88, self.order_management_service.get_order_by_id("88"))

        #test that orders are differantiated from each other
        self.assertNotEqual(order88, self.order_management_service.get_order_by_id("77"))

        #test api endpoint: "API endpoint requirement: Get orders. (Not in our SRS, new functionality)"
        

        orders = self.order_services.get_orders()
        #ordered_articles = self.order_services.get_all_ordered_articles()
        
        self.assertEqual(list(orders),[self.order1,self.order2])
    
        

