from urllib.request import Request, urlopen, urlretrieve
import os
import zipfile


class Updater:
    def __init__(self, repository, current_version: float, target_path: str, tag:str,
                 updaterinfo_filename: str = "updater.txt", stable: bool = True):
        self.cfg = None
        self.updater_info_path = None
        self.repository = repository
        self.current_version = current_version
        self.target_path = target_path
        self.last_version = None
        self.tag = tag
        self.updater_path = "./ppupdater.py"
        self.only_stable = stable
        self.updaterinfo_filename = updaterinfo_filename
        self.cache_folder = 'updatecache'

    def check_update(self):
        # Update config (changes, archive name, etc...)
        updater_info_download_path = self.repository + f"/releases/download/{self.tag}/{self.updaterinfo_filename}"
        self.updater_info_path = "updater.txt"

        # Скачивание файла с информацией о версии
        urlretrieve(updater_info_download_path, self.updater_info_path)

        # Парсинг файла с информацией о версии
        cfg_reader = ConfigReader(config_path=self.updater_info_path)
        self.cfg = cfg_reader.read()

        # Получение информации о версии
        self.last_version = float(self.cfg['version'])

        if self.last_version > self.current_version:
            return True
        else:
            return False

    def update(self):
        self.check_update()

        released_app_path = self.repository + f"/releases/download/{self.tag}/{self.cfg['archive_name']}"

        cache_path = self.cache_folder + '/' + self.cfg['archive_name']

        # Загрузка
        try: os.mkdir(self.cache_folder)
        except: pass
        urlretrieve(released_app_path, cache_path)

        # Распаковка
        with zipfile.ZipFile(cache_path, 'r') as zip:
            zip.extractall(self.target_path)

        # Удаление кэша
        os.remove(cache_path)
        os.rmdir(self.cache_folder)
        os.remove(self.updater_info_path)

        return self.last_version



# Чтение конфигов
class ConfigReader:
    def __init__(self, config_path: str, delimiter: str = ":"):
        self.config_path = config_path
        self.delimiter = delimiter

    # Return dictionary
    def read(self):
        cfg = open(self.config_path, 'r')
        data = cfg.read()
        cfg.close()

        params = {}

        # Список строк
        strings = data.split("\n")
        for string in strings:
            param = string.split(self.delimiter)
            params[param[0]] = param[1]

        return params

