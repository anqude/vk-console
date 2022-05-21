#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textwrap import indent
import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
import datetime  # ~ для времени отправки сообщения
import os  # ~ для работы с консолью
import json

class Logics(object):

    def auth(self, personal_token):
        try:
            vk_session = vk_api.VkApi(token=personal_token)  # ~ логинимся по токену
            vk = vk_session.get_api()
            return vk
        except:
            print("Auth ERROR")

    def message_send(self, personal_id, message_text, session):
        try:
            session.messages.send(peer_id=personal_id, message=message_text, random_id=0)
            return 0
        except:
            print("Message send ERROR")

    def get_info_about_me(self, session, arg): #(all id first_name last_name full_name) есть возможность указать несколько аргументов
        try:
            my_id = session.account.getProfileInfo().get("id")
            f_n = str(session.account.getProfileInfo().get("first_name"))
            l_n =  str(session.account.getProfileInfo().get("last_name"))
            first_name = {"first_name": f_n}
            last_name = {"last_name": l_n}
            fullname = {"first_name":f_n, "last_name": l_n}
            all = {"id":my_id, "first_name":f_n, "last_name": l_n}
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
        
    def history_get(self, personal_id, session, count_=200):
        try:
            t = session.messages.getHistory(count=count_, peer_id=personal_id, rev=0)
            return t
        except:
            print("History get ERROR")


    def del_message(self, message_id, session, agree="n"):
        try:
            if agree == 'y':
                session.messages.delete(delete_for_all=True, message_ids=message_id)
            
            if agree == 'custom':
                message_id = input("custom message id:")
                session.messages.delete(delete_for_all=True, message_ids=message_id)
            message = session.message.getById(message_ids=message_id)
            return message
        except:
            print("Del message ERROR")

    
    def us_ids(self, personal_id, my_id, ids, session):
        try:
            members = session.messages.getConversationMembers(peer_id=personal_id)
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
        except:
            print("User ids ERROR")

    def save_peoples(self, personal_ids, session):
        j = js()
        ps = session.users.get(user_ids = personal_ids)
        peoples = j.jtpy("peoples.json")
        ids = []
        for i in peoples:
            ids.append(str(i.get("id")))
        ids.append(personal_ids)
        pyj = session.users.get(user_ids = ids)
        j.pytj(pyj,"peoples.json")


class Console(object):
    def view(self, title, text, input_text):
        try:
            os.system("cls")
            print(title,"\n\n")
            print(text)
            a = input(input_text)
            return a
        except:
            print("Console ERROR")


class js(object):
    def pytj(self, PyObject, file_name):
        try:
            j = json.dumps(PyObject, indent=4)
            f = open(file_name,"w")
            f.write(j)
            return 0
        except:
            print("PYTJ ERROR")
    
    def jtpy(self, JsFileName):
        try:
            f = open(JsFileName,"r")
            py = json.load(f)
            return py
        except:
            print("JTPY ERROR")
        


def main():
    obj = Logics()
    sess = obj.auth(input("введите персональный токен(https://vkhost.github.io/): "))
    j = js()
    
main()
