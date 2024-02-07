import unittest
import requests
import ssl
from unittest.mock import patch, Mock
from app.upload_data import upload_data_gov_lv, upload_zva


class UploadDataTestCase(unittest.TestCase):
    @patch.object(requests, 'post')
    def test_upload_data_gov_lv(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Success"}

        mock_post.return_value = mock_response

        resource_id = '123'
        api_key = '123'
        file_name = 'antidopinga_vielas.csv'

        result = upload_data_gov_lv(resource_id=resource_id,
                                    api_key=api_key,
                                    file_name=file_name)

        # with open(file_name, encoding='utf-8') as rb:
        #     mock_post.assert_called_with(
        #         'https://data.gov.lv/dati/api/action/resource_patch',
        #         data={'id': resource_id},
        #         headers={'X-CKAN-API-Key': api_key},
        #         files=[('upload', rb)])

        self.assertTrue(mock_post.called)
        self.assertEqual(result, mock_response.json.return_value)

    @patch('ftplib.FTP_TLS', autospec=True)
    def test_upload_zva(self, mock_ftp_tls_constructor):

        user_name = 'abc'
        password = '123'
        ftp_address = 'ftp.example.com'
        ftp_port = 21
        file_name = 'antidopinga_vielas.csv'

        upload_zva(user_name=user_name,
                   password=password,
                   ftp_address=ftp_address,
                   ftp_port=ftp_port,
                   file_name=file_name)
        
        mock_ftp_tls_constructor.assert_called_with('ftp.example.com', 21)
