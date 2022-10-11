import requests
from getpass import getpass
from Constants import API_PROMPT, FILE_NAME_PROMPT, RESOURCE_ID_PROMPT
from helpers import stringInput

resourceID = stringInput(RESOURCE_ID_PROMPT)
apiKey = getpass(API_PROMPT)
fileName = stringInput(FILE_NAME_PROMPT)

requests.post('https://data.gov.lv/dati/api/action/resource_update',
              data={'id': resourceID},
              headers={'X-CKAN-API-Key': apiKey},
              files=[('upload', open(fileName, 'rb'))])
