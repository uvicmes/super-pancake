#alphabuild
import csv
import datetime
import glob
import json
import os
import numpy as np

import numpy as np
import pandas as pd
from dateutil import parser
from jdcal import gcal2jd
from netCDF4 import Dataset, date2num


def realorarchive(date_created, date_processed):
    date_created = parser.parse(date_created)
    date_processed = parser.parse(date_processed)

    difference = date_processed - date_created
    difference = difference.days
    print(difference)
    if difference > 1:
        return "archive"

    else:
        return "realtime"

def latestFileinDirectory(srcpath):
    # get latest file in directory
    list_of_files = os.listdir(srcpath)
    paths = [os.path.join(srcpath, basename) for basename in list_of_files]
    latest_file = max(paths, key=os.path.getctime)
    # print(latest_file)
    return latest_file

def csv2json(srcpath, outpath):
    csvsource = latestFileinDirectory(srcpath)
    data = []
    with open(csvsource) as f:
        for row in csv.DictReader(f):
            data.append(row)
        f.close()

    with open(outpath + "latestBuoydata.json", 'w') as f:
        json.dump(data[0], f)
        f.close()

    with open(outpath + "latestBuoydata.json", 'r+') as f:
        old = f.read()
        f.seek(0)
        f.write("window.data = " + old)
        f.close()

