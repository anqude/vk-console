#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk_api # ~ библиотека вк
import os # ~ для отчистки экрана
import time # ~ для задержки
import datetime # ~ для времени отправки сообщения
def autorization(personal_token):
	vk_session = vk_api.VkApi(token=personal_token) # ~ логинимся по токину
	global vk # ~ объявляем vk как глобальную пременную ибо ссылаемся на ней потом
	vk = vk_session.get_api()

def users_ids():
	print("1-Дима,2-Миша, 3-Балтика(группы не робят), other") # ~ предлагаем варианты или считываем кастомный вариант
	global personal_id # ~ объявляем personal_id как глобальную пременную
	personal_id=str(input("personal id of recipient>>")) # ~ вводим id получателя или номер ;)
	if personal_id=="1"or personal_id=="Дима":
		personal_id="630848795"
	if personal_id=="2"or personal_id=="Миша":
		personal_id="385594215"
	if personal_id=="3"or personal_id=="Балтика":
		personal_id="2000000053"

def message_get():
	global t
	t = vk.messages.getHistory(count = 20, peer_id = int(personal_id), rev=0) # переменная содержащая историю диалога

def message_view():
	for i in range(len(t.get("items"))-1,-1,-1):
		dateun = t.get("items")[i].get("date") # получение даты и времени в unix-time
		date = datetime.datetime.fromtimestamp(dateun) # перевод даты в нормальный вид
		text=str(us_ids().get(t.get("items")[i].get("from_id"))) +" "+date.strftime('%Y-%m-%d %H:%M:%S')+": "+t.get("items")[i].get("text")
		print(text)
		global message_id
		message_id = str(t.get("items")[i].get("id"))
		print("message id:",message_id)

		
def message_input():
	print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") # ~ просто рисуем строку
	global message_text
	message_text= str(input("Сообщение (для отмены - 'неа!!!') >>")) # ~ Считываем текст сообщения
	time.sleep(0.5)
	while True:
		if message_text=="": # ~ Если сообщение пустое, считываем текст его снова
			print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░") # ~ просто рисуем строку
			message_text= str(input("Сообщение (для отмены - 'неа!!!') >>")) # ~ считываем сообщение
		else:
				break

	
	
def message_send(personal_id):
	print("The message has been sent") # ~ просто,факт что отправили
	time.sleep(0.5)
	os.system('clear') # ~ просто отчищаем экран
	vk.messages.send(peer_id = personal_id, message = message_text, random_id =0) # ~ пишем сообщение юзеру с personal_id которы обявляли в def users_ids()

def null_message():
	if message_text!="неа!!!":
		message_send(personal_id)	
	else:
		print("Ну ок ничего значит")
	
		

def del_message(agree,message_id):
	if agree=='y':
		vk.messages.delete(delete_for_all=True, message_ids=message_id)
	if agree=='custom':
		message_id=input("custom message id:")
		vk.messages.delete(delete_for_all=True, message_ids=message_id)
	time.sleep(0.5)
	os.system('clear') # ~ просто отчищаем экран	

def us_ids():
	members = vk.messages.getConversationMembers(peer_id = personal_id)
	for i in range(members.get("count")):
		name = str(members.get("profiles")[i].get("first_name"))+" "+str(members.get("profiles")[i].get("last_name"))
		id_mem = members.get("profiles")[i].get("id")
		ids.update({id_mem: name}) # занесение в словарь id и имени
	return ids

def list_id(): # ~ получение собственного id и создание словаря с id
	global ids
	ids = {} # словарь со всеми id
	my_id = vk.account.getProfileInfo().get("id") # собственный id
	my_name = str(vk.account.getProfileInfo().get("first_name")+" "+str(vk.account.getProfileInfo().get("last_name"))) # получение своего имени
	ids.update({my_id: my_name}) # изменение словаря	
	




autorization(str(input("personal vk token >>"))) # ~ вводим токен

while True:
	list_id()
	users_ids()
	message_get()
	message_view()
	message_input()
	null_message()
	del_message(str(input("Want to delete last message ('y','n' or 'custom') >>")),message_id)
	

