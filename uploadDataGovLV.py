import requests
from getpass import getpass
from Constants import API_PROMPT, FILE_NAME_PROMPT, RESOURCE_ID_PROMPT
from helpers import stringInput

resourceID = stringInput(RESOURCE_ID_PROMPT)
apiKey = getpass(API_PROMPT)
fileName = stringInput(FILE_NAME_PROMPT)

# TODO atspoguļot informāciju par laiku, kad pēdējo reizi atjaunoti dati
# TODO atspoguļot informāciju, ka datu augšuplāde bijusi sekmīga
# TODO https://data.gov.lv/dati/lv/api/3/action/package_show?id=medikamenti-kas-satur-dopinga-vielas
requests.post('https://data.gov.lv/dati/api/action/resource_update',
              data={'id': resourceID},
              headers={'X-CKAN-API-Key': apiKey},
              files=[('upload', open(fileName, 'rb'))])
