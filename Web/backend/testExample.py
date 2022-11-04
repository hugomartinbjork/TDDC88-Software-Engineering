from django.test import TestCase
from unittest.mock import MagicMock, Mock
from .services.orderServices import OrderService
from .dataAccess.centralStorageAccess import CentralStorageAccess

class Order_service_calculate_eta_test_case(TestCase):
    def setUp(self) -> None:
        central_storage_mock = CentralStorageAccess
        #When checking the article stock, the stub will return 100 as the amount of the article found
        #in the central storage. 
        central_storage_mock.get_stock_by_article_id = MagicMock(return_value = 100)

        #These should be the data access dependencies that the tested service is using
        mocked_dependencies = {
            "CentralStorageAccess" : central_storage_mock,
            "OrderAccess" : randomCallable,
        }
        # An instance of OrderService is created with the mocked dependencies
        # inserted as the _deps argument, This requires the OrderService constructor
        # to take in a *args argument to which the real _deps are pushed over to
        self.order_service = OrderService(mocked_dependencies)
    
    def test_order_less_than_in_stock(self):
        calculated_wait_time = self.order_service.calculate_expected_wait("123", 10)
        #When we have enough in the central storage, the wait time is supposed to be 2 days
        self.assertEqual(calculated_wait_time, 2)
     
    def test_order_more_than_in_stock(self):
        calculated_wait_time = self.order_service.calculate_expected_wait("123", 101)
        #When we don't have enough in the central storage, the wait time is 14 days
        self.assertEqual(calculated_wait_time, 14)



#This class is sent in as a substitute for dependencies that won't be used for the test
class randomCallable():
   pass