#Testing transactions, user connected to cost centers, initiated cost centers, storage links to cost center and vice versa
class tes_transaction_takeout_and_withdrawal(TestCase): 
    def setUp(self):
        #create 2 articles witha certain price and a cost center
        self.article1 = Article.objects.create(lio_id="1", price = 10)
        self.article2 = Article.objects.create(lio_id="2", price = 30)
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        cost_center1 = CostCenter.objects.create(id="123")
        self.Storage1 = Storage.objects.create(id="99", cost_center = cost_center1)
        
        #create 2 mock users
        self.user1 = User.objects.create(username="userOne", password="TDDC88")
        self.use_info1 = UserInfo.objects.create(user = self.user1, cost_center = cost_center1)
        self.user2 = User.objects.create(username="userTwo", password="TDDC88")
        self.use_info2 = UserInfo.objects.create(user = self.user2, cost_center = cost_center1)

        self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"))
        self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="99"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"))
        self.transaction1 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="1"),
                                                    amount=2, operation=1, by_user = self.user1,
                                                    storage= self.storage_management_service.get_storage_by_id(id="99"),
                                                    time_of_transaction=
                                                    datetime.date(2000, 2, 15))
        self.transaction2 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="2"),
                                                    amount=2, operation=1, by_user = self.user1,
                                                    storage= self.storage_management_service.get_storage_by_id(id="99"),
                                                    time_of_transaction=
                                                    datetime.date(2000, 5, 15))   
        self.transaction1 = Transaction.objects.create(article=self.article_management_service.get_article_by_lio_id(lio_id="1"),
                                                    amount=1, operation=1, by_user = self.user2,
                                                    storage= self.storage_management_service.get_storage_by_id(id="99"),
                                                    time_of_transaction=
                                                    datetime.date(2000, 9, 15))                                        
        
    def test_FR11_1(self):
        storage1_cost = self.storage_management_service.get_storage_cost("99", "2000-01-07","2000-12-07")
        #storage2_cost = self.storage_management_service.get_storage_cost("2", "2022-10-7","2022-12-7")
        self.assertEqual(storage1_cost, 30)
        #self.assertEqual(storage2_cost, 120)


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
       