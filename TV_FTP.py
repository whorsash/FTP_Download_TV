import ftplib
import os

from ftplib import FTP_TLS

from config import host, port, user, pwd

import pandas as pd

import socket


# Подключение к FTP
def connect_FTP_TLS(url, ports, login, password):
    ftps = FTP_TLS()
    ftps.connect(url, ports)
    ftps.login(login, password)
    ftps.encoding = 'UTF-8'
    return ftps


# Получаем список на сервере
def take_list_remote(ftp_status):
    return ftp_status.nlst()


# Получаем список на локальном компьютере
def take_list_local(path_url):
    return os.listdir(path_url)


# Превращаем список в множество
def list_to_set(lst):
    return set(lst)


# Получаем множество из разницы двух множеств
def set_difference(first_set, second_set):
    return first_set - second_set


# Условия множеств
def comparison_set(diff_set):
    if len(diff_set) > 0:
        return True
    else:
        return False


# Из множества в списки возвращаем
def set_to_list(st):
    return list(st)


# Удаление файла из директории
def remove_files(st, path_url):
    file_list = set_to_list(st)
    for filename in file_list:
        file_path = os.path.join(path_url, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


# Загрузка файла в директорию
def download_files(st, path_url):
    file_list = set_to_list(st)
    for filenames in file_list:
        # print(f'{int(count * 100 / len(filenames))}% из 100%')
        # count += 1
        host_file = os.path.join(
            path_url, filenames
        )

        try:
            with open(host_file, 'wb') as local_file:
                ftp.retrbinary('RETR ' + filenames, local_file.write)
        except ftplib.error_perm:
            pass


# Получение название файла
def name_file(name_komp, orientation):
    list_tv_file = 'resource/list_tv.xlsx'

    excel_data_df = pd.read_excel(list_tv_file)

    list_file = [excel_data_df['Имя компьютера'].tolist(),
                 excel_data_df['Название файла PLAYLIST'].tolist()]

    # Получаем название файла
    for k in range(len(list_file[0])):
        # print(k)
        if name_komp == list_file[0][k]:
            # print(excel_data_df['Название файла PLAYLIST'].isnull().tolist()[k])
            if excel_data_df['Название файла PLAYLIST'].isnull().tolist()[k]:
                playlist_name = 'PLAYLIST'
                break
            else:
                playlist_name = list_file[1][k]
                break

    name_playlist = playlist_name + '_' + orientation + '.m3u'
    # print(playlist_name)
    return name_playlist

# Получаем имя компьютера
hostname = socket.gethostname()
# hostname = 'hostname'

# Получаем номер магазина
number_shop = hostname[:4]
# print(hostname[:4])

# Получаем положение ТВ
orient = hostname[4]
# print(hostname[4])


print(name_file(number_shop, orient))


# Настройка доступа к FTP
ftp = connect_FTP_TLS(host, port, user, pwd)
print('1. Подключились к ФТП')

# Переход в директорию с кодом программы и его ресурсами
ftp.cwd('/Videoreklama')

# print(ftp.cwd('Videoreklama'))
print('2. Перешли в директорию на ФТП Видеореклама')

# Получение список файлов на удаленном сервере
list_remote_files = take_list_remote(ftp)
print('3. Получен список файлов на удаленном сервере')

# Превращаем список файлов удаленного сервера в множество
set_remote_files = list_to_set(list_remote_files)
print('4. Превратили список файлов удаленного во множества')

# Получаем список файлов на локальном устройстве
path = 'D:\\Test\\'
list_local_files = take_list_local(path)
print('5. Получен список файлов на локальном компьютере')

# Превращаем список локальных файлов в множество
set_local_files = list_to_set(list_local_files)
print('6. Превратили список файлов локального во множества')

# print(set_remote_files)
# print(set_local_files)
#
# print(set_local_files - set_remote_files)

# Получаем мн-во разницы (локальное - удаленное)
set_local_dif_remote = set_difference(set_local_files, set_remote_files)
print('7. Получили множество из разницы множеств (локальное - удалённое)')

# Удаление файлов на локальном компьютере
if comparison_set(set_local_dif_remote):
    print(set_local_dif_remote)
    remove_files(set_local_dif_remote, path)
    print('8. Так разница (локальное - удаленное) ИСТИНА\nУдалили файлы на локальном компьютере')
    new_list_local = take_list_local(path)
    print('9. Получили новый список локального компьютера')
    new_set_local_files = list_to_set(new_list_local)
    print('10. Превратили новый список локального компа во множество')
    set_remote_dif_local = set_difference(set_remote_files, set_local_files)
    print('11. Получили множество из разницы множеств (удаленное - локальное)')

# Получаем мн-во разницы (удаленное - локальное)
else:
    set_remote_dif_local = set_difference(set_remote_files, set_local_files)
    print('8. Так разница (локальное - удаленное) ЛОЖЬ\nПолучили множество из разницы множеств (удаленное - локальное)')

#Загрузка файлов на локальный компьютер
if comparison_set(set_remote_dif_local):
    download_files(set_remote_dif_local, path)
    print('9. Так разница (удаленное - локальное) ИСТИНА\nСкачиваем файлы на локальный компьютер')
    playlist = ['PLAYLIST1.m3u', 'PLAYLIST1R.m3u']
    download_files(playlist, path)
    print('10. Скачиваем файлы PLAYLIST1.m3u и PLAYLIST1R.m3u на локальный компьютер')

# Загружаем только PLAYLIST1 and PLAYLIST1R
else:
    print('9. Так разница (локальное - удаленное) ЛОЖЬ\nПолучили множество из разницы множеств (удаленное - локальное)')
    playlist = ['PLAYLIST1.m3u', 'PLAYLIST1R.m3u']
    download_files(playlist, path)
    print('10. Скачиваем файлы PLAYLIST1.m3u и PLAYLIST1R.m3u на локальный компьютер')


# Закрываем FTP соединение
ftp.quit()
