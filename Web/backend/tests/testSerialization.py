from django.test import TestCase
from backend.serializers import NearbyStoragesSerializer
from backend.tests.testObjectFactory.coremodelFactory import create_compartment
import json


class serializeStorageWithCompartment(TestCase):
    def setUp(self) -> None:
        self.compartment = create_compartment()

    def test_serializer_one_compartment(self):
        serializer = NearbyStoragesSerializer(self.compartment, read_only=True)
        jsonData = json.dumps(serializer.data, indent=4)
        print(jsonData)
        self.assertEqual(
            serializer.data["compartment"]["article"]["name"], 'testarticle')
    
    def test_serializer_multiple_compartments(self):
        compartment_list = [self.compartment, self.compartment]
        serializer = NearbyStoragesSerializer(compartment_list, read_only=True, many=True)
        self.assertEqual(
            serializer.data[0]["compartment"]["article"]["name"], 'testarticle')
