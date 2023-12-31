from xls2xlsx import XLS2XLSX
import os
from urllib import request


links_for_files = ['https://inefb.ru/images/Raspisanie/Ochka/1kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/2kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/3kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka/4kyrs.xls',
                   'https://inefb.ru/images/Raspisanie/Mag_Ochka/mag1.xls',
                   'https://inefb.ru/images/Raspisanie/Mag_Ochka/mag2.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka_Zaochka/4kyrsOZ.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka_Zaochka/2kyrsOZ.xls',
                   'https://inefb.ru/images/Raspisanie/Mag_Ochka/mag1oz.xls',
                   'https://inefb.ru/images/Raspisanie/Ochka_Zaochka/1kyrsOZ.xls']




def downloading_files(list_links):
    list_of_filenames = []
    for link in list_links:
        fname = link.split('/')[-1]
        response = request.urlretrieve(link, fname)
        x2x = XLS2XLSX(fname)
        x2x.to_xlsx(fname + "x")
        list_of_filenames.append(fname + "x")
    return list_of_filenames


def updating_schedule():
    list = ['1kyrs.xlsx', '2kyrs.xlsx', '3kyrs.xlsx', '4kyrs.xlsx', 'mag1.xlsx', 'mag2.xlsx', '4kyrsOZ.xlsx',
            '2kyrsOZ.xlsx','1kyrsOZ.xlsx','mag1oz.xlsx' ]

    for val in list:
        if os.path.exists(val):
            os.remove(val)
        if os.path.exists(val[:-1]):
            os.remove(val[:-1])
    return downloading_files(links_for_files)


updating_schedule()