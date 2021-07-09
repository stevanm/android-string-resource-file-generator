import os
import pandas as pd
import re

# Stevan Milic, TeleTrader, Android Developer

# load .xlsx file from google docs (using google api)
# docSheetUrl = "https://docs.google.com/spreadsheets/d/1hwDCUVGxxDalVG9Kt-vDHigvaTfirwLm13-veTzCgxc/edit#gid=2113229455"
# dataframe_data = pd.read_excel(docSheetUrl)

# load .xlsx file data (from local directory) ################################
dataframe_data = pd.read_excel("StockMarketsMobileAppStrings.xlsx")

# remove useless columns ################
# 'project' column
del dataframe_data["project"]

# language that will not be translated
# if you want to translate ex. 'zh-rTW' language just remove corresponding line of code
del dataframe_data["ar"]
del dataframe_data["ca"]
del dataframe_data["el"]
del dataframe_data["gl"]
del dataframe_data["hi"]
del dataframe_data["iw"]
del dataframe_data["sl"]
del dataframe_data["th"]
del dataframe_data["uk"]
del dataframe_data["vi"]
del dataframe_data["zh-rTW"]

# duplicate key column ########################
dataframe_data['key0'] = dataframe_data['key']
data = dataframe_data.set_index('key0')

# get columns name ##########################
dataframe_columns = dataframe_data.columns
# print(dataframe_columns)

# make 'android' directory for resource file #################
android_directory_path = os.getcwd() + os.path.sep + "android"
# print("Path: ", android_directory_path)
if not os.path.exists(android_directory_path):
    os.mkdir(android_directory_path)

# positioning inside directory ######################
os.chdir(android_directory_path)
for c in dataframe_columns:
    if c == 'key' or c == 'key0':
        continue
    if c == 'en':
        valdir_path = "values"
    else:
        valdir_path = "values" + "-" + c
    os.mkdir(valdir_path)
    os.chdir(valdir_path)
    # print("dir: " + valdir_path)
    with open('strings.xml', mode='w+', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>')
        f.write("\n")
        f.write('<resources>')
        f.write("\n")
        # write to strings.xml file
        # If value for some key not exist for specific language
        # in strings.xml file (for that language) will appear row like
        # <string name="appstore_title">-</string>, where special value is value '-'.
        # Value '>-<' can be use for searching untranslated string for specific language
        for k in data['key']:
            f.write('\t')
            f.write('<string name="')
            f.write(str(k).strip())
            f.write('">')
            str_value = str(data.loc[k, c])
            # & -> &amp;
            str_value = re.sub("&(?!amp;)", "&amp;", str_value)
            # & amp; -> &amp;
            str_value = re.sub("&\bamp;", "&amp;", str_value)
            # remove blanco in format string: '% 1 $ s'  -> '%1$s'
            # str_value = re.sub("\b%\b(d+)\b[$]\bs\b", "\b%\\1[$]s\b", str_value)
            str_value = re.sub("%\b?(d+)\b?[$]\b?s", "%\\1[$]s", str_value)
            # \ '  -> \'
            str_value = re.sub("\ '", "\'", str_value)
            # txt'txt  -> txt\'txt
            str_value = re.sub("(w+)'(w+)", "\\1\'\\2", str_value)
            # str_value = r'{0}'.format(str(data.loc[k, c]))
            if str_value == "nan" or len(str_value.strip()) == 0:
                str_value = '-'
            f.write(str_value)
            f.write('</string>')
            f.write("\n")
        # end for
        f.write('</resources>')
    os.chdir("..")

# print(data)
