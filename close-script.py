from dotenv import load_dotenv
from closeio_api import Client
import os
import csv
import json
import re

load_dotenv()
api_key = os.getenv("API_KEY")
api = Client(api_key)
contacts_csv = 'Customer Support Engineer Take Home Project - Import File - MOCK_DATA.csv'
leads = 'leads.json'

# Create custom fields for Company Founded and Company Revenue

company_founded = api.post('/custom_field/lead/', data={
    "name": "Company Founded",
    "type": "date"
})

company_revenue = api.post('/custom_field/lead/', data={
    "name": "Company Revenue",
    "type": "number"
})

company_founded_id = company_founded["id"]
company_revenue_id = company_revenue["id"]

# Validates phone number format
def is_valid_phone_number(phone_number):
    pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    return pattern.match(phone_number) is not None

#Validates email format
def is_valid_email(email):
    regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
    return regex.match(email) is not None

# Function to convert a CSV to JSON
# Takes the file paths as arguments
def csv_to_close(csvFilePath):

    # create a dictionary that will store all of the formatted data
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data

        for rows in csvReader:
          lead = {}
          contact = {}
          for col_name in rows:
            value = rows[col_name]

            if col_name == 'Company' and value != '':
              lead["name"] = value
            elif col_name == 'Contact Name' and value != '':
              contact["name"] = value
            elif col_name == 'Contact Emails' and value != '':
              #check if email is in valid format:
              valid_email = is_valid_email(value)
              if valid_email == True:
                contact["emails"] = [{"email": value}]
              else:
                continue
            elif col_name == 'Contact Phones' and value != '':
              #check if phone is in valid format:
              valid_phone = is_valid_phone_number(value)
              if valid_phone == True:
                contact["phones"] = [{"phone": value}]
              else:
                continue
            elif col_name == 'custom.Company Founded' and value != '':
              lead[company_founded_id] = value
            elif col_name == 'custom.Company Revenue' and value != '':
              lead[company_revenue_id] = value
            elif col_name == 'Company US State' and value != '':
              lead["addresses"] = [{"state": value}]
          #Can't upload a lead that doesn't have a contact
          if len(contact) == 0:
            continue
          lead_name = lead["name"]
          lead["contacts"] = [contact]
          nameVal = data.get(lead_name)
          if nameVal is not None:
            data[lead_name]["contacts"].append(contact)
          else:
            data[lead_name] = lead
    print('leads formatted!')
    return data

# Call the csv_to_close function
formatted = csv_to_close(contacts_csv)

# Post formatted leads to API:
def import_leads(data):
  for formatted_lead in data:
      api.post('lead', data[formatted_lead])
  print('leads now available on Close dashboard!')

#Call the import_leads function
import_leads(formatted)