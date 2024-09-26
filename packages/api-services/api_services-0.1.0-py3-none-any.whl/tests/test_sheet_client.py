import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from api_calls.sheet_client import GoogleSheetsClient  # Make sure to import your GoogleSheetsClient
import json

class TestGoogleSheetsClient(unittest.TestCase):
    
    @patch('api_calls.sheet_client.create_service')
    def setUp(self, mock_create_service):
        self.mock_service = MagicMock()
        mock_create_service.return_value = self.mock_service
        # Pass scopes as a list
        self.client = GoogleSheetsClient(client_secret_file='client_secret.json',scopes=['https://www.googleapis.com/auth/spreadsheets'])

    def test_initialization_with_invalid_scopes(self):
        with self.assertRaises(ValueError):
            GoogleSheetsClient('client_secret.json',scopes='invalid_scope')
    
    def test_get_sheet_with_missing_id(self):
        with self.assertRaises(ValueError):
            self.client.get_sheet('')

    def test_get_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        mock_response = {
            'spreadsheetId':spreadsheet_id,
            'properties': {
                'title':'Mock Spreadsheet Title',
                'locale': 'en_US'
            }
        }
        # Properly set up method chaining for the mock
        self.mock_service.spreadsheets.return_value.get.return_value.execute.return_value = mock_response

        result = self.client.get_sheet(spreadsheet_id)

        # Validate the result
        expected_result = json.dumps(mock_response, indent=4)
        self.assertEqual(result, expected_result)

    def test_read_sheet_with_missing_id(self):
        with self.assertRaises(ValueError):
            self.client.read_sheet('','A1:B2')

    def test_read_sheet_with_missing_range(self):
        with self.assertRaises(ValueError):
            self.client.read_sheet('1A2B3C4D5E6F7G8H9I0J','')

    def test_read_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        range_name = 'Sheet1!A1:B2'
        mock_values = [
            ['Header1', 'Header2'],
            ['Value1', 'Value2']
        ]
        mock_response = {'values': mock_values}
        
        self.mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = mock_response
        
        result = self.client.read_sheet(spreadsheet_id, range_name)
        
        # Validate the result
        self.assertEqual(result, mock_values)

    def test_read_sheet_to_dataframe_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        range_name = 'Sheet1!A1:B2'
        mock_values = [
            ['Header1', 'Header2'],
            ['Value1', 'Value2']
        ]
        mock_response = {'values': mock_values}

        self.mock_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = mock_response

        result = self.client.read_sheet_to_dataframe(spreadsheet_id, range_name)

        # Validate the result
        expected_df = pd.DataFrame(mock_values[1:], columns=mock_values[0])
        pd.testing.assert_frame_equal(result, expected_df)

    def test_create_sheet_with_missing_id(self):
        with self.assertRaises(ValueError):
            self.client.create_sheet('', 'NewSheet')

    def test_create_sheet_with_missing_name(self):
        with self.assertRaises(ValueError):
            self.client.create_sheet('1A2B3C4D5E6F7G8H9I0J', '')
    def test_create_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        sheet_name = 'NewSheet'
        mock_response = {
            'replies': [{'addSheet': {'properties': {'title': sheet_name}}}]
        }

        self.mock_service.spreadsheets.return_value.batchUpdate.return_value.execute.return_value = mock_response

        result = self.client.create_sheet(spreadsheet_id, sheet_name)

        expected_message = f"Sheet titled '{sheet_name}' created successfully. API Response: {json.dumps(mock_response, indent=4)}"
        self.assertEqual(result, expected_message)
    
    def test_delete_sheet_with_missing_id(self):
        with self.assertRaises(ValueError):
            self.client.delete_sheet('', 123)

    def test_delete_sheet_with_missing_sheet_id(self):
        with self.assertRaises(ValueError):
            self.client.delete_sheet('1A2B3C4D5E6F7G8H9I0J', '')
    
    def test_delete_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        sheet_id = 123
        mock_response = {}

        self.mock_service.spreadsheets.return_value.batchUpdate.return_value.execute.return_value = mock_response

        result = self.client.delete_sheet(spreadsheet_id, sheet_id)

        expected_message = f"Sheet with ID '{sheet_id}' deleted successfully."
        self.assertEqual(result, expected_message)

    def test_update_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        range_name = 'Sheet1!A1:B2'
        valueInputOption = 'RAW'
        values = [['Value1', 'Value2']]
        mock_response = {'updatedCells': 2}

        self.mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = mock_response

        result = self.client.update_sheet(spreadsheet_id, range_name, valueInputOption, values)

        expected_result = json.dumps(mock_response, indent=4)
        self.assertEqual(result, expected_result)

    def test_append_sheet_success(self):
        spreadsheet_id = '1A2B3C4D5E6F7G8H9I0J'
        range_name = 'Sheet1!A1:B2'
        valueInputOption = 'RAW'
        values = [['Value1', 'Value2']]
        mock_response = {'updates': {'updatedCells': 2}}

        self.mock_service.spreadsheets.return_value.values.return_value.append.return_value.execute.return_value = mock_response

        result = self.client.append_sheet(spreadsheet_id, range_name, valueInputOption, values)

        expected_result = json.dumps(mock_response, indent=4)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
