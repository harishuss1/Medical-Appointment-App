#!/bin/bash

# Uses pycodestyle to enforce pep8
pycodestyle AddressApp/*.py --ignore=E501 --show-source > lintreport.txt

#Linting jinja
djlint AddressApp/templates/ --profile=jinja --ignore "H005, H030, H031" >> lintreport.txt
