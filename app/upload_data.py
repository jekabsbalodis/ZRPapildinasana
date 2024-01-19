'''Upload data to State agency of medicines and data.gov.lv servers'''
import ftplib
import requests


def upload_data_gov_lv(resource_id, api_key, file_name):
    '''Upload data to data.gov.lv server'''
    with open(file_name, encoding='utf-8') as rb:
        requests.post('https://data.gov.lv/dati/api/action/resource_update',
                      data={'id': resource_id},
                      headers={'X-CKAN-API-Key': api_key},
                      files=[('upload', rb)])


def upload_zva(user_name, password, ftp_address, ftp_port, file_name):
    '''Upload data to State agency of medicines server'''
    with open(file_name, 'rb') as file:
        with ftplib.FTP_TLS() as ftps:
            ftps.connect(ftp_address, ftp_port)
            ftps.login(user_name, password)
            ftps.prot_p()
            ftps.dir()
            ftps.storbinary('STOR antidopinga_vielas.csv', file)
            ftps.dir()
            ftps.quit()
