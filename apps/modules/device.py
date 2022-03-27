from .client import Client
from datetime import datetime
import pandas as pd

class DeviceProfile:
    def __init__(self, name, query_fields):
        self.name = name
        self.fields = query_fields


    def get_fieldnames(self):
        return list(self.fields.keys())

    def get_queryfields(self):
        return list(self.fields.values())

    def get_field(self, field):
        return self.fields[field]




class Device:
    def __init__(self, name, deviceprofile, client, bucket):
        self.name = name
        self.deviceprofile = deviceprofile
        self.client = client
        self.query = client.query_api()
        self.bucket = bucket


    def _make_query(self, start_time, end_time='', field_type='', field = ''):
        if end_time == '':
            date_range = f'(start:{start_time})'
        else:
            date_range = '(start:{start_time}, {end_time})' 

        field_types_arr = ['measurement', 'field']

        if not field_type in field_types_arr:
            raise ValueError(f'{field_type} does not exist in {field_types_arr}') 

        filter_field = ''

        fields = self.deviceprofile.get_queryfields() if field == '' else [field]
        for f in fields:
            filter_field +=  f'r["_{field_type}"] == "{f}" or '   

        return  f'''from(bucket: "{self.bucket}")
        |> range{date_range}
        |> filter(fn: (r) => r["device_name"] == "{self.name}")
        |> filter(fn: (r) => {filter_field[:-3]})     
    '''    

    def _query_get_all_data(self, start_time):
        filter_field = ''
        for f in self.deviceprofile.get_queryfields():
            filter_field +=  f'r["_measurement"] == "{f}" or '
        
        return f'''from(bucket: "{self.bucket}")
        |> range (start:{start_time})
        |> filter(fn: (r) => {filter_field[:-3]})
        '''


    def _collect_measurements(self, query, field_type='measurement'):
        tmp = []
        cols = self.deviceprofile.get_fieldnames()
        fields = self.deviceprofile.get_queryfields()
        for i in query:
            for j in i:
                tmp.append([j.get_measurement() if field_type == 'measurement' else j.get_field(), j.get_time(), j.get_value()])
        
        df = pd.DataFrame(tmp, columns=[field_type, 'time', 'value'])
        df = df.sort_values(by=['time'])    
        tmp = []
        for i in range(0, len(df), len(fields)):
            sliced = df.iloc[i:i+len(fields)].sort_values(by = [field_type])
            tinkge = [sliced[sliced[field_type] == f]['value'].values[0] for f in fields]
            tinkge.insert(0, str(sliced['time'].head(1).values[0]))
            tmp.append(tinkge)

        cols.insert(0, 'time')
        
        df = pd.DataFrame(tmp, columns=cols)
        df['time'] = df['time'].astype('datetime64[ns]')
        return df

    def query_all_fields(self, start_time, end_time=''):
        q = self._make_query(start_time, field_type='measurement')
        r = self.query.query(org=self.client.org, query=q)
        return self._collect_measurements(r)

    def get_all_data(self, start_time):
        q = self._query_get_all_data(start_time)
        r = self.query.query(org=self.client.org, query=q)
        return self._collect_measurements(r)


#not done
    def query_field(self, field, start_time, end_time=''):
        f = self.deviceprofile.get_field(field)
        if field in self.deviceprofile.get_fieldnames():
            q = self._make_query(start_time=start_time, end_time=end_time, field_type='measurement', field=f)
        else:
            raise ValueError(f'{field} does not exist in {self.deviceprofile.get_fieldnames()}') 
        r = self.query.query(org=self.client.org, query=q)

        tmp = []
        field_type = 'measurement'
        for i in r:
            for j in i:
                tmp.append([j.get_time(), j.get_value()])
        
        df = pd.DataFrame(tmp, columns=['time', field])
        df = df.sort_values(by=['time'])    
        return df
        
        # return self._collect_measurements(r)
        

     
       
   

