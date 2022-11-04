# from fileinput import filename
# from django.db import models
# import os.path

def make_text_file(name, article_id, storage_unit, eta, time_of_order):
    with open('Order: {}.txt'.format(name), 'w+') as file:
        file.write("Article: " + str(article_id) + "\n")
        file.write("Storage unit: " + str(storage_unit) + "\n")
        file.write("Estimated time of arrival: " + str(eta) + "\n")
        file.write("Time of order: " + str(time_of_order) + "\n")
        file.close()
