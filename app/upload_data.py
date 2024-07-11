'''Upload data to State agency of medicines and data.gov.lv servers'''
from ftplib import FTP_TLS
import requests


def upload_data_gov_lv(resource_id, api_key, file_name):
    '''Upload data to data.gov.lv server'''
    with open(file_name, encoding='utf-8') as rb:
        data_resource_patch = {'id': resource_id}
        headers = {'X-CKAN-API-Key': api_key}
        files = {'upload': rb}
        response_resource_patch = requests.post('https://data.gov.lv/dati/api/action/resource_patch',
                                                data=data_resource_patch,
                                                headers=headers,
                                                files=files)
        # reader = csv.DictReader(rb)
        # records = [row for row in reader]
        # data_datastore_upsert = {'resource_id': resource_id,
        #                          'force': True,
        #                          'records': records,
        #                          'calculate_record_count': True}
        # response_datastore_upsert = requests.post('https://data.gov.lv/dati/lv/api/3/action/datastore_upsert',
        #                                           data=data_datastore_upsert,
        #                                           headers=headers
        #                                           )
    print(response_resource_patch.content)
    # print(response_datastore_upsert.content)
    # return response_resource_patch.json(), response_datastore_upsert.json()
    return response_resource_patch.json()


def upload_zva(user_name, password, ftp_address, ftp_port, file_name):
    '''Upload data to State agency of medicines server'''
    ftps = FTP_TLS()
    ftps.connect(ftp_address, ftp_port)
    ftps.login(user_name, password)
    ftps.prot_p()
    with open(file_name, 'rb') as file:
        ftps.storbinary('STOR antidopinga_vielas.csv', file)
    ftps.quit()
