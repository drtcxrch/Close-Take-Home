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

# Portion of script that formats csv data and uploads to Close
#===========================================================================

# Create custom fields for Company Founded and Company Revenue

# company_founded = api.post('/custom_field/lead/', data={
#     "name": "Company Founded",
#     "type": "date"
# })

# company_revenue = api.post('/custom_field/lead/', data={
#     "name": "Company Revenue",
#     "type": "number"
# })

# company_founded_id = 'custom.' + company_founded["id"]
# company_revenue_id = 'custom.' + company_revenue["id"]

# # # Validates phone number format
# def is_valid_phone_number(phone_number):
#     pattern = re.compile(r'^\d{3}-\d{3}-\d{4}$')
#     return pattern.match(phone_number) is not None

# #Validates email format
# def is_valid_email(email):
#     regex = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
#     return regex.match(email) is not None

# # Function to convert a CSV to JSON
# # Takes the file paths as arguments
# def csv_to_close(csvFilePath):

#     # create a dictionary that will store all of the formatted data
#     data = {}

#     # Open a csv reader called DictReader
#     with open(csvFilePath, encoding='utf-8') as csvf:
#         csvReader = csv.DictReader(csvf)

#         # Convert each row into a dictionary
#         # and add it to data

#         for rows in csvReader:
#           lead = {}
#           contact = {}
#           for col_name in rows:
#             value = rows[col_name]

#             if col_name == 'Company' and value != '':
#               lead["name"] = value
#             elif col_name == 'Contact Name' and value != '':
#               contact["name"] = value
#             elif col_name == 'Contact Emails' and value != '':
#               #check if email is in valid format:
#               valid_email = is_valid_email(value)
#               if valid_email == True:
#                 contact["emails"] = [{"email": value}]
#               else:
#                 continue
#             elif col_name == 'Contact Phones' and value != '':
#               #check if phone is in valid format:
#               valid_phone = is_valid_phone_number(value)
#               if valid_phone == True:
#                 contact["phones"] = [{"phone": value}]
#               else:
#                 continue
#             elif col_name == 'custom.Company Founded' and value != '':
#               lead[company_founded_id] = value
#             elif col_name == 'custom.Company Revenue' and value != '':
#               lead[company_revenue_id] = value
#             elif col_name == 'Company US State' and value != '':
#               lead["addresses"] = [{"state": value}]
#           #Can't upload a lead that doesn't have a contact
#           if len(contact) == 0:
#             continue
#           lead_name = lead["name"]
#           lead["contacts"] = [contact]
#           nameVal = data.get(lead_name)
#           if nameVal is not None:
#             data[lead_name]["contacts"].append(contact)
#           else:
#             data[lead_name] = lead
#     print('leads formatted!')
#     return data

# # Call the csv_to_close function
# formatted = csv_to_close(contacts_csv)

# # Post formatted leads to API:
# def import_leads(data):
#   for formatted_lead in data:
#       api.post('lead', data[formatted_lead])
#   print('leads now available on Close dashboard!')

# #Call the import_leads function
# import_leads(formatted)

# Portion of script that fetches the leads and writes to a csv
#==============================================================================

# Getting leads filtered by by founded range between 01/01/1980 and 01/01/2023
# Data object copied from filtering on desktop Close app within leads, then clicking on the
#three 'more' dots and selecting 'Copy Filters'.

def get_filtered_lead_ids():
  filtered = api.post('/data/search/', data={
      "_limit": 200,
      "include_counts": True,
      "query": {
          "negate": False,
          "queries": [
              {
                  "negate": False,
                  "object_type": "lead",
                  "type": "object_type"
              },
              {
                  "negate": False,
                  "queries": [
                      {
                          "negate": False,
                          "queries": [
                              {
                                  "condition": {
                                      "before": {
                                          "type": "fixed_local_date",
                                          "value": "2023-01-01",
                                          "which": "end"
                                      },
                                      "on_or_after": {
                                          "type": "fixed_local_date",
                                          "value": "1980-01-01",
                                          "which": "start"
                                      },
                                      "type": "moment_range"
                                  },
                                  "field": {
                                      "custom_field_id": "cf_PRypQvDZ9yMDc8dL74vMwFNbaNy4NQsaWSDoVwNIxwx",
                                      "type": "custom_field"
                                  },
                                  "negate": False,
                                  "type": "field_condition"
                              }
                          ],
                          "type": "and"
                      }
                  ],
                  "type": "and"
              }
          ],
          "type": "and"
      },
      "results_limit": None,
      "sort": [
          {
              "direction": "asc",
              "field": {
                  "custom_field_id": "cf_PRypQvDZ9yMDc8dL74vMwFNbaNy4NQsaWSDoVwNIxwx",
                  "type": "custom_field"
              }
          }
      ]
  })

  leads = []
  lead_data = filtered["data"]

  for lead in lead_data:
    leads.append(lead["id"])

  return leads

lead_ids = get_filtered_lead_ids()

# Function to fetch filtered leads with id's obtained in last step
def fetch_filtered_leads(leads):
  results = []
  for lead in leads:
    result = api.get('lead/' + lead, params={
      '_fields': 'display_name,custom,addresses'
    })
    results.append(result)

  return results

leads = fetch_filtered_leads(lead_ids)

# Format the leads to keep just the required data
def format_leads(data):
  leads = []

  for lead in data:
    formatted_lead = {}
    revenue = lead["custom"].get("Company Revenue")
    #Confirm that we have state and revenue data from the lead and move on if we don't
    if len(lead["addresses"]) == 0 or revenue is None:
      continue
    formatted_lead["US State"] = lead["addresses"][0]["state"]
    formatted_lead["Lead"] = lead["display_name"]
    formatted_lead["Revenue"] = lead["custom"]["Company Revenue"]
    leads.append(formatted_lead)
  return leads

formatted = format_leads(leads)
print(formatted)