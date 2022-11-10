# from fileinput import filename
# from django.db import models
# import os.path

def make_text_file(name, storage, articles, eta, time_of_order):
    with open('Order: {}.txt'.format(name), 'w+') as file:
        for article in articles:
            file.write("Article: " + str(article['lioNr']) + "\n")
        file.write("Storage: " + str(storage) + "\n")
        file.write("Estimated date of arrival: " + str(eta) + "\n")
        file.write("Time of order: " + str(time_of_order) + "\n")
        file.close()
