import time
import geopandas as gpd
import urllib
import datetime as dt
import pandas as pd

class wicced():
    #constructor
    def __init__(self, max = 0, data_source = 'cema', data_format = 'application/json', ): # parameterized __init__ to pass
        ## Data source is where the data will be coming from
        ## Data format is only application or json
        self.server_url = 'https://udel-geoserver.nautilus.optiputer.net/geoserver/'       # useful params on creation
        self.workspace = 'cite'
        self.service = 'ows?service=WFS'
        self.version = 'version=1.0.0'
        self.request = 'request=GetFeature'
        self.feature_name = 'typeName=' + self.workspace + ':' + data_source
        self.format = 'outputFormat={}'.format(data_format)
        self.query_start = 'CQL_FILTER='
        self.maxFeatures = 'maxFeatures={}'.format(max)
#         print(self.maxFeatures)
    ## addDate
    ## sets the specific date and time for retreival from the database
    ## params:
    ##    date - a string of the format YYYY-mm-dd HH:MM
    ## 
    def addDate(self, date):
        ## date : string with format %Y-%m-%d %H:%M
        ## provides time for buildUrl
        #self.date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M') 
        self.date = pd.to_datetime(date, infer_datetime_format = True)

    
    
    ## addDateRange
    ## sets a specific date range for retrieval
    ## params:
    ##   start - a string of the format YYYY-mm-dd HH:MM for the starting time
    ##   end - a string of the format YYYY-mm-dd HH:MM for the ending time 
    def addDateRange(self, start, end):
        ## date range : find the dates in any range
        ## provides time for buildURL
        ## Values taken are strings
        self.start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
        self.end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
        
    
    
    ## addDataType
    ## set the data type for retreival
    ## params:
    ##    type - a string containing the data type to be retreived
    def addDataType(self, type):
        #data type: be able to get specific
        #type of data out of a list.
        ##Values taken are strings
        self.data_type = type

        
    ## addBox
    ## add a bounding box to subset data retreived to a specific area
    ## params:
    ##    ul_lon - a number representing the Upper-Left longitude
    ##    ul_lat - a number representing the Upper-Left latitude
    ##    lr_lon - a number representing the Lower-Right longitudece, but then now t
    ##    lr_lat - a number representing the Lower-Right latitude
    def addBox(self, ul_lon, ul_lat, lr_lon, lr_lat):
        ## addBox: add coordinates to map out
        ## an area. ul_lon and ul_lat is upper
        ## left part of the box and lr_lon, lr_lat
        ## is lower right part of box.
        ## Value are numbers
        self.ul_lon = ul_lon
        self.ul_lat = ul_lat
        self.lr_lon = lr_lon
        self.lr_lat = lr_lat
    
        
    ## changeFormat
    ## select a different format for the returned data
    ## params:
    ##    format - a string containing the desired format
    ##             valid options: csv, application/json
    def changeFormat(self, format):
        # changeFormat: Changes to the kind of file requested
        # csv or application/json
        self.format = "outputFormat=" + format
        
        
    ## buildUrl
    ## pulls the input user selections together to create a URL for retreiving data
    ## Params: None
    ## Return Value: a string containing the encoded URL
    
    def buildUrl(self):
        ## Put together a bunch of url strings together to make a fully functional one.
        ## constructs query url with parameters as given from above functions.
        ## makes a link you can go to
        
#         print('building_url')
        full_url = '/'.join([self.server_url, self.workspace, self.service])
        full_url += '&' + '&'.join([self.version, self.request, self.feature_name, self.maxFeatures, self.format])
        query_string = ''
        if hasattr(self, 'date'):
            query_string += "dtg='" + self.date.strftime('%Y-%m-%dT%H:%M:00Z') + "'"
        elif hasattr(self, 'start') and hasattr(self, 'end'):
            query_string += "dtg between '" + self.start.strftime('%Y-%m-%dT%H:%M:00Z') + "' and '" + self.end.strftime('%Y-%m-%dT%H:%M:00Z') + "'"
        if hasattr(self, 'data_type'):
            if not query_string:
                query_string = "type='" + self.data_type + "'"
            else:
                query_string = query_string + " and type='" + self.data_type + "'"
        if hasattr(self, 'ul_lon') and hasattr(self, 'ul_lat') and hasattr(self, 'lr_lat') and hasattr(self, 'lr_lon'):
#             print('ADDING BOUNDING BOX')
            if not query_string:
                query_string = "bbox(geom," + ",".join([str(self.ul_lon),str(self.ul_lat),str(self.lr_lon),str(self.lr_lat)])+")"
            else:
                query_string = query_string + " and bbox(geom," + ",".join([str(self.ul_lon),str(self.ul_lat),str(self.lr_lon),str(self.lr_lat)])+")"            
        if query_string != '':
            return (full_url + "&" + self.query_start + urllib.parse.quote(query_string, "="))
        else:
            return (full_url + "&" + query_string)
        

        
def get_full_query_by_month(data_source, start, end, ul, lr, feature=False): # This is the prefered way to pull data
    ## Anything in the data source within
    ## that time will be shown
    
    '''
    Requests data from the stated data source each month in the interval of time, collecting the unique collection
       of all samples in that time interval.
       
       data_source : one of <cema, usgs or ncep>
       start, end  : pandas Timestamp objects
       ul, lr      : tuples of gps coordinates
       feature     : any sing data type present in <data_source>, or false to get all data types
       '''
    max_rows = 1000000
    so_far = []
    for year in range(start.year, end.year + 1):
        for month in range(1, 13):
            first_day = pd.Timestamp(year=year, month=month, day=1)
            last_day  = pd.Timestamp(year=year, month=month, day=first_day.daysinmonth)
            
            api = wicced(max=max_rows, data_source=data_source)
            api.addDateRange(first_day.strftime('%Y-%m-%d %H:%M'), 
                             last_day.strftime('%Y-%m-%d %H:%M'))
            api.addBox(ul[1], 
                       ul[0], 
                       lr[1], 
                       lr[0])
            if feature:
                api.addDataType(feature)
            url = api.buildUrl()
            print("Requesting year {} month {}".format(year, month))
            t0 = time.time()
            tmp = gpd.read_file(url)
            print("Request took {:.1f} seconds".format(time.time() - t0))
            so_far += [tmp]
            print("Got {} rows".format(tmp.shape))
#             if tmp.shape[0] == max_rows:
#                 tmp = tmp.sort_values(by='dtg')
#                 start = pd.to_datetime(tmp.dtg.unique()[-1]).strftime('%Y-%m-%d %H:%M')
#                 print(start)
#             else:
    full_dataset = pd.concat(so_far, axis=0)
    return full_dataset

def separate_by_location(dataset, prefix):
    '''receives the output of get_full_query_by_month and returns the dataset aligned by time (index)
       and separated by unique GPS location into features
       
       dataset    : output of get_full_query_by_month for a single feature
       prefix     : string to idenify the feature 
       '''
    df = dataset.copy()
    df['hashable'] = df.geometry.apply(str)
    locs = df.hashable.unique()
    
    df = df.set_index('hashable')
    stations_idx = {i: locs[i] for i in range(len(locs))}
    stations = {}
    for idx, point in enumerate(locs):
#         print(df)
        stat = df[df.index == point].set_index('dtg')['value']
        stat = stat[~stat.index.duplicated(keep='first')]
        stations["{}_{}".format(prefix, idx)] = stat
    joined = pd.concat(stations, axis = 1)
    new_df = joined.sort_index().fillna(method='ffill')
    return new_df
