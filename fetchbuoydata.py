#alphabranch
import os
from datetime import datetime, timedelta
import datetime
import requests
import glob
from jdcal import gcal2jd
from dateutil import parser
import pandas as pd
from base64 import encodebytes

def sendemail(sender_address, sender_pass, attach_file_name, receiver_address):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from email.mime.application import MIMEApplication
    mail_content = '''Hello,

    This is the Crown Bay weather station alert bot.
    There are enough missing data from the weather station to trigger this email. Please see the attached log file.

    If you have any question, please contact the data manager @ CMES.
    '''
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Urgent Crown Bay Weather Station. See attachment.'
    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #attach_file_name = 'TP_python_prev.pdf'
    attachment = os.path.basename(attach_file_name)
    
    fp = open(attach_file_name, 'rb')
    part = MIMEBase('application', "octet-stream")
    part.set_payload(encodebytes(fp.read()).decode())
    fp.close()
    part.add_header('Content-Transfer-Encoding', 'base64')
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % attachment)
    message.attach(part)   # msg is an instance of MIMEMultipart()
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

def fetchcurrentFiles(src):

    sutronurl = 'http://sutronwin.com/goesweb/uvidock/'

    preURL = sutronurl + 'virgin_islands-' + str(pastdays_julianyear).zfill(2)[2:] + str(
        pastdays_julianday).zfill(3) + '-'

    prefilename = 'virgin_islands-' + str(pastdays_julianyear).zfill(2)[2:] + str(pastdays_julianday).zfill(3) + '-'

    if not os.path.exists(src):
        os.makedirs(src)

    timedelta = ["000050", "000650", "001250", "001850", "002450", "003050", "003650", "004250", "004850", "005450",
                 "010050", "010650", "011250", "011850", "012450", "013050", "013650", "014250", "014850", "015450",
                 "020050", "020650", "021250", "021850", "022450", "023050", "023650", "024250", "024850", "025450",
                 "030050", "030650", "031250", "031850", "032450", "033050", "033650", "034250", "034850", "035450",
                 "040050", "040650", "041250", "041850", "042450", "043050", "043650", "044250", "044850", "045450",
                 "050050", "050650", "051250", "051850", "052450", "053050", "053650", "054250", "054850", "055450",
                 "060050", "060650", "061250", "061850", "062450", "063050", "063650", "064250", "064850", "065450",
                 "070050", "070650", "071250", "071850", "072450", "073050", "073650", "074250", "074850", "075450",
                 "080050", "080650", "081250", "081850", "082450", "083050", "083650", "084250", "084850", "085450",
                 "090050", "090650", "091250", "091850", "092450", "093050", "093650", "094250", "094850", "095450",
                 "100050", "100650", "101250", "101850", "102450", "103050", "103650", "104250", "104850", "105450",
                 "110050", "110650", "111250", "111850", "112450", "113050", "113650", "114250", "114850", "115450",
                 "120050", "120650", "121250", "121850", "122450", "123050", "123650", "124250", "124850", "125450",
                 "130050", "130650", "131250", "131850", "132450", "133050", "133650", "134250", "134850", "135450",
                 "140050", "140650", "141250", "141850", "142450", "143050", "143650", "144250", "144850", "145450",
                 "150050", "150650", "151250", "151850", "152450", "153050", "153650", "154250", "154850", "155450",
                 "160050", "160650", "161250", "161850", "162450", "163050", "163650", "164250", "164850", "165450",
                 "170050", "170650", "171250", "171850", "172450", "173050", "173650", "174250", "174850", "175450",
                 "180050", "180650", "181250", "181850", "182450", "183050", "183650", "184250", "184850", "185450",
                 "190050", "190650", "191250", "191850", "192450", "193050", "193650", "194250", "194850", "195450",
                 "200050", "200650", "201250", "201850", "202450", "203050", "203650", "204250", "204850", "205450",
                 "210050", "210650", "211250", "211850", "212450", "213050", "213650", "214250", "214850", "215450",
                 "220050", "220650", "221250", "221850", "222450", "223050", "223650", "224250", "224850", "225450",
                 "230050", "230650", "231250", "231850", "232450", "233050", "233650", "234250", "234850", "235450"]
    
    timedelta2 = '000050'

    for i in timedelta:
        fullURL = preURL + i
        fullURL2 = fullURL[:-1] + '1'
        filename = prefilename + i
        filename2 = filename[:-1] + '1'
        print("======================================================================================")

        if os.path.isfile(src + filename + ".csv"):
            print(fullURL)
            print("file exist")

        elif os.path.isfile(src + filename2 + ".csv"):
            print(fullURL2)
            print('file exist')

        else:
            request = requests.get(fullURL)
            if request.status_code == 200:
                print(fullURL)
                print(200)
                with open(src + filename + ".csv", 'wb') as f:
                    f.write(request.content)
                    f.close()
            else:
                print(fullURL)
                print(404)

                try:
                    print("attempting secondary link....")
                    print(fullURL2)
                    request = requests.get(fullURL2)
                    if request.status_code == 200:
                        print(200)
                        with open(src + filename2 + ".csv", 'wb') as f:
                            f.write(request.content)
                            f.close()

                    else:
                        print(404)
                        print("link/file doesn't exist yet, or Sutron may be down. \n"
                              "Please check the online directory: " + fullURL2)

                except:
                    print("no file found")

    preURL2 = sutronurl + 'virgin_islands-' + str(tomorrowpastdays_jyear).zfill(2)[2:] + str(tomorrowpastdays_jday).zfill(3) + '-'
    print(preURL2)
    prefilename2 = 'virgin_islands-' + str(tomorrowpastdays_jyear).zfill(2)[2:] + str(tomorrowpastdays_jday).zfill(3) + '-'
    print(prefilename2)

    fullURL = preURL2 + timedelta2
    print(fullURL)
    fullURL2 = fullURL[:-1] + '1'
    filename = prefilename2 + timedelta2
    filename2 = filename[:-1] + '1'
    print("======================================================================================")

    if os.path.isfile(src + filename + ".csv"):
        print(fullURL)
        print("file exist")

    elif os.path.isfile(src + filename2 + ".csv"):
        print(fullURL2)
        print('file exist')

    else:
        request = requests.get(fullURL)
        if request.status_code == 200:
            print(fullURL)
            print(200)
            with open(src + filename + ".csv", 'wb') as f:
                f.write(request.content)
                f.close()
        else:
            print(fullURL)
            print(404)

            try:
                print("attempting secondary link....")
                print(fullURL2)
                request = requests.get(fullURL2)
                if request.status_code == 200:
                    print(200)
                    with open(src + filename2 + ".csv", 'wb') as f:
                        f.write(request.content)
                        f.close()

                else:
                    print(404)
                    print("link/file doesn't exist yet, or Sutron may be down. \n"
                          "Please check the online directory: " + fullURL2)

            except:
                print("no file found")

