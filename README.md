# vk_music_download
# python-3.8.5

Бот предназначен для скачивания музыки из Вконтакте.

Используемые библиотеки и модули:

    import vk_api
    import requests
    import time
    import os
    from pprint import pprint
    from threading import Thread
    from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
    from mutagen.easyid3 import EasyID3


Настройка:
Создать сообщество. Получить token и id группы.
Внести изменения в файл settings.txt, заменив предложенные значения на свои: 

    token, 
    group_id; 
    audio_format - формат, в котором необходимо сохранить аудио; 
    path - абсолютный путь к папке для сохранения
