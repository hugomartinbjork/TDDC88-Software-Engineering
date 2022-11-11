from django.test import TestCase
from backend.tests.testObjectFactory.dependencyFactory import DependencyFactory
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
from unittest.mock import MagicMock, Mock
from ..services.orderServices import OrderService
from ..dataAccess.centralStorageAccess import CentralStorageAccess
from ..dataAccess.storageAccess import StorageAccess
from ..dataAccess.userAccess import UserAccess
from ..dataAccess.orderAccess import OrderAccess
# from .testObjectFactory.dependencyFactory import DependencyFactory
# from .testObjectFactory.coremodelFactory import create_article
# from .testObjectFactory.coremodelFactory import create_storage
# from .testObjectFactory.coremodelFactory import create_transaction
# from .testObjectFactory.coremodelFactory import create_costcenter
# from datetime import datetime
# import datetime

# Testing FR 5.7 
# Desc: The system shall display the estimated time of arrival of articles not in stock


# #Testing FR4.4
# # Desc: An article shall consist of an article group, article description, alternative article description, LIO-number, article text,
# #       supplier, supplier article number, order procedure, picture link, standard cost, minimal order quantity, 
# #       refill unit, take-out unit, price, name, alternative names, and alternative articles as well as supplier and the order number from the supplier.

# #       It is not exactly the same as the database schema or FR, but it is the same as the API-documentation which it should be. 
# #       The class ArticleAlternativesTo is not implemented because it is handled by the article having a relation to itself. 
# #       Sanitation_level is now named Z41 which the API-documentation states. You can find the changes in article.py as well as 
# #       a getter for the article in views.py under "class article(View)". Message me if you have any questions. The group-attribute is being worked on


# class FR4_4_test(TestCase): 
#     def setUp(self):
#         self.article = Article.objects.create(id="1")
#         self.article_management_service : ArticleManagementService = ArticleManagementService()
#         self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"))

#     def test_FR4_4(self):
#         test_compartment = self.storage_management_service.get_compartment_by_qr(qr_code="1")
#         self.assertEqual(self.compartment, test_compartment)
#         self.assertEqual(self.storage, test_compartment.storage)