def convert2nc(srcpath, outpath):
    # convert latest file to nc
    global day
    latestcsv = latestFileinDirectory(srcpath)
    files = sorted(glob.glob(srcpath + "*.csv"))

    #print(latestcsv[-31:-4])

    for file in files:
        print(file)
        rightnow_datetime = datetime.datetime.utcnow()
        rightnow_date_fmt = rightnow_datetime.strftime("%Y-%m-%d")
        rightnow_year = rightnow_datetime.year
        rightnow_month = rightnow_datetime.month
        rightnow_day = rightnow_datetime.day
        rightnow_time = rightnow_datetime.strftime("%H:%M:%S")
        rightnow_datetime_fmt = str(rightnow_year) + "-" + str(rightnow_month) + "-" + str(rightnow_day) + "T" + str(
            rightnow_time) + "Z"
        print(rightnow_datetime_fmt)

        csvdf = pd.read_csv(file, na_filter=True, header=None, delimiter=',', index_col=None, skiprows=1)
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        csvdfshape = csvdf.shape
        print(csvdfshape)
        staticstrdate = csvdf[1][1]
        dateinUTC = parser.parse(staticstrdate)
        date_fmt = dateinUTC.strftime("%Y-%m-%d")

        latitude, longitude = csvdf[3][1], csvdf[4][1]

        time, wspd, wdir = [], [], []
        gst, presv, atmp = [], [], []
        rehu, rain, hail = [], [], []
        battv, instdepth, insthead = [], [], []
        instpitch, instroll, instpres = [], [], []

        evb1, evb2, evb3 = [], [], []
        evb4, evb5, evb6 = [], [], []
        evb7, evb8, evb9 = [], [], []
        evb10, evb11, evb12 = [], [], []
        evb13, evb14, evb15 = [], [], []
        evb16, evb17, evb18 = [], [], []
        evb19, evb20 = [], []
        totalevb = []

        nvb1, nvb2, nvb3 = [], [], []
        nvb4, nvb5, nvb6 = [], [], []
        nvb7, nvb8, nvb9 = [], [], []
        nvb10, nvb11, nvb12 = [], [], []
        nvb13, nvb14, nvb15 = [], [], []
        nvb16, nvb17, nvb18 = [], [], []
        nvb19, nvb20 = [], []
        totalnvb = []

        mcspd, mcdir = [], []

        pgb1, pgb2, pgb3 = [], [], []
        pgb4, pgb5, pgb6 = [], [], []
        pgb7, pgb8, pgb9 = [], [], []
        pgb10, pgb11, pgb12 = [], [], []
        pgb13, pgb14, pgb15 = [], [], []
        pgb16, pgb17, pgb18 = [], [], []
        pgb19, pgb20 = [], []

        EA01B01, EA02B01, EA03B01 = [], [], []
        EA01B02, EA02B02, EA03B02 = [], [], []
        EA01B03, EA02B03, EA03B03 = [], [], []
        EA01B04, EA02B04, EA03B04 = [], [], []
        EA01B05, EA02B05, EA03B05 = [], [], []
        EA01B06, EA02B06, EA03B06 = [], [], []
        EA01B07, EA02B07, EA03B07 = [], [], []
        EA01B08, EA02B08, EA03B08 = [], [], []
        EA01B09, EA02B09, EA03B09 = [], [], []
        EA01B10, EA02B10, EA03B10 = [], [], []
        EA01B11, EA02B11, EA03B11 = [], [], []
        EA01B12, EA02B12, EA03B12 = [], [], []
        EA01B13, EA02B13, EA03B13 = [], [], []
        EA01B14, EA02B14, EA03B14 = [], [], []
        EA01B15, EA02B15, EA03B15 = [], [], []
        EA01B16, EA02B16, EA03B16 = [], [], []
        EA01B17, EA02B17, EA03B17 = [], [], []
        EA01B18, EA02B18, EA03B18 = [], [], []
        EA01B19, EA02B19, EA03B19 = [], [], []
        EA01B20, EA02B20, EA03B20 = [], [], []

        for index, row in csvdf.iterrows():

            strtime = csvdf[2][index]
            datetimeinUTC = parser.parse(staticstrdate + ' ' + strtime)
            time_units = 'minutes since 1970-01-01 00:00:00 UTC'
            nc_datetime = round(date2num(datetimeinUTC, time_units))


            '''
            print(datetimeinUTC)
            print(nc_datetime)
            year = datetimeinUTC.timetuple().tm_year
            month = datetimeinUTC.timetuple().tm_mon
            day = datetimeinUTC.timetuple().tm_mday
            hour = datetimeinUTC.timetuple().tm_hour
            min = datetimeinUTC.timetuple().tm_min
            sec = datetimeinUTC.timetuple().tm_sec

            dategreg2julian = gcal2jd(year, month, day)[0] + gcal2jd(year, month, day)[1]
            timegreg2julian = ((hour / 24) + (min / (24 * 60)) + (sec / (3600 * 24)))
            datetimejulian = dategreg2julian + timegreg2julian
            '''

            time.append(float(nc_datetime))

            wspd.append((csvdf[5][index])), wdir.append((csvdf[6][index])), gst.append((csvdf[7][index]))
            presv.append((csvdf[8][index])), atmp.append((csvdf[9][index])), rehu.append((csvdf[10][index]))
            rain.append((csvdf[11][index])), hail.append((csvdf[12][index])), battv.append((csvdf[13][index]))

            instdepth.append((csvdf[14][index])), insthead.append((csvdf[15][index])), instpitch.append((csvdf[16][index]))
            instroll.append((csvdf[17][index])), instpres.append((csvdf[18][index]))
           
            evb1.append((csvdf[19][index])), nvb1.append((csvdf[20][index])), evb2.append((csvdf[21][index])), nvb2.append((csvdf[22][index]))
            evb3.append((csvdf[23][index])), nvb3.append((csvdf[24][index])), evb4.append((csvdf[25][index])), nvb4.append((csvdf[26][index]))
            evb5.append((csvdf[27][index])), nvb5.append((csvdf[28][index])), evb6.append((csvdf[29][index])), nvb6.append((csvdf[30][index]))
            evb7.append((csvdf[31][index])), nvb7.append((csvdf[32][index])), evb8.append((csvdf[33][index])), nvb8.append((csvdf[34][index]))
            evb9.append((csvdf[35][index])), nvb9.append((csvdf[36][index])), evb10.append((csvdf[37][index])), nvb10.append((csvdf[38][index]))
            evb11.append((csvdf[39][index])), nvb11.append((csvdf[40][index])), evb12.append((csvdf[41][index])), nvb12.append((csvdf[42][index]))
            evb13.append((csvdf[41][index])), nvb13.append((csvdf[44][index])), evb14.append((csvdf[45][index])), nvb14.append((csvdf[46][index]))
            evb15.append((csvdf[45][index])), nvb15.append((csvdf[48][index])), evb16.append((csvdf[49][index])), nvb16.append((csvdf[50][index]))
            evb17.append((csvdf[49][index])), nvb17.append((csvdf[52][index])), evb18.append((csvdf[53][index])), nvb18.append((csvdf[54][index]))
            evb19.append((csvdf[51][index])), nvb19.append((csvdf[56][index])), evb20.append((csvdf[57][index])), nvb20.append((csvdf[58][index]))

            mcspd.append((csvdf[59][index])), mcdir.append((csvdf[60][index]))

            pgb1.append((csvdf[61][index])), pgb2.append((csvdf[62][index])), pgb3.append((csvdf[63][index]))
            pgb4.append((csvdf[64][index])), pgb5.append((csvdf[65][index])), pgb6.append((csvdf[66][index]))
            pgb7.append((csvdf[67][index])), pgb8.append((csvdf[68][index])), pgb9.append((csvdf[69][index]))
            pgb10.append((csvdf[70][index])), pgb11.append((csvdf[71][index])), pgb12.append((csvdf[72][index]))
            pgb13.append((csvdf[73][index])), pgb14.append((csvdf[74][index])), pgb15.append((csvdf[75][index]))
            pgb16.append((csvdf[76][index])), pgb17.append((csvdf[77][index])), pgb18.append((csvdf[78][index]))
            pgb19.append((csvdf[79][index])), pgb20.append((csvdf[80][index]))

            EA01B01.append((csvdf[81][index])), EA02B01.append((csvdf[82][index])), EA03B01.append((csvdf[83][index]))
            EA01B02.append((csvdf[84][index])), EA02B02.append((csvdf[85][index])), EA03B02.append((csvdf[86][index]))
            EA01B03.append((csvdf[87][index])), EA02B03.append((csvdf[88][index])), EA03B03.append((csvdf[89][index]))
            EA01B04.append((csvdf[90][index])), EA02B04.append((csvdf[91][index])), EA03B04.append((csvdf[92][index]))
            EA01B05.append((csvdf[93][index])), EA02B05.append((csvdf[94][index])), EA03B05.append((csvdf[95][index]))
            EA01B06.append((csvdf[96][index])), EA02B06.append((csvdf[97][index])), EA03B06.append((csvdf[98][index]))
            EA01B07.append((csvdf[99][index])), EA02B07.append((csvdf[100][index])), EA03B07.append((csvdf[101][index]))
            EA01B08.append((csvdf[102][index])), EA02B08.append((csvdf[103][index])), EA03B08.append((csvdf[104][index]))
            EA01B09.append((csvdf[105][index])), EA02B09.append((csvdf[106][index])), EA03B09.append((csvdf[107][index]))
            EA01B10.append((csvdf[108][index])), EA02B10.append((csvdf[109][index])), EA03B10.append((csvdf[110][index]))
            EA01B11.append((csvdf[111][index])), EA02B11.append((csvdf[112][index])), EA03B11.append((csvdf[113][index]))
            EA01B12.append((csvdf[114][index])), EA02B12.append((csvdf[115][index])), EA03B12.append((csvdf[116][index]))
            EA01B13.append((csvdf[117][index])), EA02B13.append((csvdf[118][index])), EA03B13.append((csvdf[119][index]))
            EA01B14.append((csvdf[120][index])), EA02B14.append((csvdf[121][index])), EA03B14.append((csvdf[122][index]))
            EA01B15.append((csvdf[123][index])), EA02B15.append((csvdf[124][index])), EA03B15.append((csvdf[125][index]))
            EA01B16.append((csvdf[126][index])), EA02B16.append((csvdf[127][index])), EA03B16.append((csvdf[128][index]))
            EA01B17.append((csvdf[129][index])), EA02B17.append((csvdf[130][index])), EA03B17.append((csvdf[131][index]))
            EA01B18.append((csvdf[132][index])), EA02B18.append((csvdf[133][index])), EA03B18.append((csvdf[134][index]))
            EA01B19.append((csvdf[135][index])), EA02B19.append((csvdf[136][index])), EA03B19.append((csvdf[137][index]))
            EA01B20.append((csvdf[138][index])), EA02B20.append((csvdf[139][index])), EA03B20.append((csvdf[140][index]))

        print(file[-25:-4])
        print(len(totalnvb))
        print(totalnvb)

        dataset = Dataset(outpath + file[-25:-4] + ".nc", 'w', format="NETCDF4_CLASSIC")
        dataset.project = "CARICOOS"
        dataset.title = "Crown Bay Weather Station and ADCP Data."
        dataset.institution = "University of the Virgin Islands"
        dataset.institution_abbreviation = "UVI"
        dataset.institution_dept = "Center for Marine & Environmental Studies"
        dataset.naming_authority = "https://www.caricoos.org/"
        dataset.authors = "Ocean Labs"
        dataset.creator_institution = "University of the Virgin Islands"
        dataset.creator_sector = "academic"
        dataset.creator_name = "Andy Breton"
        dataset.creator_phone = "(340) 776-9200"
        dataset.creator_url = "https://www.uvi.edu/research/center-for-marine-environmental-studies/default.aspx"
        dataset.creator_email = "andy.bretonperalta@uvi.edu"
        dataset.creator_country = "United States Virgin Islands"
        dataset.creator_state = "Virgin Islands (STT)"
        dataset.creator_city = "Charlotte Amalie"
        dataset.creator_address = "2 John Brewers Bay"
        dataset.creator_postalcode = "00802-6004"
        dataset.contributor_name = "Dr. Jorge Capella (CARICOOS)"
        dataset.contributor_role = "DMAC, Scientist, & Compliance"
        dataset.contributor_email = "jorge.capella@upr.edu"
        dataset.contributor_url = "www.caricoos.org"
        dataset.source = "www.sutronwin.com/goesweb/uvidock/?C=N;O=D"
        dataset.license = "There are no restrictions placed on these data."
        dataset.citation = "The Department of Marine & Environmental Studies of UVI should be cited as the source of " \
                           "the data provided."
        dataset.acknowledgement = "Dr. Sennai Habtes (UVI) and OCOVI"

        dataset.summary = "Historical six-minute mean values of meteorological data and horizontal current profiles from a " \
                              "\nstation located on the VI Port Authority Dock at Crown Bay, St. Thomas, US Virgin Islands, USA."

        dataset.station_name = "Crown Bay Marina Weather Station - Crown Bay Marina, Charlotte Amalie West, St Thomas 00802"
        dataset.station_id = "Virgin Islands (STT) CrownBay Weather Station w/ ADCP (WXT520 w/ H-ADCP)"
        dataset.publisher_name = "CARICOOS"
        dataset.publisher_country = "United States of America"
        dataset.publisher_state = "PR"
        dataset.publisher_city = "Mayaguez"
        dataset.publisher_address = "Road 108, KM 1.0 Bo. Miradero"
        dataset.publisher_postalcode = "00680"
        dataset.publisher_institution = "UPRM R&D Center"
        dataset.publisher_phone = "(787) 832­4040 x6454"
        dataset.publisher_url = "www.caricoos.org"
        dataset.publisher_email = "jorge.capella@upr.edu"
        dataset.history = "added headers to original CSV files from sutron source, historical data concatinated at 6 minute intevals " \
                          "and converted to netCDF using Python netCDF4."
        dataset.keywords = "Atmospheric Pressure, Sea level Pressure, Atmospheric Temperature, Surface Temperature, " \
                           "Humidity, Surface Winds, Ocean Winds, Ocean Currents"
        dataset.keywords_vocabulary = "GCMD Science Keywords"
        #dataset.standard_name_vocabulary = "CF-1.6"
        dataset.Conventions = "IOOS 1.2, CF-1.6"
        dataset.infoUrl = "https://www.caricoos.org/"
        #dataset.geospatial_bounds =
        dataset.geospatial_lat_min = latitude
        dataset.geospatial_lat_max = latitude
        dataset.geospatial_lat_units = "degrees_north"
        dataset.geospatial_lon_min = longitude
        dataset.geospatial_lon_max = longitude
        dataset.geospatial_lon_units = "degrees_east"
        dataset.geospatial_vertical_min = 0.0
        dataset.geospatial_vertical_max = 0.0
        dataset.geospatial_vertical_positive = "up"
        dataset.geospatial_vertial_units = "meters above mean sea level"
        dataset.sea_name = "Caribbean Sea"
        dataset.platform = "platform"
        dataset.platform_id = "N/A"
        dataset.platform_name = "Crown Bay Weather Station"
        dataset.platform_type = "Stationary platform cement structure"
        dataset.platform_vocabulary = "N/A"
        dataset.date_created = "2020-10-05"#date_fmt+'Z'
        dataset.time_coverage_start = "2019-08-05T00:00:00Z"#date_fmt + "T00:00:00Z"
        #dataset.date_issued = #date_fmt+'Z'
        dataset.time_coverage_end = "2019-12-31T23:54:00Z"#date_fmt+"T23:54:00Z"
        dataset.time_zone = "UTC"
        #dataset.date_modified = #rightnow_datetime_fmt
        #dataset.time_coverage_duration = "6 minutes"
        dataset.instrument = "met & ADCP"
        dataset.met_vendor = "VAISALA & Teledyne RD Instruments"
        dataset.met_model = "WXT520"
        dataset.met_manual = "https://www.vaisala.com/sites/default/files/documents/M210906EN-C.pdf"
        dataset.adcp_vendor = "Teledyne RD Instruments"
        dataset.adcp_model = "H-ADCP 300 kHz Horizontal ADCP."
        dataset.adcp_manual = "http://www.teledynemarine.com/Lists/Downloads/hadcp_datasheet_lr.pdf"
        dataset.processing_mode = "Historical"  # realorarchive(date_fmt, rightnow_date_fmt)
        dataset.processing_level = "0"
        dataset.comment = "The realtime status is only considered when the it has been less than " \
                          "30 days of its generation."
        dataset.references = "http://sutronwin.com/goesweb/uvidock/"

        dataset.createDimension('time', None)
        dataset.createDimension('depth', len(instdepth))
        dataset.createDimension('lon', 1)
        dataset.createDimension('lat', 1)

        times = dataset.createVariable("time", "f8", ('time',), fill_value="NaN")
        times.long_name = "Measurement Time"
        times.standard_name = "time"
        times.short_name = "time"
        times.observation_type = "measured"
        times.calendar = "gregorian"
        times.origin = "1970-01-01 00:00:00 UTC"
        times.units = "minutes since 1970-01-01 00:00:00 UTC"
        times.ioos_category = "time"
        times.axis = "T"
        times.missing_value = "NaN"
        times.comment = "Coordinate variable"
        times.references = "https://www.programcreek.com/python/example/89490/netCDF4.date2num"
        times.note = ""
        times[:] = time

        lon = dataset.createVariable("longitude", 'f8', ('lon',), fill_value="NaN")
        lon.long_name = "Longitude"
        lon.stardard_name = "longitude"
        #lon.short_name = "lon"
        lon.units = "degrees_west"
        lon.ioos_category = "Location"
        #lon.valid_range = [-180, 180]
        lon.actual_range = [-64.95135, -64.95135]
        lon.valid_min = -180
        lon.valid_max = 180
        lon.axis = "X"
        lon.comment = "Coordinate variable"
        lon[:] = longitude
        
        lat = dataset.createVariable("latitude", 'd', ('lat',), fill_value="NaN")
        lat.long_name = "Latitude"
        lat.standard_name = "latitude"
        lat.short_name = "lat"
        lat.units = "degrees_north"
        lat.ioos_category = "Location"
        lat.valid_range = -90., 90.
        lat.actual_range = [18.331414, 18.331414]
        lat.axis = "Y"
        lat.comment = "Coordinate variable"
        lat[:] = latitude

        depth = dataset.createVariable("depth", "f8", ("depth",), fill_value="NaN")
        depth.long_name = "Instrument Depth"
        depth.standard_name = "depth"
        depth.axis = "Z"
        depth.observation_type = "measured"
        depth.units = "meter"
        #depth.actual_range =
        depth.accuracy = 0.1
        depth.ioos_category = "Location"
        depth.missing_value = "NaN"
        depth.positive = "down"
        depth.comment = "Coordinate variable"
        depth[:] = instdepth

        barometric_pressure = dataset.createVariable("air_pressure", "f8", ("time",), fill_value="NaN")
        barometric_pressure.long_name = "Barometric Pressure"
        barometric_pressure.standard_name = "air_pressure"
        #barometric_pressure.short_name = "BP"
        # barometric_pressure.ancillary_variables = "barometric_pressure_qc"
        barometric_pressure.observation_type = "measured"
        barometric_pressure.units = "hPa"
        barometric_pressure.range = [600, 1100]
        barometric_pressure.actual_range = [999.5, 1018.7]
        #barometric_pressure.resolution = "0.1 hPa"
        #barometric_pressure.is_dead = 0
        barometric_pressure.ioos_category = "Wind"
        barometric_pressure.missing_value = "NaN"
        barometric_pressure[:] = presv

        wind_speed = dataset.createVariable("wind_speed", "f8", ("time", "lon", "lat",), fill_value="NaN")
        wind_speed.long_name = "Wind Speed"
        wind_speed.standard_name = "wind_speed"
        wind_speed.short_name = "WSPD"
        # wind_speed.valid_range = "0.f", "50.f"
        wind_speed.observation_type = "measured"
        wind_speed.units = "knots"
        wind_speed.range = [0, 60]
        #wind_speed.actual_range =
        wind_speed.response_time = "0.25 s"
        wind_speed.accuracy = "+/- 3% at 10 m/s"
        wind_speed.resolution = "0.1 m/s"
        wind_speed.ioos_category = "Wind"
        wind_speed.missing_value = "NaN"
        wind_speed[:, 0, 0] = wspd

        wind_direction = dataset.createVariable("wind_from_direction", "f8", ("time", "lon", "lat",), fill_value="NaN")
        wind_direction.long_name = "Wind Direction"
        wind_direction.standard_name = "wind_from_direction"
        # wind_direction.ancillary_variables = "wind_direction_qc"
        #wind_direction.short_name = "WDIR"
        #wind_direction.dependency = "wind_speed"
        wind_direction.observation_type = "measured"
        wind_direction.units = "degrees"
        wind_direction.range = [0, 359]
        wind_direction.response_time = "0.25 s"
        wind_direction.accuracy = "+/- 3.0 degrees"
        wind_direction.resolution = "1 degree"
        wind_direction.ioos_category = "Wind"
        wind_direction.missing_value = "NaN"
        wind_direction[:, 0, 0] = wdir

        wind_gust = dataset.createVariable("wind_speed_of_gust", "f8", ("time", "lon", "lat",), fill_value="NaN")
        wind_gust.long_name = "Wind Gust Speed"
        wind_gust.standard_name = "wind_speed_of_gust"
        wind_gust.units = "knots"
        wind_gust.range = [0, 60]
        wind_gust.valid_range = [0, 50]
        wind_gust.observation_type = "measured"
        wind_gust.precision = 0.001
        wind_gust.accuracy = 0.1
        wind_gust.ioos_category = "Wind"
        wind_gust.missing_value = "NaN"
        wind_gust[:, 0, 0] = gst

        air_temperature = dataset.createVariable("air_temperature", "f8", ("time", "lon", "lat",), fill_value="NaN")
        air_temperature.long_name = "Air Temperature"
        air_temperature.standard_name = "air_temperature"
        #air_temperature.short_name = "AT"
        air_temperature.observation_type = "measured"
        air_temperature.units = "degree_Celsius"
        air_temperature.range = [-52, 60]
        # air_temperature.valid_range = -5.f, 40.f;
        air_temperature.accuracy = "+/- 0.3"
        air_temperature.resolution = "0.1"
        air_temperature.ioos_category = "Temperature"
        air_temperature.missing_value = "NaN"
        air_temperature[:, 0, 0] = atmp

        relative_humidity = dataset.createVariable("relative_humidity", "f8", ("time", "lon", "lat",), fill_value="NaN")
        relative_humidity.long_name = "Relative Humidity"
        relative_humidity.standard_name = "relative_humidity"
        #relative_humidity.short_name = "RH"
        relative_humidity.units = "percent"
        relative_humidity.observation_type = "measured"
        relative_humidity.range = [0, 100]
        #relative_humidity.accuracy = "+/- 3 %RH at 0 ... 90 %RH AND/OR +/- 5 %RH at 90 ... 100 %RH"
        relative_humidity.resolution = 0.1
        relative_humidity.measuring_interval = [1, 3600]
        relative_humidity.ioos_category = "Meteorology"
        relative_humidity.missing_value = "NaN"
        relative_humidity[:, 0, 0] = rehu

        rain_intensity = dataset.createVariable("rainfall_rate", "f8", ("time", "lon", "lat",), fill_value="NaN")
        rain_intensity.long_name = "Precipitation Rate"
        rain_intensity.standard_name = "rainfall_rate"
        #rain_intensity.short_name = "RAIN"
        rain_intensity.units = "in/h"
        rain_intensity.observation_type = "measured"
        rain_intensity.range = [0, 200]
        rain_intensity.ioos_category = "Meteorology"
        rain_intensity.missing_value = "NaN"
        rain_intensity[:, 0, 0] = rain

        '''hail_intensity = dataset.createVariable("hail_intensity", "f8", ("time", "lon", "lat",), fill_value="NaN")
        hail_intensity.long_name = "Hail Precipitation Rate"
        hail_intensity.standard_name = "hail_intensity"
        #hail_intensity.short_name = "HAIL"
        hail_intensity.observation_type = "measured"
        hail_intensity.units = "hits/in^2"
        hail_intensity.ioos_category = "Meteorology"
        hail_intensity[:, 0, 0] = hail'''

        '''battery_voltage = dataset.createVariable("BATTV", "f8", ("time", "lon", "lat",), fill_value="NaN")
        battery_voltage.long_name = "Battery"
        battery_voltage.standard_name = "battery"
        battery_voltage.short_name = "BATTV"
        battery_voltage.observation_type = "measured"
        battery_voltage.units = "volts"
        battery_voltage[:, 0, 0] = battv'''

        instrument_heading = dataset.createVariable("heading", "f8", ("time", "lon", "lat",), fill_value="NaN")
        instrument_heading.long_name = "Platform Heading"
        #instrument_heading.standard_name = "heading"
        #instrument_heading.short_name = "heading"
        instrument_heading.units = "degrees" #magnetic
        instrument_heading.observation_type = "measured"
        instrument_heading.missing_value = "NaN"
        instrument_heading[:, 0, 0] = insthead

        instrument_pitch = dataset.createVariable("pitch", "f8", ("time", "lon", "lat",), fill_value="NaN")
        instrument_pitch.long_name = "Platform Pitch"
        #instrument_pitch.standard_name = "pitch"
        instrument_pitch.short_name = "pitch"
        instrument_pitch.units = "degrees"
        instrument_pitch.observation_type = "measured"
        instrument_pitch.missing_value = "NaN"
        instrument_pitch[:, 0, 0] = instpitch

        instrument_roll = dataset.createVariable("roll", "f8", ("time", "lon", "lat",), fill_value="NaN")
        instrument_roll.long_name = "Platform Roll"
        #instrument_roll.standard_name = "roll"
        #instrument_roll.short_name = "roll"
        instrument_roll.units = "degrees"
        instrument_roll.observation_type = "measured"
        instrument_roll.missing_value = "NaN"
        instrument_roll[:, 0, 0] = instroll

        instrument_pressure = dataset.createVariable("instrument_pres", "f8", ("time", "lon", "lat",), fill_value="NaN")
        instrument_pressure.long_name = "Platform Pressure"
        #instrument_pressure.standard_name = "pressure"
        instrument_pressure.short_name = "pres"
        instrument_pressure.units = "kPa"
        instrument_pressure.observation_type = "measured"
        instrument_pressure.missing_value = "NaN"
        instrument_pressure[:, 0, 0] = instpres

        east_velocity1 = dataset.createVariable("current_u_01", "f8", ("time", "lon", "lat",), fill_value="NaN")
        east_velocity1.long_name = "Eastward Sea Water Velocity"
        east_velocity1.standard_name = "eastward_sea_water_velocity"
        east_velocity1.short_name = "u"
        east_velocity1.units = "01 mm s-1"
        east_velocity1.observation_type = "measured"
        east_velocity1.missing_value = "NaN"
        east_velocity1.ioos_category = "Currents"
        east_velocity1[:, 0, 0] = evb1

        north_velocity1 = dataset.createVariable("current_v_01", "f8", ("time", "lon", "lat",), fill_value="NaN")
        north_velocity1.long_name = "Northward Sea Water Velocity"
        north_velocity1.standard_name = "northward_sea_water_velocity"
        north_velocity1.short_name = "v"
        north_velocity1.units = "01 mm s-1"
        north_velocity1.observation_type = "measured"
        north_velocity1.ioos_category = "Currents"
        north_velocity1.missing_value = "NaN"
        north_velocity1[:, 0, 0] = nvb1

        '''east_velocity2 = dataset.createVariable("current_u_02", "f8", ("time", "lon", "lat",))
        east_velocity2.long_name = "Eastward Sea Water Velocity"
        east_velocity2.standard_name = "eastward_sea_water_velocity"
        east_velocity2.short_name = "u"
        east_velocity2.units = "01 mm s-1"
        east_velocity2.observation_type = "measured"
        east_velocity2.ioos_category = "Currents"
        east_velocity2.is_dead = "NaN"
        east_velocity2[:, 0, 0] = evb2

        north_velocity2 = dataset.createVariable("current_v_02", "f8", ("time", "lon", "lat",))
        north_velocity2.long_name = "Northward Sea Water Velocity"
        north_velocity2.standard_name = "northward_sea_water_velocity"
        north_velocity2.short_name = "v"
        north_velocity2.units = "01 mm s-1"
        north_velocity2.observation_type = "measured"
        north_velocity2.ioos_category = "Currents"
        north_velocity2.is_dead = "NaN"
        north_velocity2[:, 0, 0] = nvb2

        east_velocity3 = dataset.createVariable("current_u_03", "f8", ("time", "lon", "lat",))
        east_velocity3.long_name = "Eastward Sea Water Velocity"
        east_velocity3.standard_name = "eastward_sea_water_velocity"
        east_velocity3.short_name = "u"
        east_velocity3.units = "01 mm s-1"
        east_velocity3.observation_type = "measured"
        east_velocity3.ioos_category = "Currents"
        east_velocity3.is_dead = "NaN"
        east_velocity3[:, 0, 0] = evb3

        north_velocity3 = dataset.createVariable("current_v_03", "f8", ("time", "lon", "lat",))
        north_velocity3.long_name = "Northward Sea Water Velocity"
        north_velocity3.standard_name = "northward_sea_water_velocity"
        north_velocity3.short_name = "v"
        north_velocity3.units = "01 mm s-1"
        north_velocity3.observation_type = "measured"
        north_velocity3.ioos_category = "Currents"
        north_velocity3.is_dead = "NaN"
        north_velocity3[:, 0, 0] = nvb3

        east_velocity4 = dataset.createVariable("current_u_04", "f8", ("time", "lon", "lat",))
        east_velocity4.long_name = "Eastward Sea Water Velocity"
        east_velocity4.standard_name = "eastward_sea_water_velocity"
        east_velocity4.short_name = "u"
        east_velocity4.units = "01 mm s-1"
        east_velocity4.observation_type = "measured"
        east_velocity4.ioos_category = "Currents"
        east_velocity4.is_dead = "NaN"
        east_velocity4[:, 0, 0] = evb4

        north_velocity4 = dataset.createVariable("current_v_04", "f8", ("time", "lon", "lat",))
        north_velocity4.long_name = "Northward Sea Water Velocity"
        north_velocity4.standard_name = "northward_sea_water_velocity"
        north_velocity4.short_name = "v"
        north_velocity4.units = "01 mm s-1"
        north_velocity4.observation_type = "measured"
        north_velocity4.ioos_category = "Currents"
        north_velocity4.is_dead = "NaN"
        north_velocity4[:, 0, 0] = nvb4

        east_velocity5 = dataset.createVariable("current_u_05", "f8", ("time", "lon", "lat",))
        east_velocity5.long_name = "Eastward Sea Water Velocity"
        east_velocity5.standard_name = "eastward_sea_water_velocity"
        east_velocity5.short_name = "u"
        east_velocity5.units = "01 mm s-1"
        east_velocity5.observation_type = "measured"
        east_velocity5.ioos_category = "Currents"
        east_velocity5.is_dead = "NaN"
        east_velocity5[:, 0, 0] = evb5

        north_velocity5 = dataset.createVariable("current_v_05", "f8", ("time", "lon", "lat",))
        north_velocity5.long_name = "Northward Sea Water Velocity"
        north_velocity5.standard_name = "northward_sea_water_velocity"
        north_velocity5.short_name = "v"
        north_velocity5.units = "01 mm s-1"
        north_velocity5.observation_type = "measured"
        north_velocity5.ioos_category = "Currents"
        north_velocity5.is_dead = "NaN"
        north_velocity5[:, 0, 0] = nvb5

        east_velocity6 = dataset.createVariable("current_u_06", "f8", ("time", "lon", "lat",))
        east_velocity6.long_name = "Eastward Sea Water Velocity"
        east_velocity6.standard_name = "eastward_sea_water_velocity"
        east_velocity6.short_name = "u"
        east_velocity6.units = "01 mm s-1"
        east_velocity6.observation_type = "measured"
        east_velocity6.ioos_category = "Currents"
        east_velocity6.is_dead = "NaN"
        east_velocity6[:, 0, 0] = evb6

        north_velocity6 = dataset.createVariable("current_v_06", "f8", ("time", "lon", "lat",))
        north_velocity6.long_name = "Northward Sea Water Velocity"
        north_velocity6.standard_name = "northward_sea_water_velocity"
        north_velocity6.short_name = "v"
        north_velocity6.units = "01 mm s-1"
        north_velocity6.observation_type = "measured"
        north_velocity6.ioos_category = "Currents"
        north_velocity6.is_dead = "NaN"
        north_velocity6[:, 0, 0] = nvb6

        east_velocity7 = dataset.createVariable("current_u_07", "f8", ("time", "lon", "lat",))
        east_velocity7.long_name = "Eastward Sea Water Velocity"
        east_velocity7.standard_name = "eastward_sea_water_velocity"
        east_velocity7.short_name = "u"
        east_velocity7.units = "01 mm s-1"
        east_velocity7.observation_type = "measured"
        east_velocity7.ioos_category = "Currents"
        east_velocity7.is_dead = "NaN"
        east_velocity7[:, 0, 0] = evb7

        north_velocity7 = dataset.createVariable("current_v_07", "f8", ("time", "lon", "lat",))
        north_velocity7.long_name = "Northward Sea Water Velocity"
        north_velocity7.standard_name = "northward_sea_water_velocity"
        north_velocity7.short_name = "v"
        north_velocity7.units = "01 mm s-1"
        north_velocity7.observation_type = "measured"
        north_velocity7.ioos_category = "Currents"
        north_velocity7.is_dead = "NaN"
        north_velocity7[:, 0, 0] = nvb7

        east_velocity8 = dataset.createVariable("current_u_08", "f8", ("time", "lon", "lat",))
        east_velocity8.long_name = "Eastward Sea Water Velocity"
        east_velocity8.standard_name = "eastward_sea_water_velocity"
        east_velocity8.short_name = "u"
        east_velocity8.units = "01 mm s-1"
        east_velocity8.observation_type = "measured"
        east_velocity8.ioos_category = "Currents"
        east_velocity8.is_dead = "NaN"
        east_velocity8[:, 0, 0] = evb8

        north_velocity8 = dataset.createVariable("current_v_08", "f8", ("time", "lon", "lat",))
        north_velocity8.long_name = "Northward Sea Water Velocity"
        north_velocity8.standard_name = "northward_sea_water_velocity"
        north_velocity8.short_name = "v"
        north_velocity8.units = "01 mm s-1"
        north_velocity8.observation_type = "measured"
        north_velocity8.ioos_category = "Currents"
        north_velocity8.is_dead = "NaN"
        north_velocity8[:, 0, 0] = nvb8

        east_velocity9 = dataset.createVariable("current_u_09", "f8", ("time", "lon", "lat",))
        east_velocity9.long_name = "Eastward Sea Water Velocity"
        east_velocity9.standard_name = "eastward_sea_water_velocity"
        east_velocity9.short_name = "u"
        east_velocity9.units = "01 mm s-1"
        east_velocity9.observation_type = "measured"
        east_velocity9.ioos_category = "Currents"
        east_velocity9.is_dead = "NaN"
        east_velocity9[:, 0, 0] = evb9

        north_velocity9 = dataset.createVariable("current_v_09", "f8", ("time", "lon", "lat",))
        north_velocity9.long_name = "Northward Sea Water Velocity"
        north_velocity9.standard_name = "northward_sea_water_velocity"
        north_velocity9.short_name = "v"
        north_velocity9.units = "01 mm s-1"
        north_velocity9.observation_type = "measured"
        north_velocity9.ioos_category = "Currents"
        north_velocity9.is_dead = "NaN"
        north_velocity9[:, 0, 0] = nvb9

        east_velocity10 = dataset.createVariable("current_u_10", "f8", ("time", "lon", "lat",))
        east_velocity10.long_name = "Eastward Sea Water Velocity"
        east_velocity10.standard_name = "eastward_sea_water_velocity"
        east_velocity10.short_name = "u"
        east_velocity10.units = "01 mm s-1"
        east_velocity10.observation_type = "measured"
        east_velocity10.ioos_category = "Currents"
        east_velocity10.is_dead = "NaN"
        east_velocity10[:, 0, 0] = evb10

        north_velocity10 = dataset.createVariable("current_v_10", "f8", ("time", "lon", "lat",))
        north_velocity10.long_name = "Northward Sea Water Velocity"
        north_velocity10.standard_name = "northward_sea_water_velocity"
        north_velocity10.short_name = "v"
        north_velocity10.units = "01 mm s-1"
        north_velocity10.observation_type = "measured"
        north_velocity10.ioos_category = "Currents"
        north_velocity10.is_dead = "NaN"
        north_velocity10[:, 0, 0] = nvb10

        east_velocity11 = dataset.createVariable("current_u_11", "f8", ("time", "lon", "lat",))
        east_velocity11.long_name = "Eastward Sea Water Velocity"
        east_velocity11.standard_name = "eastward_sea_water_velocity"
        east_velocity11.short_name = "u"
        east_velocity11.units = "01 mm s-1"
        east_velocity11.observation_type = "measured"
        east_velocity11.ioos_category = "Currents"
        east_velocity11.is_dead = "NaN"
        east_velocity11[:, 0, 0] = evb11

        north_velocity11 = dataset.createVariable("current_v_11", "f8", ("time", "lon", "lat",))
        north_velocity11.long_name = "Northward Sea Water Velocity"
        north_velocity11.standard_name = "northward_sea_water_velocity"
        north_velocity11.short_name = "v"
        north_velocity11.units = "01 mm s-1"
        north_velocity11.observation_type = "measured"
        north_velocity11.ioos_category = "Currents"
        north_velocity11.is_dead = "NaN"
        north_velocity11[:, 0, 0] = nvb11

        east_velocity12 = dataset.createVariable("current_u_12", "f8", ("time", "lon", "lat",))
        east_velocity12.long_name = "Eastward Sea Water Velocity"
        east_velocity12.standard_name = "eastward_sea_water_velocity"
        east_velocity12.short_name = "u"
        east_velocity12.units = "01 mm s-1"
        east_velocity12.observation_type = "measured"
        east_velocity12.ioos_category = "Currents"
        east_velocity12.is_dead = "NaN"
        east_velocity12[:, 0, 0] = evb12

        north_velocity12 = dataset.createVariable("current_v_12", "f8", ("time", "lon", "lat",))
        north_velocity12.long_name = "Northward Sea Water Velocity"
        north_velocity12.standard_name = "northward_sea_water_velocity"
        north_velocity12.short_name = "v"
        north_velocity12.units = "01 mm s-1"
        north_velocity12.observation_type = "measured"
        north_velocity12.ioos_category = "Currents"
        north_velocity12.is_dead = "NaN"
        north_velocity12[:, 0, 0] = nvb12

        east_velocity13 = dataset.createVariable("current_u_13", "f8", ("time", "lon", "lat",))
        east_velocity13.long_name = "Eastward Sea Water Velocity"
        east_velocity13.standard_name = "eastward_sea_water_velocity"
        east_velocity13.short_name = "u"
        east_velocity13.units = "01 mm s-1"
        east_velocity13.observation_type = "measured"
        east_velocity13.ioos_category = "Currents"
        east_velocity13.is_dead = "NaN"
        east_velocity13[:, 0, 0] = evb13

        north_velocity13 = dataset.createVariable("current_v_13", "f8", ("time", "lon", "lat",))
        north_velocity13.long_name = "Northward Sea Water Velocity"
        north_velocity13.standard_name = "northward_sea_water_velocity"
        north_velocity13.short_name = "v"
        north_velocity13.units = "01 mm s-1"
        north_velocity13.observation_type = "measured"
        north_velocity13.ioos_category = "Currents"
        north_velocity13.is_dead = "NaN"
        north_velocity13[:, 0, 0] = nvb13

        east_velocity14 = dataset.createVariable("current_u_14", "f8", ("time", "lon", "lat",))
        east_velocity14.long_name = "Eastward Sea Water Velocity"
        east_velocity14.standard_name = "eastward_sea_water_velocity"
        east_velocity14.short_name = "u"
        east_velocity14.units = "01 mm s-1"
        east_velocity14.observation_type = "measured"
        east_velocity14.ioos_category = "Currents"
        east_velocity14.is_dead = "NaN"
        east_velocity14[:, 0, 0] = evb14

        north_velocity14 = dataset.createVariable("current_v_14", "f8", ("time", "lon", "lat",))
        north_velocity14.long_name = "Northward Sea Water Velocity"
        north_velocity14.standard_name = "northward_sea_water_velocity"
        north_velocity14.short_name = "v"
        north_velocity14.units = "01 mm s-1"
        north_velocity14.observation_type = "measured"
        north_velocity14.ioos_category = "Currents"
        north_velocity14.is_dead = "NaN"
        north_velocity14[:, 0, 0] = nvb14

        east_velocity15 = dataset.createVariable("current_u_15", "f8", ("time", "lon", "lat",))
        east_velocity15.long_name = "Eastward Sea Water Velocity"
        east_velocity15.standard_name = "eastward_sea_water_velocity"
        east_velocity15.short_name = "u"
        east_velocity15.units = "01 mm s-1"
        east_velocity15.observation_type = "measured"
        east_velocity15.ioos_category = "Currents"
        east_velocity15.is_dead = "NaN"
        east_velocity15[:, 0, 0] = evb15

        north_velocity15 = dataset.createVariable("current_v_15", "f8", ("time", "lon", "lat",))
        north_velocity15.long_name = "Northward Sea Water Velocity"
        north_velocity15.standard_name = "northward_sea_water_velocity"
        north_velocity15.short_name = "v"
        north_velocity15.units = "01 mm s-1"
        north_velocity15.observation_type = "measured"
        north_velocity15.ioos_category = "Currents"
        north_velocity15.is_dead = "NaN"
        north_velocity15[:, 0, 0] = nvb15

        east_velocity16 = dataset.createVariable("current_u_16", "f8", ("time", "lon", "lat",))
        east_velocity16.long_name = "Eastward Sea Water Velocity"
        east_velocity16.standard_name = "eastward_sea_water_velocity"
        east_velocity16.short_name = "u"
        east_velocity16.units = "01 mm s-1"
        east_velocity16.observation_type = "measured"
        east_velocity16.ioos_category = "Currents"
        east_velocity16.is_dead = "NaN"
        east_velocity16[:, 0, 0] = evb16

        north_velocity16 = dataset.createVariable("current_v_16", "f8", ("time", "lon", "lat",))
        north_velocity16.long_name = "Northward Sea Water Velocity"
        north_velocity16.standard_name = "northward_sea_water_velocity"
        north_velocity16.short_name = "v"
        north_velocity16.units = "01 mm s-1"
        north_velocity16.observation_type = "measured"
        north_velocity16.ioos_category = "Currents"
        north_velocity16.is_dead = "NaN"
        north_velocity16[:, 0, 0] = nvb16

        east_velocity17 = dataset.createVariable("current_u_17", "f8", ("time", "lon", "lat",))
        east_velocity17.long_name = "Eastward Sea Water Velocity"
        east_velocity17.standard_name = "eastward_sea_water_velocity"
        east_velocity17.short_name = "u"
        east_velocity17.units = "01 mm s-1"
        east_velocity17.observation_type = "measured"
        east_velocity17.ioos_category = "Currents"
        east_velocity17.is_dead = "NaN"
        east_velocity17[:, 0, 0] = evb17

        north_velocity17 = dataset.createVariable("current_v_17", "f8", ("time", "lon", "lat",))
        north_velocity17.long_name = "Northward Sea Water Velocity"
        north_velocity17.standard_name = "northward_sea_water_velocity"
        north_velocity17.short_name = "v"
        north_velocity17.units = "01 mm s-1"
        north_velocity17.observation_type = "measured"
        north_velocity17.ioos_category = "Currents"
        north_velocity17.is_dead = "NaN"
        north_velocity17[:, 0, 0] = nvb17

        east_velocity18 = dataset.createVariable("current_u_18", "f8", ("time", "lon", "lat",))
        east_velocity18.long_name = "Eastward Sea Water Velocity"
        east_velocity18.standard_name = "eastward_sea_water_velocity"
        east_velocity18.short_name = "u"
        east_velocity18.units = "01 mm s-1"
        east_velocity18.observation_type = "measured"
        east_velocity18.ioos_category = "Currents"
        east_velocity18.is_dead = "NaN"
        east_velocity18[:, 0, 0] = evb18

        north_velocity18 = dataset.createVariable("current_v_18", "f8", ("time", "lon", "lat",))
        north_velocity18.long_name = "Northward Sea Water Velocity"
        north_velocity18.standard_name = "northward_sea_water_velocity"
        north_velocity18.short_name = "v"
        north_velocity18.units = "01 mm s-1"
        north_velocity18.observation_type = "measured"
        north_velocity18.ioos_category = "Currents"
        north_velocity18.is_dead = "NaN"
        north_velocity18[:, 0, 0] = nvb18

        east_velocity19 = dataset.createVariable("current_u_19", "f8", ("time", "lon", "lat",))
        east_velocity19.long_name = "Eastward Sea Water Velocity"
        east_velocity19.standard_name = "eastward_sea_water_velocity"
        east_velocity19.short_name = "u"
        east_velocity19.units = "01 mm s-1"
        east_velocity19.observation_type = "measured"
        east_velocity19.ioos_category = "Currents"
        east_velocity19.is_dead = "NaN"
        east_velocity19[:, 0, 0] = evb19

        north_velocity19 = dataset.createVariable("current_v_19", "f8", ("time", "lon", "lat",))
        north_velocity19.long_name = "Northward Sea Water Velocity"
        north_velocity19.standard_name = "northward_sea_water_velocity"
        north_velocity19.short_name = "v"
        north_velocity19.units = "01 mm s-1"
        north_velocity19.observation_type = "measured"
        north_velocity19.ioos_category = "Currents"
        north_velocity19.is_dead = "NaN"
        north_velocity19[:, 0, 0] = nvb19

        east_velocity20 = dataset.createVariable("current_u_20", "f8", ("time", "lon", "lat",))
        east_velocity20.long_name = "Eastward Sea Water Velocity"
        east_velocity20.standard_name = "eastward_sea_water_velocity"
        east_velocity20.short_name = "u"
        east_velocity20.units = "01 mm s-1"
        east_velocity20.observation_type = "measured"
        east_velocity20.ioos_category = "Currents"
        east_velocity20.is_dead = "NaN"
        east_velocity20[:, 0, 0] = evb20

        north_velocity20 = dataset.createVariable("current_v_20", "f8", ("time", "lon", "lat",))
        north_velocity20.long_name = "Northward Sea Water Velocity"
        north_velocity20.standard_name = "northward_sea_water_velocity"
        north_velocity20.short_name = "v"
        north_velocity20.units = "01 mm s-1"
        north_velocity20.observation_type = "measured"
        north_velocity20.ioos_category = "Currents"
        north_velocity20.is_dead = "NaN"
        north_velocity20[:, 0, 0] = nvb20'''
        
        mean_current_velocity_magnitude = dataset.createVariable("current_speed", "f8", ("time", "lon", "lat",), fill_value="NaN")
        mean_current_velocity_magnitude.long_name = "Mean Current Speed"
        #mean_current_velocity_magnitude.standard_name = "mean_current_speed"
        mean_current_velocity_magnitude.short_name = "MCSPD"
        mean_current_velocity_magnitude.units = "knots"
        mean_current_velocity_magnitude.observation_type = "measured"
        mean_current_velocity_magnitude.dependency = "mean_current_direction"
        # mean_current_velocity_magnitude.instrument_range = "0.f, 300.f"
        # mean_current_velocity_magnitude.valid_range = "0.f, 300.f"
        # mean_current_velocity_magnitude.precision = 0.1
        # mean_current_velocity_magnitude.accuracy = 0.5
        mean_current_velocity_magnitude.ioos_category = "Currents"
        mean_current_velocity_magnitude.missing_value = "NaN"
        mean_current_velocity_magnitude[:, 0, 0] = mcspd

        mean_current_velocity_direction = dataset.createVariable("current_direction", "f8", ("time", "lon", "lat",), fill_value="NaN")
        mean_current_velocity_direction.long_name = "Mean Current Direction"
        #mean_current_velocity_direction.standard_name = "mean_current_direction"
        mean_current_velocity_direction.short_name = "MCDIR"
        # mean_current_velocity_direction.ancillary_variables = "current_direction_qc"
        mean_current_velocity_direction.units = "degrees"
        mean_current_velocity_direction.observation_type = "measured"
        mean_current_velocity_direction.dependency = "mean_current_speed"
        mean_current_velocity_direction.instrument_range = [0., 360.]
        mean_current_velocity_direction.valid_range = [0., 360.]
        # mean_current_velocity_direction.precision = 0.35
        # mean_current_velocity_direction.accuracy = 2
        mean_current_velocity_direction.ioos_category = "Currents"
        mean_current_velocity_direction.missing_value = "NaN"
        mean_current_velocity_direction[:, 0, 0] = mcdir

        '''percent_good_bin_01 = dataset.createVariable("PGB01", "f8", ("time", "lon", "lat",))
        percent_good_bin_01.ioos_category = "Currents"
        percent_good_bin_01.long_name = "Percent Good 01 Beam"
        percent_good_bin_01.short_name = "PGB01"
        percent_good_bin_01.units = "percent"
        percent_good_bin_01.observation_type = "measured"
        percent_good_bin_01.is_dead = "NaN"
        percent_good_bin_01[:, 0, 0] = pgb1

        percent_good_bin_02 = dataset.createVariable("PGB02", "f8", ("time", "lon", "lat",))
        percent_good_bin_02.ioos_category = "Currents"
        percent_good_bin_02.long_name = "Percent Good 02 Beam"
        percent_good_bin_02.short_name = "PGB02"
        percent_good_bin_02.units = "percent"
        percent_good_bin_02.observation_type = "measured"
        percent_good_bin_02.is_dead = "NaN"
        percent_good_bin_02[:, 0, 0] = pgb2

        percent_good_bin_03 = dataset.createVariable("PGB03", "f8", ("time", "lon", "lat",))
        percent_good_bin_03.ioos_category = "Currents"
        percent_good_bin_03.long_name = "Percent Good 03 Beam"
        percent_good_bin_03.short_name = "PGB03"
        percent_good_bin_03.units = "percent"
        percent_good_bin_03.observation_type = "measured"
        percent_good_bin_03.is_dead = "NaN"
        percent_good_bin_03[:, 0, 0] = pgb3

        percent_good_bin_04 = dataset.createVariable("PGB04", "f8", ("time", "lon", "lat",))
        percent_good_bin_04.ioos_category = "Currents"
        percent_good_bin_04.long_name = "Percent Good 04 Beam"
        percent_good_bin_04.short_name = "PGB04"
        percent_good_bin_04.units = "percent"
        percent_good_bin_04.observation_type = "measured"
        percent_good_bin_04.is_dead = "NaN"
        percent_good_bin_04[:, 0, 0] = pgb4

        percent_good_bin_05 = dataset.createVariable("PGB05", "f8", ("time", "lon", "lat",))
        percent_good_bin_05.ioos_category = "Currents"
        percent_good_bin_05.long_name = "Percent Good 05 Beam"
        percent_good_bin_05.short_name = "PGB05"
        percent_good_bin_05.units = "percent"
        percent_good_bin_05.observation_type = "measured"
        percent_good_bin_05.is_dead = "NaN"
        percent_good_bin_05[:, 0, 0] = pgb5

        percent_good_bin_06 = dataset.createVariable("PGB06", "f8", ("time", "lon", "lat",))
        percent_good_bin_06.ioos_category = "Currents"
        percent_good_bin_06.long_name = "Percent Good 06 Beam"
        percent_good_bin_06.short_name = "PGB06"
        percent_good_bin_06.units = "percent"
        percent_good_bin_06.observation_type = "measured"
        percent_good_bin_06.is_dead = "NaN"
        percent_good_bin_06[:, 0, 0] = pgb6

        percent_good_bin_07 = dataset.createVariable("PGB07", "f8", ("time", "lon", "lat",))
        percent_good_bin_07.ioos_category = "Currents"
        percent_good_bin_07.long_name = "Percent Good 07 Beam"
        percent_good_bin_07.short_name = "PGB07"
        percent_good_bin_07.units = "percent"
        percent_good_bin_07.observation_type = "measured"
        percent_good_bin_07.is_dead = "NaN"
        percent_good_bin_07[:, 0, 0] = pgb7

        percent_good_bin_08 = dataset.createVariable("PGB08", "f8", ("time", "lon", "lat",))
        percent_good_bin_08.ioos_category = "Currents"
        percent_good_bin_08.long_name = "Percent Good 08 Beam"
        percent_good_bin_08.short_name = "PGB08"
        percent_good_bin_08.units = "percent"
        percent_good_bin_08.observation_type = "measured"
        percent_good_bin_08.is_dead = "NaN"
        percent_good_bin_08[:, 0, 0] = pgb8

        percent_good_bin_09 = dataset.createVariable("PGB09", "f8", ("time", "lon", "lat",))
        percent_good_bin_09.ioos_category = "Currents"
        percent_good_bin_09.long_name = "Percent Good 09 Beam"
        percent_good_bin_09.short_name = "PGB09"
        percent_good_bin_09.units = "percent"
        percent_good_bin_09.observation_type = "measured"
        percent_good_bin_09.is_dead = "NaN"
        percent_good_bin_09[:, 0, 0] = pgb9

        percent_good_bin_10 = dataset.createVariable("PGB10", "f8", ("time", "lon", "lat",))
        percent_good_bin_10.ioos_category = "Currents"
        percent_good_bin_10.long_name = "Percent Good 10 Beam"
        percent_good_bin_10.short_name = "PGB10"
        percent_good_bin_10.units = "percent"
        percent_good_bin_10.observation_type = "measured"
        percent_good_bin_10.is_dead = "NaN"
        percent_good_bin_10[:, 0, 0] = pgb10

        percent_good_bin_11 = dataset.createVariable("PGB11", "f8", ("time", "lon", "lat",))
        percent_good_bin_11.ioos_category = "Currents"
        percent_good_bin_11.long_name = "Percent Good 11 Beam"
        percent_good_bin_11.short_name = "PGB11"
        percent_good_bin_11.units = "percent"
        percent_good_bin_11.observation_type = "measured"
        percent_good_bin_11.is_dead = "NaN"
        percent_good_bin_11[:, 0, 0] = pgb11

        percent_good_bin_12 = dataset.createVariable("PGB12", "f8", ("time", "lon", "lat",))
        percent_good_bin_12.ioos_category = "Currents"
        percent_good_bin_12.long_name = "Percent Good 12 Beam"
        percent_good_bin_12.short_name = "PGB12"
        percent_good_bin_12.units = "percent"
        percent_good_bin_12.observation_type = "measured"
        percent_good_bin_12.is_dead = "NaN"
        percent_good_bin_12[:, 0, 0] = pgb12

        percent_good_bin_13 = dataset.createVariable("PGB13", "f8", ("time", "lon", "lat",))
        percent_good_bin_13.ioos_category = "Currents"
        percent_good_bin_13.long_name = "Percent Good 13 Beam"
        percent_good_bin_13.short_name = "PGB13"
        percent_good_bin_13.units = "percent"
        percent_good_bin_13.observation_type = "measured"
        percent_good_bin_13.is_dead = "NaN"
        percent_good_bin_13[:, 0, 0] = pgb13

        percent_good_bin_14 = dataset.createVariable("PGB14", "f8", ("time", "lon", "lat",))
        percent_good_bin_14.ioos_category = "Currents"
        percent_good_bin_14.long_name = "Percent Good 14 Beam"
        percent_good_bin_14.short_name = "PGB14"
        percent_good_bin_14.units = "percent"
        percent_good_bin_14.observation_type = "measured"
        percent_good_bin_14.is_dead = "NaN"
        percent_good_bin_14[:, 0, 0] = pgb14

        percent_good_bin_15 = dataset.createVariable("PGB15", "f8", ("time", "lon", "lat",))
        percent_good_bin_15.ioos_category = "Currents"
        percent_good_bin_15.long_name = "Percent Good 15 Beam"
        percent_good_bin_15.short_name = "PGB15"
        percent_good_bin_15.units = "percent"
        percent_good_bin_15.observation_type = "measured"
        percent_good_bin_15.is_dead = "NaN"
        percent_good_bin_15[:, 0, 0] = pgb15

        percent_good_bin_16 = dataset.createVariable("PGB16", "f8", ("time", "lon", "lat",))
        percent_good_bin_16.ioos_category = "Currents"
        percent_good_bin_16.long_name = "Percent Good 16 Beam"
        percent_good_bin_16.short_name = "PGB16"
        percent_good_bin_16.units = "percent"
        percent_good_bin_16.observation_type = "measured"
        percent_good_bin_16.is_dead = "NaN"
        percent_good_bin_16[:, 0, 0] = pgb16

        percent_good_bin_17 = dataset.createVariable("PGB17", "f8", ("time", "lon", "lat",))
        percent_good_bin_17.ioos_category = "Currents"
        percent_good_bin_17.long_name = "Percent Good 17 Beam"
        percent_good_bin_17.short_name = "PGB17"
        percent_good_bin_17.units = "percent"
        percent_good_bin_17.observation_type = "measured"
        percent_good_bin_17.is_dead = "NaN"
        percent_good_bin_17[:, 0, 0] = pgb17

        percent_good_bin_18 = dataset.createVariable("PGB18", "f8", ("time", "lon", "lat",))
        percent_good_bin_18.ioos_category = "Currents"
        percent_good_bin_18.long_name = "Percent Good 18 Beam"
        percent_good_bin_18.short_name = "PGB18"
        percent_good_bin_18.units = "percent"
        percent_good_bin_18.observation_type = "measured"
        percent_good_bin_18.is_dead = "NaN"
        percent_good_bin_18[:, 0, 0] = pgb18

        percent_good_bin_19 = dataset.createVariable("PGB19", "f8", ("time", "lon", "lat",))
        percent_good_bin_19.ioos_category = "Currents"
        percent_good_bin_19.long_name = "Percent Good 19 Beam"
        percent_good_bin_19.short_name = "PGB19"
        percent_good_bin_19.units = "percent"
        percent_good_bin_19.observation_type = "measured"
        percent_good_bin_19.is_dead = "NaN"
        percent_good_bin_19[:, 0, 0] = pgb19

        percent_good_bin_20 = dataset.createVariable("PGB20", "f8", ("time", "lon", "lat",))
        percent_good_bin_20.ioos_category = "Currents"
        percent_good_bin_20.long_name = "Percent Good 20 Beam"
        percent_good_bin_20.short_name = "PGB20"
        percent_good_bin_20.units = "percent"
        percent_good_bin_20.observation_type = "measured"
        percent_good_bin_20.is_dead = "NaN"
        percent_good_bin_20[:, 0, 0] = pgb20
        
        echo_amp_1_bin_1 = dataset.createVariable("EA01B01", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_1.long_name = "Echo Amplitude 01 Bin 01"
        echo_amp_1_bin_1.standard_name = "echo_amplitude_01_bin_01"
        echo_amp_1_bin_1.short_name = "EA01B01"
        echo_amp_1_bin_1.units = "counts"
        echo_amp_1_bin_1.observation_type = "measured"
        echo_amp_1_bin_1.is_dead = "NaN"
        echo_amp_1_bin_1[:, 0, 0] = EA01B01
        
        echo_amp_2_bin_1 = dataset.createVariable("EA02B01", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_1.long_name = "Echo Amplitude 02 Bin 01"
        echo_amp_2_bin_1.standard_name = "echo_amplitude_02_bin_01"
        echo_amp_2_bin_1.short_name = "EA02B01"
        echo_amp_2_bin_1.units = "counts"
        echo_amp_2_bin_1.observation_type = "measured"
        echo_amp_2_bin_1.is_dead = "NaN"
        echo_amp_2_bin_1[:, 0, 0] = EA02B01

        echo_amp_3_bin_1 = dataset.createVariable("EA03B01", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_1.long_name = "Echo Amplitude 03 Bin 01"
        echo_amp_3_bin_1.standard_name = "echo_amplitude_03_bin_01"
        echo_amp_3_bin_1.short_name = "EA03B01"
        echo_amp_3_bin_1.units = "counts"
        echo_amp_3_bin_1.observation_type = "measured"
        echo_amp_3_bin_1.is_dead = "NaN"
        echo_amp_3_bin_1[:, 0, 0] = EA03B01

        echo_amp_1_bin_2 = dataset.createVariable("EA01B02", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_2.long_name = "Echo Amplitude 01 Bin 02"
        echo_amp_1_bin_2.standard_name = "echo_amplitude_01_bin_02"
        echo_amp_1_bin_2.short_name = "EA01B02"
        echo_amp_1_bin_2.units = "counts"
        echo_amp_1_bin_2.observation_type = "measured"
        echo_amp_1_bin_2.is_dead = "NaN"
        echo_amp_1_bin_2[:, 0, 0] = EA01B02

        echo_amp_2_bin_2 = dataset.createVariable("EA02B02", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_2.long_name = "Echo Amplitude 02 Bin 02"
        echo_amp_2_bin_2.standard_name = "echo_amplitude_02_bin_02"
        echo_amp_2_bin_2.short_name = "EA02B02"
        echo_amp_2_bin_2.units = "counts"
        echo_amp_2_bin_2.observation_type = "measured"
        echo_amp_2_bin_2.is_dead = "NaN"
        echo_amp_2_bin_2[:, 0, 0] = EA02B02

        echo_amp_3_bin_2 = dataset.createVariable("EA03B02", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_2.long_name = "Echo Amplitude 03 Bin 02"
        echo_amp_3_bin_2.standard_name = "echo_amplitude_03_bin_02"
        echo_amp_3_bin_2.short_name = "EA03B02"
        echo_amp_3_bin_2.units = "counts"
        echo_amp_3_bin_2.observation_type = "measured"
        echo_amp_3_bin_2.is_dead = "NaN"
        echo_amp_3_bin_2[:, 0, 0] = EA03B02

        echo_amp_1_bin_3 = dataset.createVariable("EA01B03", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_3.long_name = "Echo Amplitude 01 Bin 03"
        echo_amp_1_bin_3.standard_name = "echo_amplitude_01_bin_03"
        echo_amp_1_bin_3.short_name = "EA01B03"
        echo_amp_1_bin_3.units = "counts"
        echo_amp_1_bin_3.observation_type = "measured"
        echo_amp_1_bin_3.is_dead = "NaN"
        echo_amp_1_bin_3[:, 0, 0] = EA01B03

        echo_amp_2_bin_3 = dataset.createVariable("EA02B03", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_3.long_name = "Echo Amplitude 02 Bin 03"
        echo_amp_2_bin_3.standard_name = "echo_amplitude_02_bin_03"
        echo_amp_2_bin_3.short_name = "EA02B03"
        echo_amp_2_bin_3.units = "counts"
        echo_amp_2_bin_3.observation_type = "measured"
        echo_amp_2_bin_3.is_dead = "NaN"
        echo_amp_2_bin_3[:, 0, 0] = EA02B03

        echo_amp_3_bin_3 = dataset.createVariable("EA03B03", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_3.long_name = "Echo Amplitude 03 Bin 03"
        echo_amp_3_bin_3.standard_name = "echo_amplitude_03_bin_03"
        echo_amp_3_bin_3.short_name = "EA03B03"
        echo_amp_3_bin_3.units = "counts"
        echo_amp_3_bin_3.observation_type = "measured"
        echo_amp_3_bin_3.is_dead = "NaN"
        echo_amp_3_bin_3[:, 0, 0] = EA03B03

        echo_amp_1_bin_4 = dataset.createVariable("EA01B04", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_4.long_name = "Echo Amplitude 01 Bin 04"
        echo_amp_1_bin_4.standard_name = "echo_amplitude_01_bin_04"
        echo_amp_1_bin_4.short_name = "EA01B04"
        echo_amp_1_bin_4.units = "counts"
        echo_amp_1_bin_4.observation_type = "measured"
        echo_amp_1_bin_4.is_dead = "NaN"
        echo_amp_1_bin_4[:, 0, 0] = EA01B04

        echo_amp_2_bin_4 = dataset.createVariable("EA02B04", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_4.long_name = "Echo Amplitude 02 Bin 04"
        echo_amp_2_bin_4.standard_name = "echo_amplitude_02_bin_04"
        echo_amp_2_bin_4.short_name = "EA02B04"
        echo_amp_2_bin_4.units = "counts"
        echo_amp_2_bin_4.observation_type = "measured"
        echo_amp_2_bin_4.is_dead = "NaN"
        echo_amp_2_bin_4[:, 0, 0] = EA02B04

        echo_amp_3_bin_4 = dataset.createVariable("EA03B04", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_4.long_name = "Echo Amplitude 03 Bin 04"
        echo_amp_3_bin_4.standard_name = "echo_amplitude_03_bin_04"
        echo_amp_3_bin_4.short_name = "EA03B04"
        echo_amp_3_bin_4.units = "counts"
        echo_amp_3_bin_4.observation_type = "measured"
        echo_amp_3_bin_4.is_dead = "NaN"
        echo_amp_3_bin_4[:, 0, 0] = EA03B04

        echo_amp_1_bin_5 = dataset.createVariable("EA01B05", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_5.long_name = "Echo Amplitude 01 Bin 05"
        echo_amp_1_bin_5.standard_name = "echo_amplitude_01_bin_05"
        echo_amp_1_bin_5.short_name = "EA01B05"
        echo_amp_1_bin_5.units = "counts"
        echo_amp_1_bin_5.observation_type = "measured"
        echo_amp_1_bin_5.is_dead = "NaN"
        echo_amp_1_bin_5[:, 0, 0] = EA01B05

        echo_amp_2_bin_5 = dataset.createVariable("EA02B05", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_5.long_name = "Echo Amplitude 02 Bin 05"
        echo_amp_2_bin_5.standard_name = "echo_amplitude_02_bin_05"
        echo_amp_2_bin_5.short_name = "EA02B05"
        echo_amp_2_bin_5.units = "counts"
        echo_amp_2_bin_5.observation_type = "measured"
        echo_amp_2_bin_5.is_dead = "NaN"
        echo_amp_2_bin_5[:, 0, 0] = EA02B05

        echo_amp_3_bin_5 = dataset.createVariable("EA03B05", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_5.long_name = "Echo Amplitude 03 Bin 05"
        echo_amp_3_bin_5.standard_name = "echo_amplitude_03_bin_05"
        echo_amp_3_bin_5.short_name = "EA03B05"
        echo_amp_3_bin_5.units = "counts"
        echo_amp_3_bin_5.observation_type = "measured"
        echo_amp_3_bin_5.is_dead = "NaN"
        echo_amp_3_bin_5[:, 0, 0] = EA03B05

        echo_amp_1_bin_6 = dataset.createVariable("EA01B06", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_6.long_name = "Echo Amplitude 01 Bin 06"
        echo_amp_1_bin_6.standard_name = "echo_amplitude_01_bin_06"
        echo_amp_1_bin_6.short_name = "EA01B06"
        echo_amp_1_bin_6.units = "counts"
        echo_amp_1_bin_6.observation_type = "measured"
        echo_amp_1_bin_6.is_dead = "NaN"
        echo_amp_1_bin_6[:, 0, 0] = EA01B06

        echo_amp_2_bin_6 = dataset.createVariable("EA02B06", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_6.long_name = "Echo Amplitude 02 Bin 06"
        echo_amp_2_bin_6.standard_name = "echo_amplitude_02_bin_06"
        echo_amp_2_bin_6.short_name = "EA02B06"
        echo_amp_2_bin_6.units = "counts"
        echo_amp_2_bin_6.observation_type = "measured"
        echo_amp_2_bin_6.is_dead = "NaN"
        echo_amp_2_bin_6[:, 0, 0] = EA02B06

        echo_amp_3_bin_6 = dataset.createVariable("EA03B06", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_6.long_name = "Echo Amplitude 03 Bin 06"
        echo_amp_3_bin_6.standard_name = "echo_amplitude_03_bin_06"
        echo_amp_3_bin_6.short_name = "EA03B06"
        echo_amp_3_bin_6.units = "counts"
        echo_amp_3_bin_6.observation_type = "measured"
        echo_amp_3_bin_6.is_dead = "NaN"
        echo_amp_3_bin_6[:, 0, 0] = EA03B06

        echo_amp_1_bin_7 = dataset.createVariable("EA01B07", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_7.long_name = "Echo Amplitude 01 Bin 07"
        echo_amp_1_bin_7.standard_name = "echo_amplitude_01_bin_07"
        echo_amp_1_bin_7.short_name = "EA01B07"
        echo_amp_1_bin_7.units = "counts"
        echo_amp_1_bin_7.observation_type = "measured"
        echo_amp_1_bin_7.is_dead = "NaN"
        echo_amp_1_bin_7[:, 0, 0] = EA01B07

        echo_amp_2_bin_7 = dataset.createVariable("EA02B07", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_7.long_name = "Echo Amplitude 02 Bin 07"
        echo_amp_2_bin_7.standard_name = "echo_amplitude_02_bin_07"
        echo_amp_2_bin_7.short_name = "EA02B07"
        echo_amp_2_bin_7.units = "counts"
        echo_amp_2_bin_7.observation_type = "measured"
        echo_amp_2_bin_7.is_dead = "NaN"
        echo_amp_2_bin_7[:, 0, 0] = EA02B07

        echo_amp_3_bin_7 = dataset.createVariable("EA03B07", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_7.long_name = "Echo Amplitude 03 Bin 07"
        echo_amp_3_bin_7.standard_name = "echo_amplitude_03_bin_07"
        echo_amp_3_bin_7.short_name = "EA03B07"
        echo_amp_3_bin_7.units = "counts"
        echo_amp_3_bin_7.observation_type = "measured"
        echo_amp_3_bin_7.is_dead = "NaN"
        echo_amp_3_bin_7[:, 0, 0] = EA03B07

        echo_amp_1_bin_8 = dataset.createVariable("EA01B08", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_8.long_name = "Echo Amplitude 01 Bin 08"
        echo_amp_1_bin_8.standard_name = "echo_amplitude_01_bin_08"
        echo_amp_1_bin_8.short_name = "EA01B08"
        echo_amp_1_bin_8.units = "counts"
        echo_amp_1_bin_8.observation_type = "measured"
        echo_amp_1_bin_8.is_dead = "NaN"
        echo_amp_1_bin_8[:, 0, 0] = EA01B08

        echo_amp_2_bin_8 = dataset.createVariable("EA02B08", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_8.long_name = "Echo Amplitude 02 Bin 08"
        echo_amp_2_bin_8.standard_name = "echo_amplitude_02_bin_08"
        echo_amp_2_bin_8.short_name = "EA02B08"
        echo_amp_2_bin_8.units = "counts"
        echo_amp_2_bin_8.observation_type = "measured"
        echo_amp_2_bin_8.is_dead = "NaN"
        echo_amp_2_bin_8[:, 0, 0] = EA02B08

        echo_amp_3_bin_8 = dataset.createVariable("EA03B08", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_8.long_name = "Echo Amplitude 03 Bin 08"
        echo_amp_3_bin_8.standard_name = "echo_amplitude_03_bin_08"
        echo_amp_3_bin_8.short_name = "EA03B08"
        echo_amp_3_bin_8.units = "counts"
        echo_amp_3_bin_8.observation_type = "measured"
        echo_amp_3_bin_8.is_dead = "NaN"
        echo_amp_3_bin_8[:, 0, 0] = EA03B08

        echo_amp_1_bin_9 = dataset.createVariable("EA01B09", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_9.long_name = "Echo Amplitude 01 Bin 09"
        echo_amp_1_bin_9.standard_name = "echo_amplitude_01_bin_09"
        echo_amp_1_bin_9.short_name = "EA01B09"
        echo_amp_1_bin_9.units = "counts"
        echo_amp_1_bin_9.observation_type = "measured"
        echo_amp_1_bin_9.is_dead = "NaN"
        echo_amp_1_bin_9[:, 0, 0] = EA01B09

        echo_amp_2_bin_9 = dataset.createVariable("EA02B09", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_9.long_name = "Echo Amplitude 02 Bin 09"
        echo_amp_2_bin_9.standard_name = "echo_amplitude_02_bin_09"
        echo_amp_2_bin_9.short_name = "EA02B09"
        echo_amp_2_bin_9.units = "counts"
        echo_amp_2_bin_9.observation_type = "measured"
        echo_amp_2_bin_9.is_dead = "NaN"
        echo_amp_2_bin_9[:, 0, 0] = EA02B09

        echo_amp_3_bin_9 = dataset.createVariable("EA03B09", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_9.long_name = "Echo Amplitude 03 Bin 09"
        echo_amp_3_bin_9.standard_name = "echo_amplitude_03_bin_09"
        echo_amp_3_bin_9.short_name = "EA03B09"
        echo_amp_3_bin_9.units = "counts"
        echo_amp_3_bin_9.observation_type = "measured"
        echo_amp_3_bin_9.is_dead = "NaN"
        echo_amp_3_bin_9[:, 0, 0] = EA03B09

        echo_amp_1_bin_10 = dataset.createVariable("EA01B10", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_10.long_name = "Echo Amplitude 01 Bin 10"
        echo_amp_1_bin_10.standard_name = "echo_amplitude_03_bin_10"
        echo_amp_1_bin_10.short_name = "EA01B10"
        echo_amp_1_bin_10.units = "counts"
        echo_amp_1_bin_10.observation_type = "measured"
        echo_amp_1_bin_10.is_dead = "NaN"
        echo_amp_1_bin_10[:, 0, 0] = EA01B10

        echo_amp_2_bin_10 = dataset.createVariable("EA02B10", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_10.long_name = "Echo Amplitude 02 Bin 10"
        echo_amp_2_bin_10.standard_name = "echo_amplitude_02_bin_10"
        echo_amp_2_bin_10.short_name = "EA02B10"
        echo_amp_2_bin_10.units = "counts"
        echo_amp_2_bin_10.observation_type = "measured"
        echo_amp_2_bin_10.is_dead = "NaN"
        echo_amp_2_bin_10[:, 0, 0] = EA02B10

        echo_amp_3_bin_10 = dataset.createVariable("EA03B10", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_10.long_name = "Echo Amplitude 03 Bin 10"
        echo_amp_3_bin_10.standard_name = "echo_amplitude_03_bin_10"
        echo_amp_3_bin_10.short_name = "EA03B10"
        echo_amp_3_bin_10.units = "counts"
        echo_amp_3_bin_10.observation_type = "measured"
        echo_amp_3_bin_10.is_dead = "NaN"
        echo_amp_3_bin_10[:, 0, 0] = EA03B10

        echo_amp_1_bin_11 = dataset.createVariable("EA01B11", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_11.long_name = "Echo Amplitude 01 Bin 11"
        echo_amp_1_bin_11.standard_name = "echo_amplitude_01_bin_11"
        echo_amp_1_bin_11.short_name = "EA01B11"
        echo_amp_1_bin_11.units = "counts"
        echo_amp_1_bin_11.observation_type = "measured"
        echo_amp_1_bin_11.is_dead = "NaN"
        echo_amp_1_bin_11[:, 0, 0] = EA01B11

        echo_amp_2_bin_11 = dataset.createVariable("EA02B11", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_11.long_name = "Echo Amplitude 02 Bin 11"
        echo_amp_2_bin_11.standard_name = "echo_amplitude_02_bin_11"
        echo_amp_2_bin_11.short_name = "EA02B11"
        echo_amp_2_bin_11.units = "counts"
        echo_amp_2_bin_11.observation_type = "measured"
        echo_amp_2_bin_11.is_dead = "NaN"
        echo_amp_2_bin_11[:, 0, 0] = EA02B11

        echo_amp_3_bin_11 = dataset.createVariable("EA03B11", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_11.long_name = "Echo Amplitude 03 Bin 11"
        echo_amp_3_bin_11.standard_name = "echo_amplitude_03_bin_11"
        echo_amp_3_bin_11.short_name = "EA03B11"
        echo_amp_3_bin_11.units = "counts"
        echo_amp_3_bin_11.observation_type = "measured"
        echo_amp_3_bin_11.is_dead = "NaN"
        echo_amp_3_bin_11[:, 0, 0] = EA03B11

        echo_amp_1_bin_12 = dataset.createVariable("EA01B12", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_12.long_name = "Echo Amplitude 01 Bin 12"
        echo_amp_1_bin_12.standard_name = "echo_amplitude_01_bin_12"
        echo_amp_1_bin_12.short_name = "EA01B12"
        echo_amp_1_bin_12.units = "counts"
        echo_amp_1_bin_12.observation_type = "measured"
        echo_amp_1_bin_12.is_dead = "NaN"
        echo_amp_1_bin_12[:, 0, 0] = EA01B12

        echo_amp_2_bin_12 = dataset.createVariable("EA02B12", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_12.long_name = "Echo Amplitude 02 Bin 12"
        echo_amp_2_bin_12.standard_name = "echo_amplitude_02_bin_12"
        echo_amp_2_bin_12.short_name = "EA02B12"
        echo_amp_2_bin_12.units = "counts"
        echo_amp_2_bin_12.observation_type = "measured"
        echo_amp_2_bin_12.is_dead = "NaN"
        echo_amp_2_bin_12[:, 0, 0] = EA02B12

        echo_amp_3_bin_12 = dataset.createVariable("EA03B12", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_12.long_name = "Echo Amplitude 03 Bin 12"
        echo_amp_3_bin_12.standard_name = "echo_amplitude_03_bin_12"
        echo_amp_3_bin_12.short_name = "EA03B12"
        echo_amp_3_bin_12.units = "counts"
        echo_amp_3_bin_12.observation_type = "measured"
        echo_amp_3_bin_12.is_dead = "NaN"
        echo_amp_3_bin_12[:, 0, 0] = EA03B12

        echo_amp_1_bin_13 = dataset.createVariable("EA01B13", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_13.long_name = "Echo Amplitude 01 Bin 13"
        echo_amp_1_bin_13.standard_name = "echo_amplitude_01_bin_13"
        echo_amp_1_bin_13.short_name = "EA01B13"
        echo_amp_1_bin_13.units = "counts"
        echo_amp_1_bin_13.observation_type = "measured"
        echo_amp_1_bin_13.is_dead = "NaN"
        echo_amp_1_bin_13[:, 0, 0] = EA01B13

        echo_amp_2_bin_13 = dataset.createVariable("EA02B13", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_13.long_name = "Echo Amplitude 02 Bin 13"
        echo_amp_2_bin_13.standard_name = "echo_amplitude_02_bin_13"
        echo_amp_2_bin_13.short_name = "EA02B13"
        echo_amp_2_bin_13.units = "counts"
        echo_amp_2_bin_13.observation_type = "measured"
        echo_amp_2_bin_13.is_dead = "NaN"
        echo_amp_2_bin_13[:, 0, 0] = EA02B13

        echo_amp_3_bin_13 = dataset.createVariable("EA03B13", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_13.long_name = "Echo Amplitude 03 Bin 13"
        echo_amp_3_bin_13.standard_name = "echo_amplitude_03_bin_13"
        echo_amp_3_bin_13.short_name = "EA03B13"
        echo_amp_3_bin_13.units = "counts"
        echo_amp_3_bin_13.observation_type = "measured"
        echo_amp_2_bin_13.is_dead = "NaN"
        echo_amp_3_bin_13[:, 0, 0] = EA03B13

        echo_amp_1_bin_14 = dataset.createVariable("EA01B14", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_14.long_name = "Echo Amplitude 01 Bin 14"
        echo_amp_1_bin_14.standard_name = "echo_amplitude_01_bin_14"
        echo_amp_1_bin_14.short_name = "EA01B14"
        echo_amp_1_bin_14.units = "counts"
        echo_amp_1_bin_14.observation_type = "measured"
        echo_amp_1_bin_14.is_dead = "NaN"
        echo_amp_1_bin_14[:, 0, 0] = EA01B14

        echo_amp_2_bin_14 = dataset.createVariable("EA02B14", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_14.long_name = "Echo Amplitude 02 Bin 14"
        echo_amp_2_bin_14.standard_name = "echo_amplitude_02_bin_14"
        echo_amp_2_bin_14.short_name = "EA02B14"
        echo_amp_2_bin_14.units = "counts"
        echo_amp_2_bin_14.observation_type = "measured"
        echo_amp_2_bin_14.is_dead = "NaN"
        echo_amp_2_bin_14[:, 0, 0] = EA02B14

        echo_amp_3_bin_14 = dataset.createVariable("EA03B14", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_14.long_name = "Echo Amplitude 03 Bin 14"
        echo_amp_3_bin_14.standard_name = "echo_amplitude_03_bin_14"
        echo_amp_3_bin_14.short_name = "EA03B14"
        echo_amp_3_bin_14.units = "counts"
        echo_amp_3_bin_14.observation_type = "measured"
        echo_amp_3_bin_14.is_dead = "NaN"
        echo_amp_3_bin_14[:, 0, 0] = EA03B14

        echo_amp_1_bin_15 = dataset.createVariable("EA01B15", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_15.long_name = "Echo Amplitude 01 Bin 15"
        echo_amp_1_bin_15.standard_name = "echo_amplitude_01_bin_15"
        echo_amp_1_bin_15.short_name = "EA01B15"
        echo_amp_1_bin_15.units = "counts"
        echo_amp_1_bin_15.observation_type = "measured"
        echo_amp_1_bin_15.is_dead = "NaN"
        echo_amp_1_bin_15[:, 0, 0] = EA01B15

        echo_amp_2_bin_15 = dataset.createVariable("EA02B15", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_15.long_name = "Echo Amplitude 02 Bin 15"
        echo_amp_2_bin_15.standard_name = "echo_amplitude_02_bin_15"
        echo_amp_2_bin_15.short_name = "EA02B15"
        echo_amp_2_bin_15.units = "counts"
        echo_amp_2_bin_15.observation_type = "measured"
        echo_amp_2_bin_15.is_dead = "NaN"
        echo_amp_2_bin_15[:, 0, 0] = EA02B15

        echo_amp_3_bin_15 = dataset.createVariable("EA03B15", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_15.long_name = "Echo Amplitude 03 Bin 15"
        echo_amp_3_bin_15.standard_name = "echo_amplitude_03_bin_15"
        echo_amp_3_bin_15.short_name = "EA03B15"
        echo_amp_3_bin_15.units = "counts"
        echo_amp_3_bin_15.observation_type = "measured"
        echo_amp_3_bin_15.is_dead = "NaN"
        echo_amp_3_bin_15[:, 0, 0] = EA03B15

        echo_amp_1_bin_16 = dataset.createVariable("EA01B16", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_16.long_name = "Echo Amplitude 01 Bin 16"
        echo_amp_1_bin_16.standard_name = "echo_amplitude_01_bin_16"
        echo_amp_1_bin_16.short_name = "EA01B16"
        echo_amp_1_bin_16.units = "counts"
        echo_amp_1_bin_16.observation_type = "measured"
        echo_amp_1_bin_16.is_dead = "NaN"
        echo_amp_1_bin_16[:, 0, 0] = EA01B16

        echo_amp_2_bin_16 = dataset.createVariable("EA02B16", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_16.long_name = "Echo Amplitude 02 Bin 16"
        echo_amp_2_bin_16.standard_name = "echo_amplitude_02_bin_16"
        echo_amp_2_bin_16.short_name = "EA02B16"
        echo_amp_2_bin_16.units = "counts"
        echo_amp_2_bin_16.observation_type = "measured"
        echo_amp_2_bin_16.is_dead = "NaN"
        echo_amp_2_bin_16[:, 0, 0] = EA02B16

        echo_amp_3_bin_16 = dataset.createVariable("EA03B16", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_16.long_name = "Echo Amplitude 03 Bin 16"
        echo_amp_3_bin_16.standard_name = "echo_amplitude_03_bin_16"
        echo_amp_3_bin_16.short_name = "EA03B16"
        echo_amp_3_bin_16.units = "counts"
        echo_amp_3_bin_16.observation_type = "measured"
        echo_amp_3_bin_16.is_dead = "NaN"
        echo_amp_3_bin_16[:, 0, 0] = EA03B16

        echo_amp_1_bin_17 = dataset.createVariable("EA01B17", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_17.long_name = "Echo Amplitude 01 Bin 17"
        echo_amp_1_bin_17.standard_name = "echo_amplitude_01_bin_17"
        echo_amp_1_bin_17.short_name = "EA01B17"
        echo_amp_1_bin_17.units = "counts"
        echo_amp_1_bin_17.observation_type = "measured"
        echo_amp_1_bin_17.is_dead = "NaN"
        echo_amp_1_bin_17[:, 0, 0] = EA01B17

        echo_amp_2_bin_17 = dataset.createVariable("EA02B17", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_17.long_name = "Echo Amplitude 02 Bin 17"
        echo_amp_2_bin_17.standard_name = "echo_amplitude_02_bin_17"
        echo_amp_2_bin_17.short_name = "EA02B17"
        echo_amp_2_bin_17.units = "counts"
        echo_amp_2_bin_17.observation_type = "measured"
        echo_amp_2_bin_17.is_dead = "NaN"
        echo_amp_2_bin_17[:, 0, 0] = EA02B17

        echo_amp_3_bin_17 = dataset.createVariable("EA03B17", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_17.long_name = "Echo Amplitude 03 Bin 17"
        echo_amp_3_bin_17.standard_name = "echo_amplitude_03_bin_17"
        echo_amp_3_bin_17.short_name = "EA03B17"
        echo_amp_3_bin_17.units = "counts"
        echo_amp_3_bin_17.observation_type = "measured"
        echo_amp_3_bin_17.is_dead = "NaN"
        echo_amp_3_bin_17[:, 0, 0] = EA03B17

        echo_amp_1_bin_18 = dataset.createVariable("EA01B18", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_18.long_name = "Echo Amplitude 01 Bin 18"
        echo_amp_1_bin_18.standard_name = "echo_amplitude_01_bin_18"
        echo_amp_1_bin_18.short_name = "EA01B18"
        echo_amp_1_bin_18.units = "counts"
        echo_amp_1_bin_18.observation_type = "measured"
        echo_amp_1_bin_18.is_dead = "NaN"
        echo_amp_1_bin_18[:, 0, 0] = EA01B18

        echo_amp_2_bin_18 = dataset.createVariable("EA02B18", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_18.long_name = "Echo Amplitude 02 Bin 18"
        echo_amp_2_bin_18.standard_name = "echo_amplitude_02_bin_18"
        echo_amp_2_bin_18.short_name = "EA02B18"
        echo_amp_2_bin_18.units = "counts"
        echo_amp_2_bin_18.observation_type = "measured"
        echo_amp_2_bin_18.is_dead = "NaN"
        echo_amp_2_bin_18[:, 0, 0] = EA02B18

        echo_amp_3_bin_18 = dataset.createVariable("EA03B18", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_18.long_name = "Echo Amplitude 03 Bin 18"
        echo_amp_3_bin_18.standard_name = "echo_amplitude_03_bin_18"
        echo_amp_3_bin_18.short_name = "EA03B18"
        echo_amp_3_bin_18.units = "counts"
        echo_amp_3_bin_18.observation_type = "measured"
        echo_amp_3_bin_18.is_dead = "NaN"
        echo_amp_3_bin_18[:, 0, 0] = EA03B18

        echo_amp_1_bin_19 = dataset.createVariable("EA01B19", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_19.long_name = "Echo Amplitude 01 Bin 19"
        echo_amp_1_bin_19.standard_name = "echo_amplitude_01_bin_19"
        echo_amp_1_bin_19.short_name = "EA01B19"
        echo_amp_1_bin_19.units = "counts"
        echo_amp_1_bin_19.observation_type = "measured"
        echo_amp_1_bin_19.is_dead = "NaN"
        echo_amp_1_bin_19[:, 0, 0] = EA01B19

        echo_amp_2_bin_19 = dataset.createVariable("EA02B19", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_19.long_name = "Echo Amplitude 02 Bin 19"
        echo_amp_2_bin_19.standard_name = "echo_amplitude_02_bin_19"
        echo_amp_2_bin_19.short_name = "EA02B19"
        echo_amp_2_bin_19.units = "counts"
        echo_amp_2_bin_19.observation_type = "measured"
        echo_amp_2_bin_19.is_dead = "NaN"
        echo_amp_2_bin_19[:, 0, 0] = EA02B19

        echo_amp_3_bin_19 = dataset.createVariable("EA03B19", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_19.long_name = "Echo Amplitude 03 Bin 19"
        echo_amp_3_bin_19.standard_name = "echo_amplitude_03_bin_19"
        echo_amp_3_bin_19.short_name = "EA03B19"
        echo_amp_3_bin_19.units = "counts"
        echo_amp_3_bin_19.observation_type = "measured"
        echo_amp_3_bin_19.is_dead = "NaN"
        echo_amp_3_bin_19[:, 0, 0] = EA03B19

        echo_amp_1_bin_20 = dataset.createVariable("EA01B20", "f8", ("time", "lon", "lat",))
        echo_amp_1_bin_20.long_name = "Echo Amplitude 01 Bin 20"
        echo_amp_1_bin_20.standard_name = "echo_amplitude_01_bin_20"
        echo_amp_1_bin_20.short_name = "EA01B20"
        echo_amp_1_bin_20.units = "counts"
        echo_amp_1_bin_20.observation_type = "measured"
        echo_amp_1_bin_20.is_dead = "NaN"
        echo_amp_1_bin_20[:, 0, 0] = EA01B20

        echo_amp_2_bin_20 = dataset.createVariable("EA02B20", "f8", ("time", "lon", "lat",))
        echo_amp_2_bin_20.long_name = "Echo Amplitude 02 Bin 20"
        echo_amp_2_bin_20.standard_name = "echo_amplitude_02_bin_20"
        echo_amp_2_bin_20.short_name = "EA02B20"
        echo_amp_2_bin_20.units = "counts"
        echo_amp_2_bin_20.observation_type = "measured"
        echo_amp_2_bin_20.is_dead = "NaN"
        echo_amp_2_bin_20[:, 0, 0] = EA02B20

        echo_amp_3_bin_20 = dataset.createVariable("EA03B20", "f8", ("time", "lon", "lat",))
        echo_amp_3_bin_20.long_name = "Echo Amplitude 03 Bin 20"
        echo_amp_3_bin_20.standard_name = "echo_amplitude_03_bin_20"
        echo_amp_3_bin_20.short_name = "EA03B20"
        echo_amp_3_bin_20.units = "counts"
        echo_amp_3_bin_20.observation_type = "measured"
        echo_amp_3_bin_20.is_dead = "NaN"
        echo_amp_3_bin_20[:, 0, 0] = EA03B20'''

        # print(dataset.variables)
        dataset.close()
        print(dataset.file_format)

