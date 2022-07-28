#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import sys
import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
from datetime import *  # ~ для времени отправки сообщения
import json

start_time = datetime.now()  # ~ обозначаем время запуска


class Logics:

    def LPauth(self, login, password):
        vk_session = vk_api.VkApi(login,password)
        vk_session.auth()
        vk = vk_session.get_api()

        return vk

    def Tauth(self, personal_token):
        # ~ логинимся по токену
        vk_session = vk_api.VkApi(token=personal_token)
        vk = vk_session.get_api()
        return vk


    def message_send(self, personal_id, message_text):
        session.messages.send(peer_id=personal_id,
                              message=message_text, random_id=0)
        return 0


    # (all id first_name last_name full_name) есть возможность указать несколько аргументов
    def get_info_about_me(self):

        p_info = session.account.getProfileInfo()
        my_id = p_info["id"]
        f_n = p_info["first_name"]
        l_n = p_info["last_name"]
        all = {"id": my_id, "name": f_n + " " + l_n}
        return all


    # ~ история сообщений для указанного диалога
    def get_history(self, personal_id, count_=200):
        messages = {}
        MessageHistory = session.messages.getHistory(
            count=count_, peer_id=personal_id, rev=0)
        for i in reversed(MessageHistory["items"]):
            print(i["from_id"])
            print(i["text"])
            print(i)
        return MessageHistory


    def del_message(self, message_id, agree="n"):  # ~ Удаление сообщения

        if agree == 'y':
                # ~ Удалить последнее сообщение
            session.messages.delete(
                delete_for_all=True, message_ids=message_id)

        if agree == 'custom':  # ~ Удалить выбранное по id сообщение
            message_id = input("custom message id:")
            session.messages.delete(
                delete_for_all=True, message_ids=message_id)
        message = session.message.getById(message_ids=message_id)
        return message


    def us_ids(self, personal_id, session):

        members = session.messages.getConversationMembers(
            peer_id=personal_id)
        print(members.get("items"))


    def save_peoples(self, personal_ids, json):

        peoples = json.jtpy("peoples.json")
        ids = []
        for i in peoples:
            ids.append(i.get("id"))
        for i in personal_ids:
            if (i in ids) == False:
                ids.append(i)
        pyj = session.users.get(user_ids=ids)
        json.pytj(pyj, "peoples.json")
        return pyj

    def get_dialogs(self, number):

        dialogs_obj = session.messages.getConversations(
            count=number, extended=1)

        profiles = {}
        chats = {"ids":[], "name": []}
        dialogs = {"count": session.messages.getConversations(
            count=number, extended=1)["count"], "ids": [],"names": []}

        for i in dialogs_obj["items"]:
            dialogs_id = i["conversation"]["peer"]["id"]

            if i["conversation"]["peer"]["type"] == "chat":
                chat_name = i["conversation"]["chat_settings"]["title"]
                chats["ids"].append(dialogs_id)
                chats["name"].append(chat_name)


            elif i["conversation"]["peer"]["type"] == "user":
                dialogs["ids"].append(dialogs_id)

        for i in dialogs_obj["profiles"]:
            profiles.update({ str(i["id"]): i["first_name"]+ " " +i["last_name"]})

        for i in dialogs["ids"]:
            for j in list(profiles):
                if i == int(j):
                    dialogs["names"].append(profiles[j])


        for i in chats["ids"]:
            dialogs["ids"].append(i)
        for i in chats["name"]:
            dialogs["names"].append(i)

        return dialogs

    def get_friends(self, us_id, number):

        friends = {"ids": [], "names": []}
        j = session.friends.get(
            user_id=us_id, order="random", count=number, fields='nickname')

        for i in range(number):
            name = j["items"][i]["first_name"] + " " + j["items"][i]["last_name"]
            id = j["items"][i]["id"]
            friends["ids"].append(id)
            friends["names"].append(name)

        return friends


    def get_chat_members(self, dialog_id):
        chat_members = {"ids":[], "names":[]}
        members = session.messages.getChat(
            chat_id=dialog_id, fields='nickname')
        kolvo = int(members["members_count"])
        for i in range(kolvo):
            first_name = str(members["users"][i]["first_name"])
            last_name = str(members["users"][i]["last_name"])
            id = str(members["users"][i]["id"])
            chat_members["ids"].append(id)
            chat_members["names"].append(first_name + " " + last_name)

        return chat_members


class js(object):
    def pytj(self, PyObject, file_name):
        try:
            j = json.dumps(PyObject, indent=4)
            f = open(file_name, "w")
            f.write(j)
            return PyObject
        except:
            print("PYTJ ERROR")

    def jtpy(self, JsFileName):
        try:
            f = open(JsFileName, "r")
            py = json.load(f)
            return py
        except:
            py = []
            print("JTPY ERROR")
            return py


def main():
    obj = Logics()
    global session

    session = obj.Tauth(TOKEN)
    j = js()
    print(obj.get_history(personal_id=405276453))




settings_open = open("settings.json", "r")
py = json.load(settings_open)
if py["Token"] == "":
    global TOKEN
    TOKEN = input("введите свой токен: ")
    pyj = {"Token": TOKEN}
    j = json.dumps(pyj, indent=4)
    settings_open = open("settings.json", "w")
    settings_open.write(j)

else:
    TOKEN = py["Token"]
main()

print(datetime.now() - start_time)  # время от запуска кода до его завершения
