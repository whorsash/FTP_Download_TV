import ftplib
import os

from ftplib import FTP_TLS

from config import host, port, user, pwd


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


# Настройка доступа к FTP
ftp = connect_FTP_TLS(host, port, user, pwd)
print('1. Подключились к ФТП')

# Переход в директорию с кодом программы и его ресурсами
ftp.cwd('/FTP_Programming')
print('2. Перешли в директорию на /FTP_Programming')

# Получаем список файлов из удаленной директории FTP_Programming
list_remote_files = take_list_remote(ftp)
print('3. Получили список файлов программирования FTP_Programming')

# Указываем путь для технических программ на локальном устройстве
path = 'D:\\Test\\Programming\\'
#path_linux = '/home/fissman/Programming'
print('4. Указали путь к папке Programming на локальном компьютере')

# Скачиваем технические файлы (list_tv.xlsx и TV_FTP.py)
resource_list = ['list_tv.xlsx', 'TV_FTP.py']
print('5. Скачиваем файлы list_tv.xlsx и TV_FTP.py')
download_files(resource_list, path)
print('6. Скачали файл')

print('Закрываем соединение')
# Закрываем FTP соединение
ftp.quit()

os.system('python TV_FTP.py')
