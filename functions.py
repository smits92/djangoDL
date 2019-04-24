import numpy as np
import datetime
import pandas as pd
import os



def get_hour(time):
    """
    Function to extract the hour in 'int' from a string
    :param time: (str) column with time values (only numbers)
    :return: hour('int') or NaN if the string was not a number
    """
    try:
        _ = int(time)
        if time != time:
            hour = np.nan
        elif len(time) == 2:
            hour = 0
        elif len(time) == 3:
            hour = int(time[:1])
        elif len(time) == 4:
            hour = int(time[:2])
        else:
            hour = np.nan
    except ValueError:
        hour = np.nan
    return hour
def get_minutes(time):
    """
    Function to extract the minutes in 'int' from a string
    :param time: (str) column with time values (only numbers)
    :return: minutes('int') or NaN if the string was not a number
    """
    try:
        _ = int(time)
        if time != time:
            minutes = np.nan
        elif len(time) == 2:
            minutes = int(time[:2])
        elif len(time) == 3:
            minutes = int(time[-2:])
        elif len(time) == 4:
            minutes = int(time[-2:])
        else:
            minutes = np.nan
    except ValueError:
        minutes = np.nan
    return minutes
def get_date(date):
    """
    Function to convert the date column to Datetime.date format
    :param date: (str) column with the date values
    :return: date in Datetime.date format
    """
    try:
        if date != date:
            day = np.nan
        elif len(date) == 3:
            day = datetime.date(2017,int(date[-2:]),int(date[:1]))
        else:
            date = date[:4]
            day = datetime.date(2017,int(date[-2:]),int(date[:2]))
    except ValueError:
        day = np.nan
    return day
def get_weekday(day):
    """
    Function to get the day of the week from a Datetime.date value
    :param day: column with Datetime.date values
    :return: day of the week in number, e.g 0 = Monday
    """
    if day!=day:
        return np.nan
    else:
        return day.weekday()
def get_dayname(day):
    """
    Function to convert the day number into day name
    :param day: (int) column with the day numbers (0-6)
    :return: name of the day
    """
    if day == 0:
        day_name = 'Mon'
    elif day == 1:
        day_name = 'Tue'
    elif day == 2:
        day_name = 'Wed'
    elif day == 3:
        day_name = 'Thu'
    elif day == 4:
        day_name = 'Fri'
    elif day == 5:
        day_name = 'Sat'
    elif day == 6:
        day_name = 'Sun'
    return day_name
def get_shifts(time):
    """
    Function to define the shifts
    :param time: (int) column with the time of the day
    :return: (str) name of the shift it belongs to
    """
    if time >= 6 and time < 14:
        shift = "Morning"
    elif time >= 14 and time < 22:
        shift = "Afternoon"
    else:
        shift = "Night"
    return shift
def get_plotpath(path, id):
    """
    Function to make the correct path to load the graph depending on the id number
    :param path: (str) predetermined full path with a '$' instead of the plot number
    e.g. 'Statistics/tmp_main_$.json'
    :param id: plot number to graph
    :return: correct path, e.g. Statistics/tmp_main_1.json'
    """
    if id < 10:
        new_path = path.replace('$', str(id))
    elif id > 10:
        new_path = []
        d = [int(i) for i in str(id)]
        for i in d:
            new_path.append(path.replace('$', str(i)))
    return new_path

def fix_cols(df, cols):
    """
    Function to delete all non numerical characters from a column
    :param df: Data Frame
    :param cols: array with the names of the columns to be "fixed"
    :return: Data Frame with fixed values in the columns 'cols'
    """
    for i in cols:
        if i != '':
            df[i] = df[i].str.replace(" ","")
            df[i] = df[i].str.replace(":","")
            df[i] = df[i].str.replace(".","")
            df[i] = df[i].str.replace("'","")
            df[i] = df[i].str.replace(",","")
            df[i] = df[i].str.replace("t","7")
    return df
def filter_date(df, date1, date2):
    """
    Function to filter the data frame with values between two dates
    :param df: whole data frame
    :param date1: start date in Datetime.date format
    :param date2: end date in Datetime.date format
    :return: filtered data frame
    """
    date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
    date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
    df = df.query('@date1 <= Date <= @date2')
    df = df.reset_index(drop=True)

    return df
