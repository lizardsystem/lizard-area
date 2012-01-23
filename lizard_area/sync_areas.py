"""
Adapter for areas
"""

import httplib
from lizard_area.models import Area
from lizard_area.models import Category


class CSVHeader(Object):

    """ """
    def __init__(self):
        self.headers = []

    def __getitem__(self):
        return self.data[key]

    def __setitem__(self, header):
        self.data.append(header)


class CSVParser(Object):
    """
    Adapter for showing areas from GeoObjects.
    """
    def __init__(self, csv_string):
        super(CSVParser, self).__init__(*args, **kwargs)
        self.csv_string = csv_string
        self.csv_arrays = []
        self.header = []
        

    def set_header(self):
        pass

    def set_csv_array(self):
        patern = '/r/n'
        self.csv_array.split

    
   
