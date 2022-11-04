# from requests import request
# from Web.backend.views.views import Compartment
from backend.dataAccess.orderAccess import OrderAccess
from backend.dataAccess.storageAccess import StorageAccess
from backend.dataAccess.userAccess import UserAccess
from backend.serializers import OrderSerializer, StorageSpaceSerializer
from backend.coremodels.article import Article
from backend.coremodels.storage_unit import StorageUnit
from backend.coremodels.storage_space import StorageSpace
from backend.coremodels.transaction import Transaction
from backend.coremodels.inputOutput import InputOutput
from django.contrib.auth.models import User
# from datetime import datetime, timezone
from django.utils.dateparse import parse_date
from backend.__init__ import serviceInjector as si
from ..__init__ import dataAccessInjector as di


@si.register(name='StorageManagementService')
class StorageManagementService():
    @di.inject
    def __init__(self, _deps, *args):
        self.storage_access: StorageAccess = _deps["StorageAccess"]()
        self.order_access: OrderAccess = _deps["OrderAccess"]()
        self.user_access: UserAccess = _deps["UserAccess"]()

    def get_storage_unit_by_id(self, id: str) -> StorageUnit:
        return self.storage_access.get_storage(id)

    def get_storage_space_by_id(self, id: str) -> StorageSpace:
        return self.storage_access.get_compartment_by_id(id)

    def get_storage_space_by_article(self, article: Article) -> StorageSpace:
        return self.storage_access.get_compartment_by_id(id)

    def set_storage(self, id: str, amount: int) -> int:
        return self.storage_access.set_storage_amount(compartment_id=id,
                                                      amount=amount)

    def get_stock(self, id: str, article_id: str) -> int:
        return self.storage_access.get_compartment_stock(compartment_id=id,
                                                         article_id=article_id)

    def get_storage_unit_stock(self, id: str) -> dict:
        return self.storage_access.get_storage_stock(storage_id=id)

    def get_all_storage_units(self) -> dict:
        return self.storage_access.get_all_storage_units()

    def get_storage_value(self, id: str) -> int:
        compartments = self.storage_access.get_compartments_by_storage(
            storage_id=id)
        value = 0
        for compartment in compartments:
            value += compartment.article.price * compartment.amount
        return value

    def get_all_transactions(self) -> dict:
        return self.storage_access.get_all_transactions()

    # Storage is not connected to a costcenter atm
    # For now this is sum och costs (takeout-return)
    # from transactions for one storage_compartment
    def get_storage_cost(self, storage_id: str, start_date: str,
                         end_date: str) -> int:
        start_date_date = parse_date(start_date)
        end_date_date = parse_date(end_date)
        transactions = self.storage_access.get_transaction_by_storage(
            storage_id=storage_id)
        print(transactions)
        sum_value = 0
        takeout_value = 0
        return_value = 0
        for transaction in transactions:
            transaction_date = transaction.time_of_transaction
            transaction_date_date = transaction_date  # .date()
            user_cost_center = self.user_access.get_user_cost_center(
                transaction.by_user)
            if (user_cost_center == transaction.storage_unit.cost_center):
                if (start_date_date <= transaction_date_date
                        and end_date_date >= transaction_date_date):
                    # transaction_user = transaction.by_user
                    # cost_center = self.user_access.get_user_cost_center(
                    #                                   user=transaction_user)
                    # if cost_center == transaction.storage_id.cost_center
                    if transaction.operation == 1:
                        takeout_value = transaction.get_value()
                    if transaction.operation == 2:
                        return_value = transaction.get_value()
        sum_value = takeout_value - return_value
        return sum_value

    def get_storage_by_costcenter(self, cost_center: str) -> StorageUnit:
        return self.storage_access.get_storage_by_costcenter(cost_center)

