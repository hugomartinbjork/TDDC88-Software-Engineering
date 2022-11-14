
# Testing FR 1.1 The system shall support three different user types: medical employee, inventory employee, and MIV employee.
class SupportDifferentUsers(TestCase):
    def setUp(self):
        #create 3 mock users and info about them
        self.user_service : UserService = UserService()
        cost_center1 = CostCenter.objects.create(id="123")
        self.user1 = User.objects.create(username="MIV-Employee", password="TDDC88")
        self.user_info1 = UserInfo.objects.create(user = self.user1, cost_center = cost_center1)
        self.user2 = User.objects.create(username="Medical Employee", password="TDDC88")
        self.user_info2 = UserInfo.objects.create(user = self.user2, cost_center = cost_center1)
        self.user3 = User.objects.create(username="Inventory Employee", password="TDDC88")
        self.user_info3 = UserInfo.objects.create(user = self.user3, cost_center = cost_center1)
    def test_setup_users(self):
        #By getting info from database we can verify that we it was created.
        test_user_creation1 = self.user_service.get_user_info(self.user1)
        self.assertEqual(test_user_creation1, self.user_info1)
        test_user_creation2 = self.user_service.get_user_info(self.user2)
        self.assertEqual(test_user_creation2, self.user_info2)
        test_user_creation3 = self.user_service.get_user_info(self.user3)
        self.assertEqual(test_user_creation3, self.user_info3)