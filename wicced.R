#globals - don't adjust these
wicced.server_url = 'https://udel-geoserver.nautilus.optiputer.net/geoserver/'
wicced.workspace = 'cite'
wicced.service = 'ows?service=WFS'
wicced.version = 'version=1.0.0'
wicced.request = 'request=GetFeature'
wicced.query_start = 'CQL_FILTER='

#User configurable variables
#change cema to one of the other database names to pull data from other sources
#current valid options: cema, dgs_well, usgs
wicced.database_name = 'cema'
wicced.feature_name = sprintf("typeName=%s:%s", as.character(wicced.workspace), as.character(wicced.database_name))
#change the output format, default is geojson for use with the geojsonR package
#other options: csv
wicced.format = 'outputFormat=application/json'
#maxiumum number of data points to return
wicced.maxFeatures = 'maxFeatures=5000'

## function addDate ###########################################
## used for retrieving a SINGLE timestamp from the database
## Note: use this or addDateRange NOT both
## Params:
##   date  - MUST be of the form YYYY-MM-DD HH24:mm
##           where YYYY - 4 digit year, MM - 2 digit month, DD - 2 digit day of month
##           HH24 - 2 digit hour of the day(on a 24 hour clock), mm - 2 digit minute
wicced.addDate <- function(date){
  wicced.date <<- strptime(date, '%Y-%m-%d %H:%M') 
}

## function addDateRange ####################################
## used for retrieving a range of dates from the database
## Note: use this or addDate NOT both
## Params:
##   date - MUST be of the form YYYY-MM-DD HH24:mm
##          where YYYY - 4 digit year, MM - 2 digit month, DD - 2 digit day of month
##          HH24 - 2 digit hour of the day(on a 24 hour clock), mm - 2 digit minute
wicced.addDateRange <- function(start, end){
  wicced.start <<- strptime(start, '%Y-%m-%d %H:%M')
  wicced.end <<- strptime(end, '%Y-%m-%d %H:%M')
}

## function addDataType #####################################
## retreive a specific data type from the system
## Params
##   type - string containing the data type name to be retreived
##          current valid types are:
##          Air Temperature, Wind Speed, Wind Direction, Barometric Pressure, Solar Radiation, Wind Gust Speed (5), 
##          Gage Precipitation (5), Relative humidity
wicced.addDataType <- function(type){
  wicced.data_type <<- type
}

## function addBox ###########################################
## limit data returns to within the supplied lat/lon coordinates
## Params
##   ul_lon - upper left longitude
##   ul_lat - upper left latitude
##   lr_lon - lower right longitude
##   lr_lat - lower right latitude
wicced.addBox <- function(ul_lon, ul_lat, lr_lon, lr_lat){
  wicced.ul_lon <<- ul_lon
  wicced.lr_lon <<- lr_lon
  wicced.ul_lat <<- ul_lat
  wicced.lr_lat <<- lr_lat
}

## function changeFormat ######################################
## change the format of the returned data
## Params
##    format - a string containing the desired format
##             valid options are application/json or csv
wicced.changeFormat <- function(format){
  wicced.format <<- sprintf("outputFormat=%s", format)
}

## function buildUrl ##########################################
## pieces together server parameters and user supplied input to make the data url
## use the returned URL to retrieve data from the system
## Params: None
## Returns: character string containing the server url to retrieve data
wicced.buildUrl <- function(){
  full_url = sprintf("%s/%s/%s", wicced.server_url, wicced.workspace, wicced.service)
  full_url = sprintf("%s&%s&%s&%s&%s&%s", full_url, wicced.version, wicced.request, wicced.feature_name, wicced.maxFeatures, wicced.format)
  if(exists('wicced.date')){
    query_string = sprintf("dtg='%s'", format(wicced.date, '%Y-%m-%dT%H:%M:00Z'))
  }else if(exists('wicced.start') && exists('wicced.end')){
    query_string = sprintf("dtg between '%s' and '%s'", format(wicced.start, '%Y-%m-%dT%H:%M:00Z'), format(wicced.end, '%Y-%m-%dT%H:%M:00Z'))
  }
  if(exists('wicced.data_type')){
    if(exists('query_string')){
      query_string = sprintf("%s and type='%s'", query_string, wicced.data_type)
    }else{
      query_string = sprintf("type='%s'", wicced.data_type)
    }
  }
  if(exists('wicced.ul_lon')){
    if(exists('query_string')){
      query_string = sprintf("%s and bbox(geom,%f,%f,%f,%f)", query_string, wicced.ul_lon, wicced.ul_lat, wicced.lr_lon, wicced.lr_lat)
    }else{
      query_string = sprintf("bbox(geom,%f,%f,%f,%f)", wicced.ul_lon, wicced.ul_lat, wicced.lr_lon, wicced.lr_lat)
    }
  }
  if(exists('query_string')){
    full_url = sprintf("%s&%s%s", full_url, wicced.query_start, URLencode(query_string))
  }
  return(full_url)
}

## function reset
## Resets the environment for a subsequent call(building more then one url)
## This should be called after using buildUrl
## Params: None
## Return: None
wicced.reset <- function(){
  if(exists('wicced.date'))
    rm('wicced.date', pos='.GlobalEnv')
  if(exists('wicced.start'))
    rm('wicced.start', pos='.GlobalEnv')
  if(exists('wicced.end'))
    rm('wicced.end', pos='.GlobalEnv')
  if(exists('wicced.lr_lat'))
    rm('wicced.lr_lat', pos='.GlobalEnv')
  if(exists('wicced.lr_lon'))
    rm('wicced.lr_lon', pos='.GlobalEnv')
  if(exists('wicced.ul_lat'))
    rm('wicced.ul_lat', pos='.GlobalEnv')
  if(exists('wicced.ul_lon'))
    rm('wicced.ul_lon', pos='.GlobalEnv')
}