# FR 10.1.3 #
# alltid takeout/takein
# TODO: This is a lot of work to refactor since barely any of the
# methods work. Leaving this
# TODO to the original author

    def add_to_storage(self, space_id: str, amount: int, username: str,
                       add_output_unit: bool) -> Transaction:
        storage_space = self.storage_access.get_compartment_by_id(
            id=space_id)
        storage_unit_id = storage_space.storage_unit
        article = Article.objects.get(lio_id=storage_space.article.lio_id)
        # inputOutput = InputOutput.objects.get(article=article)
        converter = 2
        user = User.objects.get(username=username)
        if (add_output_unit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount
            new_amount = amount
        else:
            amount_in_storage = StorageSpace.objects.get(
                id=id).amount + amount*converter
            new_amount = amount*converter

        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            new_transaction = Transaction.objects.create(
                storage_unit=storage_unit_id, article=article, operation=3,
                by_user=user, amount=new_amount,
                time_of_transaction=time_of_transaction)
            new_transaction.save()
            print("New add transaction created:")
            print(new_transaction)
            return new_transaction
            # except:
            # return None

# TODO: This is a lot of work to refactor since barely any of the methods work.
# Leaving this
# TODO to the original author

    def add_to_return_storage(self, space_id: str, amount: int,
                              username: str, add_output_unit: bool,
                              time_of_transaction) -> Transaction:
        storage_space = StorageSpace.objects.get(id=space_id)
        storage_unit_id = storage_space.storage_unit
        amount = amount
        article = Article.objects.get(lio_id=storage_space.article.lio_id)
        user = User.objects.get(username=username)
        medical_employee = User.objects.get(username=username).groups.filter(
            name='medical employee').exists()
        input_output_check = InputOutput.objects.filter(
                                article=article).exists()
        if (input_output_check):
            print("inne i första if")
            input_output = InputOutput.objects.get(article=article)
            converter = input_output.output_unit_per_input_unit
        else:
            print("inne i else")
            input_output = InputOutput.objects.create(article=article)
            converter = input_output.output_unit_per_input_unit

        if (medical_employee and article.sanitation_level == 'Z41'):
            return None

        if (add_output_unit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount + amount
            new_amount = amount
        else:
            amount_in_storage = StorageSpace.objects.get(
                id=id).amount + amount*converter
            new_amount = amount*converter
        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            print("skapar ny transaction")
            new_transaction = Transaction.objects.create(
                storage_unit=storage_unit_id, article=article, operation=2,
                by_user=user, amount=new_amount,
                time_of_transaction=time_of_transaction)
            new_transaction.save()
            print("New return transaction created:")
            print(new_transaction)
            return new_transaction

    def take_from_Compartment(self, space_id, amount, username,
                              add_output_unit, time_of_transaction):
        compartment = self.storage_access.get_compartment_by_id(id=space_id)
        article = Article.objects.get(lio_id=compartment.article.lio_id)
# inputOutput = InputOutput.objects.get(article=article)
        converter = 2
        user = User.objects.get(username=username)
        if (add_output_unit):
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount - amount
            new_amount = amount
        else:
            # eftersom det inte verkar finnas funktionalitet för
            # input/output-amounts så har jag satt denna till 2 bara för
            # testningens skull.
            if not converter:
                converter = 2
            amount_in_storage = StorageSpace.objects.get(
                id=space_id).amount - amount*converter
            new_amount = amount*converter
        if (amount_in_storage < 0):
            return None
        else:
            StorageSpace.objects.update(amount=amount_in_storage)
            new_transaction = Transaction.objects.create(
                storage_unit=compartment.storage_unit, article=article,
                operation=1, by_user=user, amount=new_amount,
                time_of_transaction=time_of_transaction)
            new_transaction.save()
            print("New add transaction created:")
            print(new_transaction)
            return new_transaction

    def get_article_in_storage_space(self, storage_space_id: str) -> Article:
        return self.storage_access.get_article_in_storage_space(
                                    storage_space_id=storage_space_id)

    def search_article_in_storage(self, storageUnitId: str,
                                  articleId: str) -> int:
        return self.storage_access.search_article_in_storage(
            storageUnitId=storageUnitId, articleId=articleId)
# FR 10.1.3 #

    def get_compartment_content_and_orders(self, compartment_id):
        compartment = self.storage_access.get_compartment_by_id(
            id=compartment_id)
        altered_dict = {}

        if compartment is None:
            return None

        compartment_serializer = StorageSpaceSerializer(compartment)
        if not compartment_serializer.is_valid:
            return None
        altered_dict.update(compartment_serializer.data)

        order = self._orderAccess.get_order_by_article_and_storage(
            compartment.storage_unit.id, compartment.article.lio_id)
        if order is not None:
            order_serializer = OrderSerializer(order)
            eta = self.order_access.get_eta(order.id)
            order_dictionary = {"ETA": eta}
            if order_serializer.is_valid:
                order_dictionary.update(order_serializer.data)
            altered_dict['Order'] = order_dictionary
            return altered_dict

    # FR 9.4.1 och FR 9.4.2 ##
    def create_compartment(self, storage_id: str, placement: str,
                           qr_code: str) -> StorageSpace:

        print(storage_id)
        compartment = self.storage_access.create_compartment(
            storage_id=storage_id, placement=placement, qr_code=qr_code
        )
        return compartment

    def get_compartment_by_qr(self, qr_code: str) -> StorageSpace:
        compartment = self.storage_access.get_compartment_by_qr(
            qr_code=qr_code)
        return compartment

    # FR 9.4.1 och FR 9.4.2 ##
