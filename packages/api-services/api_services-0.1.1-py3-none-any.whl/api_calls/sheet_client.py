from api_services.utils import create_service
import json
import pandas as pd

class GoogleSheetsClient:
    def __init__(self, client_secret_file,api_version='v4', scopes=None, prefix=''):
        if scopes is None:
            scopes=[]
        elif not isinstance(scopes,list):
            raise ValueError("Scopes must be a list.")
        self.service = create_service(client_secret_file, 'sheets', api_version, *scopes, prefix=prefix)

    def get_sheet(self, spreadsheet_id):
        # Ensure the spreadsheet_id is provided
        if not spreadsheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get"
            )
        
        try:
            # Call the Google Sheets API to fetch the spreadsheet metadata
            result = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            data = json.dumps(result, indent=4)
            return data
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch metadata information about the spreadsheet '{spreadsheet_id}'. "
                "For more help, check the API documentation: "
                "https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get. "
                f"Error details: {str(e)}"
            )
    
    def read_sheet(self, spreadsheet_id, range_name):
        # Ensure both spreadsheet_id and range_name are provided
        if not spreadsheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get"
            )

        if not range_name:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get"
            )
        
        try:
            # Call the Google Sheets API to fetch data from the specified range
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, 
                range=range_name
            ).execute()
            # Extract the values from the result
            data = result.get('values',[])
        except Exception as e:
            raise RuntimeError(
                f"Failed to get data from the spreadsheet '{spreadsheet_id}' in range '{range_name}'. "
                "For more details, check the API documentation: "
                "https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get. "
                f"Error details: {str(e)}"  
            )

        if not data:
            raise ValueError(
                f"No data found in the specified range '{range_name}' in spreadsheet '{spreadsheet_id}'. "
                "Please ensure the range is correct. "
                "For more information, visit: https://developers.google.com/sheets/api/guides/values#reading_data"
            )
        
        return data

    def read_sheet_to_dataframe(self, spreadsheet_id, range_name):
        # Ensure both spreadsheet_id and range_name are provided
        if not spreadsheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get"
            )
        
        if not range_name:
            raise ValueError(
                "Missing arguments, ensure you include the range_name. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get"
            )
        
        try:
            # Call the Google Sheets API to fetch data from the specified range
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, 
                range=range_name
            ).execute()
            # Extract the values from the result
            values = result.get('values',[])
        except Exception as e:
            raise RuntimeError(
                f"Failed to get data from the spreadsheet '{spreadsheet_id}' in range '{range_name}'. "
                "For more details, check the API documentation: "
                "https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get. "
                f"Error details: {str(e)}"  
            )

        # Check if the fetched range contains any data
        if not values:
            raise ValueError(
                f"No data found in the specified range '{range_name}' in spreadsheet '{spreadsheet_id}'. "
                "Please ensure the range is correct. "
                "For more information, visit: https://developers.google.com/sheets/api/guides/values#reading_data"
            )
        
        # Covert values into a dataframe
        data = pd.DataFrame(values[1:],columns=values[0])
        
        return data
    
    def create_sheet(self, spreadsheet_id, sheet_name):
        # Ensure both spreadsheet_id and sheet_name are provided 
        if not spreadsheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate"
            )
        
        if not sheet_name:
            raise ValueError(
                "Missing arguments, ensure you include the sheet_name. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate"
            )
        # Define the request to add a new sheet
        requests = [{
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            }
        }]
        body = {'requests':requests}
        try:
            # Call the Google Sheets API to create a new sheet
            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body
            ).execute()

            # Convert the result to a formatted JSON string for readability
            result_formatted = json.dumps(result, indent=4)

            # Return a success message with the sheet name and the API response
            return f"Sheet titled '{sheet_name}' created successfully. API Response: {result_formatted}"
        except Exception as e:
            # Provide a detailed error message with a link to the API documentation
            raise RuntimeError(
                f"Failed to create a new sheet titled '{sheet_name}' in spreadsheet '{spreadsheet_id}'. "
                "For more details, check the API documentation: "
                "https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate. "
                f"Error details: {str(e)}"
            )

    def delete_sheet(self, spreadsheet_id, sheet_id):
        # Ensure sheet_id and spreadsheet_id are provided
        if not spreadsheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the spreadsheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate"
            )
        
        if not sheet_id:
            raise ValueError(
                "Missing arguments, ensure you include the sheet_id. "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate"
            )
        # Define the request to delete the sheet
        requests = [{
            'deleteSheet': {
                'sheetId': sheet_id
            }
        }]
        body= {'requests':requests}
        try:
            # Call the Google Sheets API to delete the sheet
            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id, 
                body=body
            ).execute()

            # Return a success message
            return f"Sheet with ID '{sheet_id}' deleted successfully."

        except Exception as e:
            # Provide detailed error information along with a link to the documentation
            raise RuntimeError(
                f"Failed to delete sheet with ID '{sheet_id}' in spreadsheet '{spreadsheet_id}'. "
                "For more details, check the API documentation: "
                "https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate. "
                f"Error details: {str(e)}"
            )

    def update_sheet(self, spreadsheet_id, range_name, valueInputOption, values, include_headers=True):
        # Ensure spreadsheet_id and range_name, valueInputOption, values are provided 
        if not range_name and not spreadsheet_id and not valueInputOption and not values:
            raise ValueError(
                "Missing argument, ensure you include all required arguments: spreadsheet_id, range_name, valueInputOption (either 'RAW' or 'USER_ENTERED'). "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update"
            )
        # If value is a dataframe, convert it to a 2D list
        if isinstance(values,pd.DataFrame):
            if include_headers:
                headers = [list(values.columns)]
                data = values.values.to_list()
                values = headers + data
            else:
                values = values.values.tolist()
        # Ensure values in a 2D list (list of lists)
        if not isinstance(values,list) or not all(isinstance(row,list) for row in values):
            raise ValueError(
                "Values must be a 2D list (list of lists), where each inner list represents a row of values. "
                "For more details, visit: https://developers.google.com/sheets/api/guides/values#writing_data_to_a_range"
            )
        body = {'values': values}
        try:
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=valueInputOption,
                body=body
            ).execute()
            return json.dumps(result, indent=4)
        except Exception as e:
            raise RuntimeError(
                f"Failed to update sheet '{spreadsheet_id}' in range '{range_name}'. For more help, check the API documentation: "
                f"https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update. Error details: {str(e)}"
            )
        
    def append_sheet(self, spreadsheet_id, range_name, valueInputOption, values, include_headers=True):
        # Ensure spreadsheet_id and range_name, valueInputOption, values are provided 
        if not range_name and not spreadsheet_id and not valueInputOption and not values:
            raise ValueError(
                "Missing argument, ensure you include all required arguments: spreadsheet_id, range_name, valueInputOption (either 'RAW' or 'USER_ENTERED'). "
                "For more information, visit: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update"
            )
        # If value is a dataframe, convert it to a 2D list
        if isinstance(values,pd.DataFrame):
            if include_headers:
                headers = [list(values.columns)]
                data = values.values.to_list()
                values = headers + data
            else:
                values = values.values.tolist()
        # Ensure values in a 2D list (list of lists)
        if not isinstance(values,list) or not all(isinstance(row,list) for row in values):
            raise ValueError(
                "Values must be a 2D list (list of lists), where each inner list represents a row of values. "
                "For more details, visit: https://developers.google.com/sheets/api/guides/values#writing_data_to_a_range"
            )
        # Prepare the body for the request
        body = {'values': values}
        try:
            # Call the append API
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=valueInputOption,
                body=body
            ).execute()
            # Return the result in a formatted JSON string
            return json.dumps(result, indent=4)
        except Exception as e:
            raise RuntimeError(
                f"Failed to append sheet '{spreadsheet_id}' in range '{range_name}'. For more help, check the API documentation: "
                f"https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append. Error details: {str(e)}"
            )
        