'''

def send2ftp(srcpath):, 0, 0

    latestncfile = latestFileinDirectory(srcpath)
    print(latestncfile)

    #session = ftplib.FTP("octopus.uvi.edu/", "Files", "ftpuserpassword")
    #file = open(srcpath+latestncfile, "rb")  # file to send
    #session.storbinary("STOR "+srcpath+latestncfile, file)  # send the file
    #file.close()  # close file and FTP
    #session.quit()
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect("octopus.uvi.edu", 21)
    ftp.login("Files", "ftpuserpassword")
    ftp.cwd("/array1/share/crownbay_sutronnc/")

    fp = open(localfile, 'rb')
    ftp.storbinary("STOR %s" % os.path.basename(latestncfile), fp, 1024)
    fp.close()
    print("after upload remotefile")


    print(latestncfile)

'''

if __name__ == "__main__":
    sutronurl = "http://sutronwin.com/goesweb/uvidock/"
    csvDir = "/home/caricoos/ftp/csvfolder/"
    ncDir = "/home/caricoos/ftp/ncfolder/"
    ogDir = "/home/caricoos/ftp/ogfolder/"
    jsonDir = "/var/www/html/requirements/"
    concatcsvDir = "/home/caricoos/ftp/concatcsvfolder/"

    convert2nc(concatcsvDir, ncDir)