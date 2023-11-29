import requests
import ftplib


def upload_data_gov_lv(resourceID, apiKey, fileName):
    requests.post('https://data.gov.lv/dati/api/action/resource_update',
                  data={'id': resourceID},
                  headers={'X-CKAN-API-Key': apiKey},
                  files=[('upload', open(fileName, 'rb'))])


def upload_zva(userName, passWord, ftpAddress, ftpPort, fileName):
    with open(fileName, 'rb') as file:
        with ftplib.FTP_TLS() as ftps:
            ftps.connect(ftpAddress, ftpPort)
            ftps.login(userName, passWord)
            ftps.prot_p()
            ftps.dir()
            ftps.storbinary('STOR antidopinga_vielas.csv', file)
            ftps.dir()
            ftps.quit()
