import unittest
from unittest.mock import patch, Mock
import requests
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
        # self.assertEqual(result, (mock_response.json.return_value, mock_response.json.return_value))
        self.assertEqual(result, mock_response.json.return_value)

    @patch('app.upload_data.FTP_TLS')
    def test_upload_zva(self, mock_ftp_tls):

        mock_ftp_instance = mock_ftp_tls.return_value
        mock_ftp_instance.connect.return_value = None
        mock_ftp_instance.login.return_value = None
        mock_ftp_instance.prot_p.return_value = None
        mock_ftp_instance.storbinary.return_value = None
        mock_ftp_instance.quit.return_value = None

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

        mock_ftp_tls.assert_called_once_with()
        mock_ftp_instance.connect.assert_called_once_with('ftp.example.com', 21)
        mock_ftp_instance.login.assert_called_once_with('abc', '123')
        mock_ftp_instance.prot_p.assert_called_once()
        mock_ftp_instance.storbinary.assert_called_once()
        mock_ftp_instance.quit.assert_called_once()
