from ...coremodels.transaction import Transaction
from ...coremodels.storage_unit import StorageUnit
from ...coremodels.cost_center import CostCenter
from ...coremodels.article import Article
from django.contrib.auth.models import User
from datetime import datetime
import uuid
# This allows us to create test objects easily, only assigning the parameters
# needed for the current test


def create_transaction(
    id=None, storage_unit=None, by_user=None, article=None,
        amount=1, time_of_transaction=None, operation=1):
    '''Create new transaction.'''

    if id is None:
        id = "1337"
    if storage_unit is None:
        storage_unit = create_storageunit()
    if by_user is None:
        by_user = create_user()
    if article is None:
        article = create_article()
    if time_of_transaction is None:
        time_of_transaction = datetime.now()

    transaction = Transaction(
        id=id, storage_unit=storage_unit, by_user=by_user,
        article=article, amount=amount, operation=operation,
        time_of_transaction=time_of_transaction)

    return transaction


def create_storageunit(id="1337",
                       name="testStorageUnit",
                       building="testbuilding",
                       floor="testFloor",
                       costCenter=None):
    '''Create new storage-unit.'''

    if costCenter is None:
        costCenter = create_costcenter()
    storage_unit = StorageUnit(name=name, building=building,
                               floor=floor,
                               cost_center=costCenter)

    return storage_unit


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
                   refill_unit=None, takeout_unit=None):
    '''Creating new article.'''

    article = Article(lio_id=lio_id, description=description,
                      price=price, name=name, Z41=Z41, image=image,
                      refill_unit=refill_unit, takeout_unit=takeout_unit)

    article.article_group.set(article_group)
    article.alternative_articles.set(alternative_articles)

    return article
