#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
import datetime  # ~ для времени отправки сообщения


def autorization(personal_token):
    vk_session = vk_api.VkApi(token=personal_token)  # ~ логинимся по токину
    global vk  # ~ объявляем vk как глобальную пременную ибо ссылаемся на ней потом
    vk = vk_session.get_api()


def message_input():
    # ~ просто рисуем строку
    print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    global message_text
    # ~ Считываем текст сообщения
    message_text = str(input("Сообщение (exit чтобы выйти) >> "))
    while True:
        if message_text == "":  # ~ Если сообщение пустое, считываем текст его снова
            # ~ просто рисуем строку
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            message_text = str(input("Сообщение >>"))  # ~ считываем сообщение
        elif message_text == "exit":
            users_ids()
        else:
            break


def message_send(personal_id):
    # ~ пишем сообщение юзеру с personal_id которы обявляли в def users_ids()
    print("The message has been sent") # ~ просто,факт что отправили
	time.sleep(0.5)
	os.system('clear') # ~ просто отчищаем экран
    vk.messages.send(peer_id=personal_id, message=message_text, random_id=0)
    


def users_ids():
    conversations = {}
    percent = 0
    for i in range(len(vk.messages.getConversations().get("items"))):
        type = vk.messages.getConversations().get("items")[i].get(
            "conversation").get("peer").get("type")
        if type == "chat":
            chat_name = vk.messages.getConversations().get("items")[i].get(
                "conversation").get("chat_settings").get("title")
            chat_id = vk.messages.getConversations().get(
                "items")[i].get("conversation").get("peer").get("id")
            conversations.update({chat_name: chat_id})
        elif type == "group":
            continue
        else:
            user_chat_id = vk.messages.getConversations().get(
                "items")[i].get("conversation").get("peer").get("id")
            username = vk.users.get(user_ids=user_chat_id)[0].get(
                "first_name") + " "+vk.users.get(user_ids=user_chat_id)[0].get("last_name")
            conversations.update({username: user_chat_id})
    print("Диалоги:\n \n")
    for i in conversations:
        print(i)
    global personal_id  # ~ объявляем personal_id как глобальную пременную
    personal_id = str(conversations.get(input("personal name of recipient>>")))


def message_get():
    global t
    # переменная содержащая историю диалога
    t = vk.messages.getHistory(count=20, peer_id=personal_id, rev=0)


def message_view():
    for i in range(len(t.get("items"))-1, -1, -1):
        # получение даты и времени в unix-time
        dateun = t.get("items")[i].get("date")
        date = datetime.datetime.fromtimestamp(
            dateun)  # перевод даты в нормальный вид
        text = str(us_ids().get(t.get("items")[i].get("from_id"))) + " "+date.strftime(
            '%Y-%m-%d %H:%M:%S')+": "+t.get("items")[i].get("text")
        print(text)
        global message_id
		message_id = str(t.get("items")[i].get("id"))
		print("message id:",message_id)


def us_ids():
    members = vk.messages.getConversationMembers(peer_id=personal_id)
    if personal_id != str(my_id):
        for i in range(members.get("count")):
            name = str(members.get("profiles")[i].get(
                "first_name"))+" "+str(members.get("profiles")[i].get("last_name"))
            id_mem = members.get("profiles")[i].get("id")
            ids.update({id_mem: name})  # занесение в словарь id и имени
    else:
        for i in range(members.get("count")-1):
            name = str(members.get("profiles")[i].get(
                "first_name"))+" "+str(members.get("profiles")[i].get("last_name"))
            id_mem = members.get("profiles")[i].get("id")
            ids.update({id_mem: name})  # занесение в словарь id и имени
    return ids


def list_id():  # ~ получение собственного id и создание словаря с id
    global ids
    ids = {}  # словарь со всеми id
    global my_id
    my_id = vk.account.getProfileInfo().get("id")  # собственный id
    my_name = str(vk.account.getProfileInfo().get("first_name")+" " +
                  str(vk.account.getProfileInfo().get("last_name")))  # получение своего имени
    ids.update({my_id: my_name})  # изменение словаря

def del_message(agree,message_id):
	if agree=='y':
		vk.messages.delete(delete_for_all=True, message_ids=message_id)
	if agree=='custom':
		message_id=input("custom message id:")
		vk.messages.delete(delete_for_all=True, message_ids=message_id)
	time.sleep(0.5)
	os.system('clear') # ~ просто отчищаем экран	
    
autorization(str(input("personal vk token >>")))  # ~ вводим токен


while True:
    list_id()
    users_ids()
    message_get()
    message_view()
    message_input()
    message_send(personal_id)
    del_message(str(input("Want to delete last message ('y','n' or 'custom') >>")),message_id)