def process_csv(src, out, log):
    fmt_date, savenameformat = "", ""
    good_count, partial_count, none_count, total_cnt, total_bad = 0, 0, 0, 0, 0

    if not os.path.exists(out):
        os.makedirs(out)
    log_file_path = log + "vi_stt_crownbay_" + str(pastdays_julianyear).zfill(2) + str(pastdays_julianday).zfill(3) + "_log.txt"
    f = open(log_file_path, 'w+')
    f.write("URL = http://sutronwin.com/goesweb/uvidock/?C=N;O=D\n")
    csv_directory = sorted(glob.glob(src + "*.csv"))

    columns = ["Station", "Date(GMT)", "Time(GMT)", "WSPD(kts)",
               "WDIR(degM)", "GST(kts)", "PRES(mm)", "ATMP(degC)", "RH(percent)", "RAIN(inches/hour)",
               "HAIL(hits/in^2/hour)", "BATTV(Volts)", "InstDEPTH(0.1meter)", "InstHEADING(degM)",
               "InstPITCH(deg)", "InstROLL(deg)", "InstPRES(kPa)",
               "EVB(01mm/s)", "NVB(01mm/s)", "EVB(02mm/s)", "NVB(02mm/s)", "EVB(03mm/s)", "NVB(03mm/s)",
               "EVB(04mm/s)", "NVB(04mm/s)", "EVB(05mm/s)", "NVB(05mm/s)", "EVB(06mm/s)", "NVB(06mm/s)",
               "EVB(07mm/s)", "NVB(07mm/s)", "EVB(08mm/s)", "NVB(08mm/s)", "EVB(09mm/s)", "NVB(09mm/s)",
               "EVB(10mm/s)", "NVB(10mm/s)", "EVB(11mm/s)", "NVB(11mm/s)", "EVB(12mm/s)", "NVB(12mm/s)",
               "EVB(13mm/s)", "NVB(13mm/s)", "EVB(14mm/s)", "NVB(14mm/s)", "EVB(15mm/s)", "NVB(15mm/s)",
               "EVB(16mm/s)", "NVB(16mm/s)", "EVB(17mm/s)", "NVB(17mm/s)", "EVB(18mm/s)", "NVB(18mm/s)",
               "EVB(19mm/s)", "NVB(19mm/s)", "EVB(20mm/s)", "NVB(20mm/s)",
               "MCSPD(kts)", "MCDIR(degM)",
               "PGB01(percent)", "PGB02(percent)", "PGB03(percent)", "PGB04(percent)", "PGB05(percent)",
               "PGB06(percent)", "PGB07(percent)", "PGB08(percent)", "PGB09(percent)", "PGB10(percent)",
               "PGB11(percent)", "PGB12(percent)", "PGB13(percent)", "PGB14(percent)", "PGB15(percent)",
               "PGB16(percent)", "PGB17(percent)", "PGB18(percent)", "PGB19(percent)", "PGB20(percent)",
               "EA01B01(counts)", "EA02B01(counts)", "EA03B01(counts)",
               "EA01B02(counts)", "EA02B02(counts)", "EA03B02(counts)",
               "EA01B03(counts)", "EA02B03(counts)", "EA03B03(counts)",
               "EA01B04(counts)", "EA02B04(counts)", "EA03B04(counts)",
               "EA01B05(counts)", "EA02B05(counts)", "EA03B05(counts)",
               "EA01B06(counts)", "EA02B06(counts)", "EA03B06(counts)",
               "EA01B07(counts)", "EA02B07(counts)", "EA03B07(counts)",
               "EA01B08(counts)", "EA02B08(counts)", "EA03B08(counts)",
               "EA01B09(counts)", "EA02B09(counts)", "EA03B09(counts)",
               "EA01B10(counts)", "EA02B10(counts)", "EA03B10(counts)",
               "EA01B11(counts)", "EA02B11(counts)", "EA03B11(counts)",
               "EA01B12(counts)", "EA02B12(counts)", "EA03B12(counts)",
               "EA01B13(counts)", "EA02B13(counts)", "EA03B13(counts)",
               "EA01B14(counts)", "EA02B14(counts)", "EA03B14(counts)",
               "EA01B15(counts)", "EA02B15(counts)", "EA03B15(counts)",
               "EA01B16(counts)", "EA02B16(counts)", "EA03B16(counts)",
               "EA01B17(counts)", "EA02B17(counts)", "EA03B17(counts)",
               "EA01B18(counts)", "EA02B18(counts)", "EA03B18(counts)",
               "EA01B19(counts)", "EA02B19(counts)", "EA03B19(counts)",
               "EA01B20(counts)", "EA02B20(counts)", "EA03B20(counts)"]

    for file in csv_directory:

        csvname = file[-31:]
        csvsize = os.stat(file).st_size
        year = file[-16:-14]
        jday = file[-14:-11]
        hour = file[-10:-8]
        min = file[-8:-6]
        sec = '00'
        time = hour + ':' + min + ':' + sec

        greg_date = datetime.datetime.strptime(year + jday, '%y%j').date()
        parsedatetime = parser.parse(str(greg_date) + ' ' + time) - datetime.timedelta(minutes=6)
        fmt_greg_date = datetime.date.strftime(parsedatetime, "%m/%d/%Y %H:%M:%S")
        fmt_date = fmt_greg_date[:-9]
        fmt_time = fmt_greg_date[11:]
        fmt_year = str(parsedatetime.timetuple().tm_year)[2:]
        fmt_yday = str(parsedatetime.timetuple().tm_yday).zfill(3)

        if csvsize == 0:
            print(csvname + " is empty, generating values....")
            f.write(csvname[:-4] + " no data present....\n")

            csvdf = pd.DataFrame(columns=columns)
            csvdf.insert(loc=3, column='Latitude', value=18.331414)
            csvdf.insert(loc=4, column='Longitude', value=-64.951350)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            csvdf = csvdf.append({'Station': 'CROWN BAY', 'Latitude': 18.331414, 'Longitude': -64.951350,
                                  'Date(GMT)': fmt_date, 'Time(GMT)': fmt_time}, ignore_index=True)
            csvdf = csvdf.fillna('NaN')
            savenameformat = 'virgin_islands-' + str(fmt_year) + str(fmt_yday) + '-' + fmt_time.replace(':', '') + '.csv'
            csvdf.to_csv(out + savenameformat, index=False)
            none_count += 1

        elif csvsize < 300:

            print(csvname + " ADCP data is missing....")
            f.write(csvname[:-4] + " ADCP data missing....\n")

            # read, format and insert csv.
            csvdf = pd.read_csv(file, na_filter=True, delimiter=",", header=None, index_col=None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            csvdf.columns = columns
            csvdf.insert(loc=3, column='Latitude', value=18.331414)
            csvdf.insert(loc=4, column='Longitude', value=-64.951350)
            csvdf["Station"] = csvdf["Station"].replace("UVIDOCK", "CROWN BAY")
            # formatting and changing datetime
            strdate = csvdf['Date(GMT)'].iloc[0]
            strtime = csvdf['Time(GMT)'].iloc[0]
            datetimeinGMT = parser.parse(strdate + ' ' + strtime)
            GMTdateinstr = str(datetimeinGMT)[:10]
            GMTtimeinstr = str(datetimeinGMT)[-8:]
            formatteddate = datetime.datetime.strptime(GMTdateinstr, '%Y-%m-%d')
            GMTformatteddate = datetime.date.strftime(formatteddate, "%m/%d/%Y")
            # datetime2julian = datetime.datetime.strptime(str(datetimeinGMT), '%Y-%m-%d %H:%M:%S')
            yearday = str(datetimeinGMT.timetuple().tm_yday).zfill(3)
            # replaces the local date time with GMT
            csvdf['Date(GMT)'] = csvdf['Date(GMT)'].replace(strdate, GMTformatteddate)
            csvdf['Time(GMT)'] = csvdf['Time(GMT)'].replace(strtime, GMTtimeinstr)

            # fills the rest of the blank columns with NaN
            csvdf = csvdf.fillna("NaN")
            savenameformat = 'virgin_islands-' + str(datetimeinGMT)[2:-15] + yearday + '-' + GMTtimeinstr.replace(':',
                                                                                                                  '') + '.csv'
            csvdf.to_csv(out + savenameformat, index=False)
            partial_count += 1

        else:

            print(csvname + " has full data")
            # read, format and insert csv.
            csvdf = pd.read_csv(file, na_filter=True, delimiter=",", header=None, index_col=None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_rows', None)
            csvdf.columns = columns
            csvdf.insert(loc=3, column='Latitude', value=18.331414)
            csvdf.insert(loc=4, column='Longitude', value=-64.951350)
            csvdf["Station"] = csvdf["Station"].replace("UVIDOCK", "CROWN BAY")
            # formatting and changing datetime
            strdate = csvdf['Date(GMT)'].iloc[0]
            strtime = csvdf['Time(GMT)'].iloc[0]
            datetimeinGMT = parser.parse(strdate + ' ' + strtime)
            GMTdateinstr = str(datetimeinGMT)[:10]
            GMTtimeinstr = str(datetimeinGMT)[-8:]
            formatteddate = datetime.datetime.strptime(GMTdateinstr, '%Y-%m-%d')
            GMTformatteddate = datetime.date.strftime(formatteddate, "%m/%d/%Y")
            # datetime2julian = datetime.datetime.strptime(str(datetimeinGMT), '%Y-%m-%d %H:%M:%S')
            yearday = str(datetimeinGMT.timetuple().tm_yday).zfill(3)
            # replaces the local date time with GMT
            csvdf['Date(GMT)'] = csvdf['Date(GMT)'].replace(strdate, GMTformatteddate)
            csvdf['Time(GMT)'] = csvdf['Time(GMT)'].replace(strtime, GMTtimeinstr)

            # fills the rest of the blank columns with NaN
            csvdf = csvdf.fillna("NaN")
            savenameformat = 'virgin_islands-' + str(datetimeinGMT)[2:-15] + yearday + '-' + GMTtimeinstr.replace(':',
                                                                                                            '') + '.csv'
            csvdf.to_csv(out + savenameformat, index=False)
            good_count += 1
    
    total_bad = partial_count + none_count
    total_cnt = good_count + partial_count + none_count
    f.write("There are: \n" + str(good_count) + "/" + str(total_cnt) + " files with complete data.\n" +
            str(partial_count) + "/" + str(total_cnt) + " files with partial data.\n" +
            str(none_count) + "/" + str(total_cnt) + " with no data.\n")
    f.write("Date of log files: "+ str(fmt_date)+"Z\n")
    f.write("Log generated on: "+ str(datetime.datetime.utcnow().strftime("%m/%d/%Y %H:%m"))+"Z\n")
    f.close()

    #send email if the number of missing data is greater than the # assigned.
    if(total_bad > 30):
        print(log_file_path)
        sendemail("cmesuvistt@gmail.com", "cmesuniversity123",
                  log_file_path, "andyvp@live.com")

def concat_csv(src, out):

    csv_directory = sorted(glob.glob(src + "*.csv"))
    list = []
    for file in csv_directory:
        df = pd.read_csv(file, index_col=None, header=0)
        list.append(df)
        print(file)

    frame = pd.concat(list, axis=0, ignore_index=True)
    df = pd.DataFrame(frame)
    df = df.fillna("NaN")
    df.to_csv(out+"vi_stt_crownbay_"+str(pastdays_julianyear).zfill(2)[2:]+str(pastdays_julianday).zfill(3)+".met.dopp.csv", index=None, header=True)
    #print(frame)

if __name__ == '__main__':
    csvDir = "/home/caricoos/ftp/csvfolder/"
    ncDir = "/home/caricoos/ftp/ncfolder/"
    ogDir = "/home/caricoos/ftp/ogfolder/"
    logDir = "/home/caricoos/ftp/logfolder/"
    concatcsvDir = "/home/caricoos/ftp/concatcsvfolder/"

    #current_date = datetime.date.today()
    pastdays = 1

    current_date = datetime.datetime.utcnow()
    current_julianyear = current_date.timetuple().tm_year
    current_julianday = current_date.timetuple().tm_yday
    pastdays_date = current_date - timedelta(days=pastdays)
    pastdays_julianyear = pastdays_date.timetuple().tm_year
    pastdays_julianday = pastdays_date.timetuple().tm_yday
    tomorrowpastdays_date = pastdays_date + timedelta(days=1)
    tomorrowpastdays_jyear = tomorrowpastdays_date.timetuple().tm_year
    tomorrowpastdays_jday = tomorrowpastdays_date.timetuple().tm_yday

    y_ogDir = ogDir + str(pastdays_julianyear).zfill(2)[2:] + str(pastdays_julianday).zfill(3) + '/'
    y_csvDir = csvDir + str(pastdays_julianyear).zfill(2)[2:] + str(pastdays_julianday).zfill(3) + '/'

    if not os.path.exists(csvDir):
        os.makedirs(csvDir)
        os.makedirs(ncDir)
        os.makedirs(ogDir)
        os.makedirs(logDir)
        os.makedirs(concatcsvDir)

    fetchcurrentFiles(y_ogDir)
    process_csv(y_ogDir, y_csvDir, logDir)
    concat_csv(y_csvDir, concatcsvDir)