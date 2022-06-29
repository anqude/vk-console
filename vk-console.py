#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# anton sosi

import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
from datetime import *  # ~ для времени отправки сообщения
import json

start_time = datetime.now()  # ~ обозначаем время запуска


class Logics:

    def auth(self, personal_token):
        try:
            # ~ логинимся по токену
            vk_session = vk_api.VkApi(token=personal_token)
            vk = vk_session.get_api()
            return vk
        except:
            print("Auth ERROR")

    def message_send(self, personal_id, message_text, session):
        try:
            session.messages.send(peer_id=personal_id,
                                  message=message_text, random_id=0)
            return 0
        except:
            print("Message send ERROR")

    # (all id first_name last_name full_name) есть возможность указать несколько аргументов
    def get_info_about_me(self, session, arg):
        try:
            my_id = session.account.getProfileInfo().get("id")
            f_n = str(session.account.getProfileInfo().get("first_name"))
            l_n = str(session.account.getProfileInfo().get("last_name"))
            first_name = {"first_name": f_n}
            last_name = {"last_name": l_n}
            fullname = {"first_name": f_n, "last_name": l_n}
            all = {"id": my_id, "first_name": f_n, "last_name": l_n}
            if arg == "all":
                return all
            if arg == "id":
                return my_id
            if arg == "first_name":
                return first_name
            if arg == "last_name":
                return last_name
            if arg == "full_name":
                return fullname
        except:
            print("Get info about me ERROR")

    # ~ история сообщений для указанного диалога
    def history_get(self, personal_id, session, count_=200):
        try:
            MessageHistory = session.messages.getHistory(
                count=count_, peer_id=personal_id, rev=0)
            return MessageHistory
        except:
            print("History get ERROR")

    def del_message(self, message_id, session, agree="n"):  # ~ Удаление сообщения
        try:
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
        except:
            print("Del message ERROR")

    def us_ids(self, personal_id, session):
        try:
            members = session.messages.getConversationMembers(
                peer_id=personal_id)
            print(members.get("items"))
        except:
            print("User ids ERROR")

    def save_peoples(self, personal_ids, session, json):
        try:
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
        except:
            print("Save peoples ERROR")

    def get_dialogs(self, session, number):
        dialogs_obj = session.messages.getConversations(
            count=number, extended=1)
        dialogs = {"count": dialogs_obj["count"], "ids": []}

        for i in range(number):
            dialogs_ids = dialogs_obj["items"][i]["conversation"]["peer"]["id"]
            dialogs["ids"].append(dialogs_ids)
        return dialogs

    def get_friends(self, us_id, number, session):
        try:
            friends = {}
            j = session.friends.get(
                user_id=us_id, order="random", count=number, fields='nickname')

            for i in range(number):
                first_name = j["items"][i]["first_name"]
                last_name = j["items"][i]["last_name"]
                id = j["items"][i]["id"]
                friends.update({id: first_name + " " + last_name})

            return friends
        except:
            return "Get Friends ERROR"

    def get_chat_members(self, session, dialog_id):
        try:
            chat_members = []
            members = session.messages.getChat(
                chat_id=dialog_id, fields='nickname')
            kolvo = int(members["members_count"])
            for i in range(kolvo):
                first_name = str(members["users"][i]["first_name"])
                last_name = str(members["users"][i]["last_name"])
                id = str(members["users"][i]["id"])
                chat_members.append(
                    {"id": id, "first_name": first_name, "last_name": last_name})

            return chat_members

        except:
            return "Get Vhat Members ERROR"


class js(object):
    def pytj(self, PyObject, file_name):
        try:
            j = json.dumps(PyObject, indent=4)
            f = open(file_name, "w")
            f.write(j)
            return 0
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
    sess = obj.auth(TOKEN)
    j = js()
    print(obj.get_chat_members(sess, "14", "22"))


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
