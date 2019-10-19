# Company-Domain-Finder

## Commandline python script to find domain names of company

### Table of Contents
* [General info](#general-info)
* [How To use?](#how-to-use?)
* [Sample Usage](#sample-usage)
* [Features](#features)

### General info
Command line python script to find domain names of company.

### How to use?
To use this app locally, follow these steps:
1. Clone the project
2. Install requirements using `pip install -r requirements.txt`
3. For single company search - Run `python -W ignore app.py COMPANY_NAME`
4. For list of companies in a file -  Run `python -W ignore app.py -f  ABSOLUTE_PATH_OF_FILE`

## Sample usage
1. ` python -W ignore app.py Microsoft `
2. ` python -W ignore app.py "Salusive Health" `
3. ` python -W ignore app.py -f  ~/Desktop/sample_data.txt`

### Features
- Domain Finder
- Fuzzy String Matching
- Multiprocessing
- Prediction Confidence Score
