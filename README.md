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

## Sample usage
1. ` python -W ignore app.py Microsoft `
2. ` python -W ignore app.py "Salusive Health" `

### Features
- Domain Finder
- Fuzzy String Matching For Comparing Similiar Results
- Non Daemonic Multiprocessing
- Tertiary Sources Validation(Crucnhbase,Angellist,Owler,Twitter)
- Cloudflare's IUAM Bypass
