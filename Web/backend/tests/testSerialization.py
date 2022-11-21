from django.test import TestCase
from backend.serializers import NearbyStoragesSerializer, ArticleCompartmentProximitySerializer
from backend.tests.testObjectFactory.coremodelFactory import create_compartment, create_storage, create_article, create_costcenter
import json
import pprint


class serializeStorageWithCompartment(TestCase):
    def setUp(self) -> None:
        self.compartment = create_compartment()

    def test_serializer_one_compartment(self):
        serializer = NearbyStoragesSerializer(self.compartment, read_only=True)
        # jsonData = json.dumps(serializer.data, indent=4)
        # print(jsonData)
        self.assertEqual(
            serializer.data["compartment"]["article"]["name"], 'testarticle')
    
    def test_serializer_multiple_compartments(self):
        compartment_list = [self.compartment, self.compartment]
        serializer = NearbyStoragesSerializer(compartment_list, read_only=True, many=True)
        self.assertEqual(
            serializer.data[0]["compartment"]["article"]["name"], 'testarticle')


class serializeArticlesOrderedCompartments(TestCase):
    def setUp(self):
        create_costcenter().save()
        self.article = create_article()
        self.articleNoCompartment = create_article(name="nocompartment", lio_id="22")
        self.articleNoCompartment.save()
        self.article.save()
        self.storage11 = create_storage(floor="1", building="1", id="1")
        storage12 = create_storage(floor="1", building="2", id="2")
        storage21 = create_storage(floor="2", building="1", id="3")
        storage22 = create_storage(floor="2", building="2", id="4")
        storage21.save()
        storage22.save()
        self.storage11.save()
        storage12.save()

        create_compartment(
            article=self.article, storage=storage21, id="Floor2Build1",
            ).save()
        create_compartment(
            article=self.article, storage=storage22, id="Floor2Build2"
            ).save()
        create_compartment(
            article=self.article, storage=self.storage11, id="Floor1Build1"
            ).save()
        create_compartment(
            article=self.article, storage=storage12, id="Floor1Build2"
            ).save()
    
    def test_regular_case_serialization(self):
        serializer = ArticleCompartmentProximitySerializer(
            article=self.article, storage=self.storage11)
        self.assertEqual(serializer.is_valid(), True)

    def test_article_no_compartment(self):
        serializer = ArticleCompartmentProximitySerializer(
            article=self.articleNoCompartment, storage=self.storage11)