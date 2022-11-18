from ...coremodels.transaction import Transaction
from ...coremodels.storage import Storage
from ...coremodels.cost_center import CostCenter
from ...coremodels.article import Article
from ...coremodels.compartment import Compartment
from django.contrib.auth.models import User
from datetime import datetime
import uuid
# This allows us to create test objects easily, only assigning the parameters
# needed for the current test

def create_compartment(
        id="123", storage=None, article=None, amount=30,
        order_point=20, standard_order_amount=10, placement="AB",
        maximal_capacity=50):

    if storage is None:
        storage = create_storage()
    if article is None:
        article = create_article()
    compartment = Compartment(maximal_capacity=maximal_capacity, id=id,
                              storage=storage, article=article, amount=amount,
                              order_point=order_point, placement=placement,
                              standard_order_amount=standard_order_amount
                              )
    return compartment


def create_transaction(
    id=None, storage=None, by_user=None, article=None,
        amount=1, time_of_transaction=None, operation=1):
    '''Create new transaction.'''

    if id is None:
        id = "1337"
    if storage is None:
        storage = create_storage()
    if by_user is None:
        by_user = create_user()
    if article is None:
        article = create_article()
    if time_of_transaction is None:
        time_of_transaction = datetime.now()

    transaction = Transaction(
        id=id, storage=storage, by_user=by_user,
        article=article, amount=amount, operation=operation,
        time_of_transaction=time_of_transaction)

    return transaction


def create_storage(id="1337",
                   name="testStorage",
                   building="testbuilding",
                   floor="testFloor",
                   costCenter=None):
    '''Create new storage-unit.'''

    if costCenter is None:
        costCenter = create_costcenter()
    storage = Storage(id=id, name=name,
                      building=building, floor=floor,
                      cost_center=costCenter)
    return storage


def create_user(first_name="Elias", is_superuser=False,
                last_name="Eliasson", username="Elias123"):
    '''Creating new user.'''
    user = User(first_name=first_name, is_superuser=is_superuser,
                last_name=last_name, username=username)
    return user


def create_costcenter(name="testCostCenter", id="1337"):
    '''Creating new cost-center.'''
    cost_center = CostCenter(name=name, id=id)
    return cost_center


def create_article(lio_id="1337", description="testdescription",
                   price=0, name="testarticle", Z41=False, image=None,
                   article_group=[], alternative_articles=[],
                   input=1, output=1, output_per_intput=1):
    '''Creating new article.'''

    article = Article(lio_id=lio_id, description=description,
                      price=price, name=name, Z41=Z41, image=image,
                      input=input, output=output)

    article.article_group.set(article_group)
    article.alternative_articles.set(alternative_articles)

    return article


# def create_compartment_list(
#     length, ids=None, storages=None, articles=None, amounts=None,
#     order_points=None, standard_order_amounts=None, placements=None,
#     maximal_capacities=None):

#     compartment_list = []

#     for i in range(1, length):
#         if ids is not None:
#             id = ids[i]
#         else: 
#             id=Non
#         if storages is not None:
#             storage = storages[i]
#         if articles is not None:
#             article = articles[i]
#         if amounts is not None:
#             amount = amounts[i]
#         if order_points is not None:
#             order_point = order_points[i]
#         if standard_order_amounts is not None:
#             standard_order_amount = standard_order_amounts[i]
#         if placements is not None:
#             placement = placements[i]
#         if maximal_capacities is not None: 
#             maximal_capacity = maximal_capacities[i]
#         compartment_list.append(create_compartment(
#             id=id, storage=storage, article=article, amount=amount,
#             order_point=order_point, standard_order_amount=standard_order_amount,
#             placement=placement, maximal_capacity=maximal_capacity
#         ))
