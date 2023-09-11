import openpyxl
import wget
from xls2xlsx import XLS2XLSX
from openpyxl import load_workbook
import datetime
import re
import os

links_for_files = ['https://inefb.ru/images/Raspisanie/Ochka/1kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/2kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/3kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/4kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Mag_Ochka/mag1.xls',
                   'https://inefb.ru/images/Raspisanie/Mag_Ochka/mag2.xls']


def downloading_files(list_links):
    list_of_filenames = []
    for link in list_links:
        fname = link.split('/')[-1]
        wget.download(link, fname)
        x2x = XLS2XLSX(fname)
        x2x.to_xlsx(fname + "x")
        list_of_filenames.append(fname + "x")
    return list_of_filenames


def processing(filename):
    dict_teach_and_group = {}
    week = ""
    val = None

    workbook = load_workbook(filename)
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        group_row = None
        for row in sheet.rows:
            if row[1].value == "Время":
                # if not any(val.value is None for val in row):
                group_row = row
                continue
            if group_row is None:
                continue
            if row[0].value is not None:
                week = row[0].value
                week = ' '.join(week.split())
            if row[1].value is None:
                continue
            time = row[1].value

            key_time = week + " " + time
            dict_teach_and_group[key_time] = {}

            for i in range(2, len(row)):
                group = group_row[i].value
                group = str(group)
                if isinstance(row[i], openpyxl.cell.cell.MergedCell) and val is not None:
                    dict_teach_and_group[key_time][val] += [group.strip()]
                elif row[i].value is not None:
                    val = row[i].value
                    val = ' '.join(val.split())
                    if val not in dict_teach_and_group[key_time]:
                        dict_teach_and_group[key_time][val] = [group.strip()]
                    else:
                        dict_teach_and_group[key_time][val] += [group.strip()]
                else:
                    val = None
    return dict_teach_and_group


def date_check(date_str_checking):
    date_line = re.search('\d{2}-\d{2}-\d{4}|\d{2}.\d{2}.\d{4}|\d{2}.\d{2}.\d{2}|\d{2}..\d{2}.\d{4}', date_str_checking)
    date = datetime.datetime.strptime(date_line.group(), '%d.%m.%Y').date()
    return date


list = ['1kyrs.xlsx', '2kyrs.xlsx', '3kyrs.xlsx', '4kyrs.xlsx', 'mag1.xlsx', 'mag2.xlsx']

for val in list:
    if os.path.exists(val):
        os.remove(val)
    if os.path.exists(val[:-1]):
        os.remove(val[:-1])


def updating_schedule():
    list = ['1kyrs.xlsx', '2kyrs.xlsx', '3kyrs.xlsx', '4kyrs.xlsx', 'mag1.xlsx', 'mag2.xlsx']

    for val in list:
        if os.path.exists(val):
            os.remove(val)
        if os.path.exists(val[:-1]):
            os.remove(val[:-1])
    return downloading_files(links_for_files)


def printing_schedule():
    string_monday = ''
    string_tuesday = ''
    string_wednesday = ''
    string_thursday = ''
    string_friday = ''
    string_saturday = ''
    for fname in updating_schedule():
        mergeddicts = processing(fname)
        for key in mergeddicts:
            for name in mergeddicts[key]:
                if 'Янгирова' in name:
                    if datetime.date.today() <= date_check(key) <= (
                            datetime.date.today() + datetime.timedelta(days=6)):
                        if '1kyrs' in fname or '2kyrs' in fname or '3kyrs' in fname or '4kyrs' in fname or\
                                'mag1' in fname or 'mag2' in fname:
                            string_for_adding = str(key) + '\n' + "предмет: " + str(name) + '\n' + "группы(очное): " \
                                                + str(', '.join(mergeddicts[key][name])) + " " + '\n' + '\n'
                        else:
                            string_for_adding = str(key) + '\n' + "предмет: " + str(name) + '\n' + "группы: " \
                                                + str(', '.join(mergeddicts[key][name])) + " " + '\n' + '\n'
                        if 'Понедельник' in key:
                            string_monday += string_for_adding
                        elif 'Вторник' in key:
                            string_tuesday += string_for_adding
                        elif 'Среда' in key:
                            string_wednesday += string_for_adding
                        elif 'Четверг' in key:
                            string_thursday += string_for_adding
                        elif 'Пятница' in key:
                            string_friday += string_for_adding
                        elif 'Суббота' in key:
                            string_saturday += string_for_adding
    string_schedule = string_monday + '\n' + '\n' + string_tuesday + '\n' + '\n' + string_wednesday + '\n' + '\n' + \
                      string_thursday + '\n' + '\n' + string_friday + '\n' + '\n' + string_saturday
    return string_schedule
