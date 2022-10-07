from django.test import TestCase
from backend.coremodels.article import * 
from backend.services.articleManagementService import *

class ArticleIdentificationTest(TestCase):    
     def setUp(self):                     
         Article.objects.create(lioId="1", description="First")         
            
         
     def test_getArticleByLioId_function(self):                    
        self.assertEqual(articleManagementService.getArticleByLioId("1"))        
        