#project wicced python class
class wicced():
    import urllib
    import datetime as dt
    #constructor
    def __init__(self):
        self.server_url = 'https://udel-geoserver.nautilus.optiputer.net/geoserver/'
        self.workspace = 'cite'
        self.service = 'ows?service=WFS'
        self.version = 'version=1.0.0'
        self.request = 'request=GetFeature'
        self.feature_name = 'typeName=' + self.workspace + ':cema'
        self.format = 'outputFormat=application/json'
        self.query_start = 'CQL_FILTER='
        self.maxFeatures = 'maxFeatures=5000'
    ## addDate
    ## sets the specific date and time for retreival from the database
    ## params:
    ##    date - a string of the format YYYY-mm-dd HH:MM
    ## 
    def addDate(self, date):
        self.date = self.dt.datetime.strptime(date, '%Y-%m-%d %H:%M') 
    
    ## addDateRange
    ## sets a specific date range for retrieval
    ## params:
    ##   start - a string of the format YYYY-mm-dd HH:MM for the starting time
    ##   end - a string of the format YYYY-mm-dd HH:MM for the ending time 
    def addDateRange(self, start, end):
        self.start = self.dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
        self.end = self.dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    
    ## addDataType
    ## set the data type for retreival
    ## params:
    ##    type - a string containing the data type to be retreived
    def addDataType(self, type):
        self.data_type = type
        
    ## addBox
    ## add a bounding box to subset data retreived to a specific area
    ## params:
    ##    ul_lon - a number representing the Upper-Left longitude
    ##    ul_lat - a number representing the Upper-Left latitude
    ##    lr_lon - a number representing the Lower-Right longitude
    ##    lr_lat - a number representing the Lower-Right latitude
    def addBox(self, ul_lon, ul_lat, lr_lon, lr_lat):
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
        self.format = "outputFormat=" + format
        
    ## buildUrl
    ## pulls the input user selections together to create a URL for retreiving data
    ## Params: None
    ## Return Value: a string containing the encoded URL
    def buildUrl(self):
        print('building_url')
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
            print('ADDING BOUNDING BOX')
            if not query_string:
                query_string = "bbox(geom," + ",".join([str(self.ul_lon),str(self.ul_lat),str(self.lr_lon),str(self.lr_lat)])+")"
            else:
                query_string = query_string + " and bbox(geom," + ",".join([str(self.ul_lon),str(self.ul_lat),str(self.lr_lon),str(self.lr_lat)])+")"            
        if query_string != '':
            return (full_url + "&" + self.query_start + self.urllib.parse.quote(query_string, "="))
        else:
          return (full_url + "&" + query_string)
        