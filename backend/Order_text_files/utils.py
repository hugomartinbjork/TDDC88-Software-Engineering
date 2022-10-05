from django.db import models

def makeTextFile(article_id, storage_unit, eta, timeOfOrder):
    
    
        id = models.AutoField(primary_key=True)
        file = open("Order id: {}".format(id), "w+")

        file.write("Article: " + article_id)
        file.write("Storage unit: " + storage_unit)
        file.write("Estimated time of arrival: " + eta)
        file.write("Time of order: " + timeOfOrder)
        file.close()

        return file

