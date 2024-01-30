import unittest
import requests
from unittest.mock import patch, Mock
from app.upload_data import upload_data_gov_lv, upload_zva


class UploadDataTestCase(unittest.TestCase):
    @patch.object(requests, 'post')
    def test_upload_data_gov_lv(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Success"}

        mock_post.return_value = mock_response

        resource_id = 'ee8f9b14-1eee-494a-b7f5-6777a8232dcb'
        api_key = '31bf794d-f10c-4dd0-86ff-9ffc9f987505'
        file_name = 'antidopinga_vielas.csv'

        result = upload_data_gov_lv(resource_id=resource_id,
                                    api_key=api_key,
                                    file_name=file_name)

        # with open('antidopinga_vielas.csv', encoding='utf-8') as rb:
        #     mock_post.assert_called_with(
        #         'https://data.gov.lv/dati/api/action/resource_patch',
        #         data={'id': 'ee8f9b14-1eee-494a-b7f5-6777a8232dcb'},
        #         headers={'X-CKAN-API-Key': '31bf794d-f10c-4dd0-86ff-9ffc9f987505'},
        #         files=[('upload', rb)])

        self.assertEqual(result, mock_response.json.return_value)
