import pygsheets

import pandas as pd
import datetime as dt

class GSheetHelper():
    def __init__(self, sheet_name_or_id, path='/nfs/secrets/', cred_file='client_secret.json'):
        self.__client__ = pygsheets.authorize(service_file=path + cred_file)

        if len(sheet_name_or_id) >= 44:
            self.__spreadsheet__ = self.__client__.open_by_key(sheet_name_or_id)
        else:
            self.__spreadsheet__ = self.__client__.open(sheet_name_or_id)
        
    def __read_cell__(self, sheet_name, cell):
        sheet = self.__spreadsheet__.worksheet_by_title(sheet_name)
        return sheet.cell(cell).value
        
    def __read_range__(self, sheet_name, cell_range, header=True, header_range=None):
        start = cell_range.split(':')[0]
        end = cell_range.split(':')[1]

        sheet = self.__spreadsheet__.worksheet_by_title(sheet_name)
        values = sheet.get_values(start, end, include_tailing_empty=False, include_tailing_empty_rows=False)

        if header:
            if header_range == None:
                header = values[0]
                values = values[1:]
            else:
                start = header_range.split(':')[0]
                end = header_range.split(':')[1]

                header = sheet.get_values(start, end, include_tailing_empty=False, include_tailing_empty_rows=False)

            df = pd.DataFrame(values, columns=header)
        else:
            df = pd.DataFrame(values)

        return df
    
    def __write_cell__(self, sheet_name, value, cell):
        sheet = self.__spreadsheet__.worksheet_by_title(sheet_name)
        sheet.update_value(cell, value)
        
    def __write_dataframe__(self, sheet_name, df, start_cell, header=True):
        sheet = self.__spreadsheet__.worksheet_by_title(sheet_name)
        sheet.set_dataframe(df, start=start_cell, copy_index=False, copy_head=header)
    
    def read(self, sheet_name, cell_or_range, header=True, header_range=None):
        print('[{}] Reading from Tab: {}'.format(dt.datetime.now(), sheet_name))
        
        if_range = cell_or_range.find(':')
        
        if if_range == -1:
            return self.__read_cell__(sheet_name, cell_or_range)
        
        return self.__read_range__(sheet_name, cell_or_range, header, header_range)
    
        print('[{}] Data Read Successfully'.format(dt.datetime.now()))
    
    def write(self, sheet_name, val_or_df, cell):
        print('[{}] Writing to Tab: {}'.format(dt.datetime.now(), sheet_name))
        
        if type(val_or_df) == type(pd.DataFrame()):
            self.__write_dataframe__(sheet_name, val_or_df, cell)
        else:
            self.__write_cell__(sheet_name, val_or_df, cell)
        
        print('[{}] Data Written Successful'.format(dt.datetime.now()))
        
    def delete(self, sheet_name, cell_or_range):
        print('[{}] Delete from Tab: {}'.format(dt.datetime.now(), sheet_name))
        
        if cell_or_range.find(':') != -1:
            start = cell_or_range.split(':')[0]
            end = cell_or_range.split(':')[1]
        
            sheet = self.__spreadsheet__.worksheet_by_title(sheet_name)
            empty_values = [['' for _ in row] for row in sheet.get_values(start, end)]
            self.__write_dataframe__(sheet_name, pd.DataFrame(empty_values), cell_or_range, False)
        else:
            self.__write_cell__(sheet_name, '', cell)
        
        print('[{}] Data Deleted Successful'.format(dt.datetime.now()))