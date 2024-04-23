#!/bin/bash

# Uses pycodestyle to enforce pep8
pycodestyle MedicalApp/*.py --ignore=E501 --show-source > lintreport.txt

#Linting jinja
djlint MedicalApp/templates/ --profile=jinja --ignore "H005,H030,H031" >> lintreport.txt