def filter_room(df,flt):
    """
    Function to filter the Room column for all the values that start with the input value(flt)
    :param df: Whole data frame
    :param flt: str or int to use as filter
    :return: filtered data frame
    """
    try:
        df = df[df.Room.str.startswith(flt)]
    except:
        if len(flt) > 0:
            df = df[(df['Room'] // (10**(4-len(flt)))) == int(flt)]
    return df
def open_file(path):
    """
    Function to open a file and transform it to pandas Data Frame. Set to only open .csv files
    that are separated by ";".
    :param path: full path of the file (including file name)
    :return: data frame with the data from the opened file
    """
    if path.endswith('.csv') or path.endswith('.txt'):
        df = pd.read_csv(path, sep=";", decimal=',', dtype='str')
    else:
        df = "Incorrect file"
    return df
def new_table(df,cols,cols2fix):
    """
    Function to generate a new data frame with own calculated values and new row names
    :param df: whole new data frame
    :param cols: names of the columns in order [Date, Room, Call Type, Time of call, nurse entrance, nurse leaves]
    :param cols2fix: name of the columns tha have numerical values.
    :return: new data frame
    """
    nr_old_cols = df.columns.size

    #Time and date correction
    df = fix_cols(df, cols2fix)

    #New Columns/Indicators
    df['Date'] = df[cols[0]].apply(get_date)
    df['Room'] = df[cols[1]]
    df['Call_Type'] = df[cols[2]]
    df['Weekday'] = df['Date'].apply(get_weekday)
    df['Calls'] = pd.Series(np.ones(df.shape[0]), index=df.index)
    df['Call_Hr'] = df[cols[3]].apply(get_hour)
    df['Call_Min'] = df[cols[3]].apply(get_minutes)
    df['Shift'] = df['Call_Hr'].apply(get_shifts)
    df['Ent_Hr'] = df[cols[4]].apply(get_hour)
    df['Ent_Min'] = df[cols[4]].apply(get_minutes)
    try:
        df['Ext_Hr'] = df[cols[5]].apply(get_hour)
        df['Ext_Min'] = df[cols[5]].apply(get_minutes)
    except:
        df['Ext_Hr'] = df[cols[4]].apply(get_hour)
        df['Ext_Min'] = df[cols[4]].apply(get_minutes)

    df['Resp_Time'] = (df['Ent_Hr']*60 + df['Ent_Min']) - (df['Call_Hr']*60 + df['Call_Min'])
    df['Resp_Time'] = df['Resp_Time'].apply(diff_err)

    df['Dur'] = (df['Ext_Hr']*60 + df['Ext_Min']) - (df['Call_Hr']*60 + df['Call_Min'])
    df['Dur'] = df['Dur'].apply(diff_err)

    nr_new_cols = df.columns.size - nr_old_cols  # calculate number of new columns
    cols = df.columns[-nr_new_cols:]  # delete old columns
    df = df[cols]  # delete old columns

    return df
def diff_err(x):
    """
    Function made for teh calculation of Duration time of the nurse, returns a NaN in casa the duration was negative
    :param x: number
    :return: NaN if negative, same number if positive
    """
    if x < 0:
        x = np.nan
    else:
        x = x
    return x

def myPlot(df, id, outliers, per_room):
    """
    Function that calculates the values for each type of plot and saves the values in a .json file
    :param df: data frame
    :param id: number of graph to calculate
    :param outliers: outliers for nurse time (number of calls cannot have outliers)
    :param per_room: boolean, if true divide values by the number of unique rooms
    :return: nothing, saves the values to memory
    """
    opt = 'table'  # format for saving the .json file
    path = 'Statistics/static/Statistics'  # Path to save the file
    outliers = int(outliers)

    df.Call_Type = df.Call_Type.str.lower()  # Make all Call Types lowercase

    i = [int(d) for d in str(id)]

    for plot in i:
        if plot == 1:
            title = "Calls per Hour"
            xaxis = "Hour"
            yaxis = "Number of Calls"
            plot_df = df[(df.Call_Type.str.contains('ruf')==True)].groupby(['Call_Hr'])
            temp_df = plot_df['Calls'].sum() / df['Date'].nunique()

            temp_df.to_json(os.path.join(path,'tmp_main_1.json'), orient=opt)
            plot_df['Resp_Time'].mean().to_json(os.path.join(path, 'tmp_sec_1.json'), orient=opt)

        elif plot == 2:
            title = "Calls per Shift"
            xaxis = "Weekday / Shift"
            yaxis = "Number of Calls"
            plot_df = df[(df.Call_Type.str.contains('ruf')==True)].groupby(['Weekday', 'Shift'])
            temp_df = plot_df['Calls'].sum()/df['Date'].nunique()

            temp_df.to_json(os.path.join(path,'tmp_main_2.json'),orient=opt)
            plot_df['Resp_Time'].mean().to_json(os.path.join(path,'tmp_sec_2.json'),orient=opt)

        elif plot == 4:
            title = "Calls per Day"
            xaxis = "Date"
            yaxis = "Number of Calls"
            plot_df = df[(df.Call_Type.str.contains('ruf')==True)].groupby(['Date'])
            if per_room:
                temp_df = plot_df['Calls'].sum() / plot_df['Room'].nunique()
            else:
                temp_df = plot_df['Calls'].sum()

            temp_df.to_json(os.path.join(path,'tmp_main_4.json'),orient=opt)
            plot_df['Room'].nunique().to_json(os.path.join(path, 'tmp_sec_4.json'), orient=opt)

        elif plot == 5:
            title = "Nurse Time per Hour"
            xaxis = "Hour"
            yaxis = "Nurse Time (min)"
            plot_df = df[(df.Call_Type.str.contains('ruf')==False) & (df['Dur'] < outliers)].groupby(['Call_Hr'])
            if per_room:
                temp_df = plot_df['Dur'].sum()/plot_df['Room'].nunique()/plot_df['Date'].nunique()
            else:
                temp_df = plot_df['Dur'].sum()/plot_df['Date'].nunique()
            temp_df.to_json(os.path.join(path,'tmp_main_5.json'),orient=opt)

        elif plot == 6:
            title = "Nurse Time per Shift"
            xaxis = "Weekday / Shift"
            yaxis = "Nurse Time (min)"
            plot_df = df[(df.Call_Type.str.contains('ruf')==False) & (df['Dur'] < outliers)].groupby(['Weekday','Shift'])
            if per_room:
                temp_df = plot_df['Dur'].sum()/plot_df['Room'].nunique()/plot_df['Date'].nunique()
            else:
                temp_df = plot_df['Dur'].sum()/ plot_df['Date'].nunique()
            temp_df.to_json(os.path.join(path,'tmp_main_6.json'),orient=opt)

        elif plot == 3:
            title = "Nurse Time per Day"
            xaxis = "Date"
            yaxis = "Nurse Time (min)"
            plot_df = df[(df.Call_Type.str.contains('ruf')==False) & (df['Dur'] < outliers)].groupby(['Date'])
            if per_room:
                temp_df = plot_df['Dur'].sum()/plot_df['Room'].nunique()
            else:
                temp_df = plot_df['Dur'].sum()

            temp_df.to_json(os.path.join(path,'tmp_main_3.json'),orient=opt)
            plot_df['Room'].nunique().to_json(os.path.join(path, 'tmp_sec_3.json'), orient=opt)

        elif plot == 7: #check how to iterate rows
            title = "Re-Calls per Room"
            xaxis = "Rooms"
            yaxis = "Number of Re-Calls"
            plot_df = df[(df.Call_Type.str.contains('ruf')==True)].groupby(['Date','Room'])
            temp_df = plot_df['Call_Hr'].count() - plot_df['Call_Hr'].nunique()
            temp_df = temp_df.reset_index()
            temp_df = temp_df.groupby('Room')['Call_Hr'].sum()

            temp_df.to_json(os.path.join(path,'tmp_main_7.json'),orient=opt)

        elif plot == 8:  # Re-Calls per Day
            title = "Re-Calls per Day"
            xaxis = "Date"
            yaxis = "Number of Re-Calls"
            plot_df = df[(df.Call_Type.str.contains('ruf') == True)].groupby(['Date','Room'])
            temp_df = plot_df['Call_Hr'].count() - plot_df['Call_Hr'].nunique()
            temp_df = temp_df.reset_index()
            temp_df = temp_df.groupby('Date')['Call_Hr'].sum()

            temp_df.to_json(os.path.join(path, 'tmp_main_8.json'), orient=opt)

    return title, xaxis, yaxis


