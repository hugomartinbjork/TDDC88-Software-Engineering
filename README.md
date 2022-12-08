<div align='center'>
<h1>Welcome to RDX Solutions</h1>
<i>"Software so good you have to C4 yourself"</i>
</div>

![](rdx.gif)

[![api](https://img.shields.io/badge/API%20Version-2.3.0-green)](https://tddc88-2022.gitlab-pages.liu.se/api/api-v2/) [![uml](https://img.shields.io/badge/UML%20Diagram-blue)](https://app.diagrams.net/#G1wfihktfheNB74xuKVK3J80uDa2fYga5N)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

<h2>Prerequisites</h2>

[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/downloads/)   [![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)](https://www.djangoproject.com/download/) 


## Installation and Setup:
**1.Clone the Repository**
```sh
https://gitlab.liu.se/tddc88-2022/c4/rdx-solutions-backend-project.git
```
**2.Navigate to the Project Folder**
```sh
cd Web/

```
**3.Setup Virtual Environment and Install Requirements**
```sh
python3 -m venv venv
source venv/bin/activate - Mac 
source venv/Scripts/activate - Windows 
pip install -r requirements.txt

```
**4.Create a Superuser and Provide Login Details**
```sh
python3 manage.py createsuperuser
Username: example
Email address: example@gmail.com
Password: *****
```
**5.Migrate Database**
```sh
python3 manage.py makemigrations
python3 manage.py migrate
```
**6.Start Server**
```sh
python3 manage.py runserver
```
**7.Enter the site and login with provided credentials**
```sh
http://127.0.0.1:8000/admin/
```


