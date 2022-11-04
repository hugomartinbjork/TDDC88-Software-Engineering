from django.test import TestCase
from unittest.mock import MagicMock, Mock
from ..services.orderServices import OrderService
from ..services.storageManagementService import storageManagementService
from ..dataAccess.centralStorageAccess import centralStorageAccess
from ..dataAccess.storageAccess import storageAccess
from ..dataAccess.userAccess import userAccess
from .testObjectFactory.dependencyFactory import DependencyFactory
from .testObjectFactory.coremodelFactory import create_article, create_storageunit, create_transaction, create_costcenter
from datetime import datetime
import datetime

dependency_factory = DependencyFactory()


class OrderServiceCalculateEtaTestCase(TestCase):
    def setUp(self) -> None:
        central_storage_mock = centralStorageAccess
        # When checking the article stock, the stub will return 100 as the amount of the article found
        # in the central storage. 
        central_storage_mock.getStockByArticleId = MagicMock(return_value = 100)
        # dependency factory autocompletes with the rest of the   
        # dependencies that are not used for this specific test
        mocked_dependencies = dependency_factory.complete_dependency_dictionary({"centralStorageAccess" : central_storage_mock})

        # An instance of OrderService is created with the mocked dependencies
        # inserted as the _deps argument, This requires the OrderService constructor
        # to take in a *args argument to which the real _deps are pushed over to
        self.order_service = OrderService(mocked_dependencies)
    
    def test_order_less_than_in_stock(self):
        calculated_wait_time = self.order_service.calculate_expected_wait("123", 10)
        # When we have enough in the central storage, 
        # the wait time is supposed to be 2 days
        self.assertEqual(calculated_wait_time, 2)
     
    def test_order_more_than_in_stock(self):
        calculated_wait_time = self.order_service.calculate_expected_wait("123", 101)
        #When we don't have enough in the central storage, the wait time is 14 days
        self.assertEqual(calculated_wait_time, 14)

class StorageServiceEconomyTest(TestCase):
    def setUp(self):
        transacted_article = create_article(price=10)
        cost_center = create_costcenter(id="123")
        storage_unit = create_storageunit(costCenter=cost_center)
        transaction_time = datetime.date(2000,7,15)
        transaction_list = []
        transaction_list.append(create_transaction(article=transacted_article, amount=2, operation=2, storage_unit=storage_unit, time_of_transaction=transaction_time))
        transaction_list.append(create_transaction(article=transacted_article, amount=2, operation=1, storage_unit=storage_unit, time_of_transaction=transaction_time))
        transaction_list.append(create_transaction(article=transacted_article, amount=4, operation=1, storage_unit=storage_unit, time_of_transaction=transaction_time))
        storage_access_mock = storageAccess
        storage_access_mock.get_transaction_by_storage = MagicMock(return_value=transaction_list)
        user_access_mock = userAccess
        user_access_mock.get_user_cost_center = MagicMock(return_value=cost_center)
        mocked_dependencies = dependency_factory.complete_dependency_dictionary(
            {"storageAccess" : storage_access_mock, "userAccess" : user_access_mock}
        )
        self.storage_service = storageManagementService(mocked_dependencies)
    
    def test_sum_transactions_and_withdrawals(self):
        economyresult = self.storage_service.getStorageCost("","2000-06-15","2000-08-15")
        self.assertAlmostEquals(economyresult,40)