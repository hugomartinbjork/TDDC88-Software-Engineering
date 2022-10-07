from django.test import TestCase
from backend.coremodels.article import * 
from backend.services.articleManagementService import *

class ArticleIdentificationTest(TestCase):    
     def setUp(self):                     
         Article.objects.create(lioId="1")         
            
         
     def test_getArticleByLioId_function(self): 
        article = Article.objects.get(lioId="1")                  
        self.assertEqual(articleManagementService.getArticleByLioId(self,"1"), article)        
