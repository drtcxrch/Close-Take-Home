from dotenv import load_dotenv
from closeio_api import Client
import os

load_dotenv()
api_key = os.getenv("API_KEY")
api = Client(api_key)

# Run this script to delete custom fields:

# custom_fields = api.get('/custom_field/lead/')

# fields = custom_fields["data"]
# for field in fields:
#   api.delete('/custom_field/lead/' + field["id"])

deleted = api.get('/custom_field/lead/')
print(deleted)
