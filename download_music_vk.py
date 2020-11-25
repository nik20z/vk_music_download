import vk_api
import requests
import time
import os
from pprint import pprint
from threading import Thread
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from mutagen.easyid3 import EasyID3



# читаем файл и создаём словарь
def create_settings():
	settings = {}
	lines = open('settings.txt', encoding = 'utf8').readlines()
	for i in lines:
		words = i.split()
		if words[0] == 'path':
			settings[words[0]] = i[5:].replace('\\\\', '\\')
		else:
			settings[words[0]] = words[-1]
	return settings


# авторизация
def auth(token, group_id):
	print('Авторизация на сервере')
	vk = vk_api.VkApi(token = token)
	longpoll = VkBotLongPoll(vk, group_id)
	vk = vk.get_api()
	return vk, longpoll


# добавляем информацию об аудио в файл
def mutagen(path, title, artist, subtitle):	# tracknumber, 
	audio = EasyID3(path)
	audio['title'] = title
	audio['artist'] = artist

	#EasyID3.RegisterTextKey('comment', 'COMM')
	#audio['comment'] = subtitle
	#pprint(audio)

	audio.save()


# обрабатываем audio
class AUDIO(Thread):

	def __init__(self, audio):
		Thread.__init__(self)
		self.audio = audio
		self.t = time.time() 

	def run(self):
		subtitle = '' # подзаголовок, пояснение 
		title = self.audio['title'] # название 
		artist = self.audio['artist'] # исполнитель 
		url = self.audio['url'] # ссылка на скачивание 

		# создание подзаголовка / комментария
		if 'subtitle' in self.audio:
			subtitle = ' (' + self.audio['subtitle'] + ')'

		file_name = title + subtitle + ' — ' +  artist # название файла
		file_name = file_name.replace('"', '')
		path = settings['path'] # путь к папке
		full_file_name = file_name + settings['audio_format'] # название файла с расширением
		full_path = path + '\\' + full_file_name # полный путь к файлу

		if not os.path.exists(path): # если пути не существует
			os.makedirs(path) # создаём путь
		os.chdir(path) # переходим в текущую директорию	

		# если файла не существует
		if not os.path.exists(full_file_name):
			# сохраняем файл
			open(full_file_name, "wb").write(requests.get(url).content)

			# добавляем теги
			mutagen(full_path,
					title = title,
					artist = artist,
					subtitle = subtitle)

			print(str(round(time.time() - self.t, 2)) + ' с |', file_name) # название файла и время скачивания
		else:
			print(file_name, ' уже скачан')


# обрабатываем вложения
def get_attachments(attachments):
	for attachment in attachments: # перебираем массив вложений
		if attachment['type'] == 'audio': # если тип вложения - audio
			audio = attachment['audio'] # получаем информацию о вложении с типом audio
			#pprint(audio)
			AUDIO(audio).start() # создаём поток для скачивания файла
		else:
			print('вложение имеет тип, отличный от audio')
			print(attachment)


# обрабатываем event
def get_events(event):
	message = event.object.message # словарь с инфой о сообщении
	from_id = message['from_id'] # id пользователя, с которым идёт диалог
	peer_id = message['peer_id'] # id пользователя, который создал сообщение
	attachments = message['attachments'] # массив вложений
	if attachments != []: # если имеются вложения
		get_attachments(attachments) # обрабатываем вложения
	else:
		print('сообщение не содержит вложений')



# авторизация вк
settings = create_settings()
vk, longpoll = auth(settings['token'], settings['group_id'])

# основной цикл, получающий события от сервера вк
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW: # если событие - новое сообщение
    	get_events(event) # обрабатываем event - json с информацией о пользователе и сообщении, которое он отправил