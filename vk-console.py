#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import *
import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
from datetime import *  # ~ для времени отправки сообщения
import json
start_time = datetime.now()
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

    
    def us_ids(self, personal_id, session):
        try:
            members = session.messages.getConversationMembers(peer_id=personal_id)
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
            pyj = session.users.get(user_ids = ids)
            json.pytj(pyj,"peoples.json")
            return pyj
        except:
            print("Save peoples ERROR")

    def get_dialogs_info(self,session,number):
        conversations = session.messages.getConversations(count=number,extended=1)
        conversations_info = {}
        
        """for i in range(len(conversations)):
            name = conversations["profiles"][i]["first_name"]+" "+conversations["profiles"][i]["last_name"]
            id = conversations["items"][i]["conversation"]["peer"]["id"]
            print(i,name,id)
            conversations_info.update({id: name})"""
        return conversations


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
            py = []
            print("JTPY ERROR")
            return py
        

def main():
    obj = Logics()
    sess = obj.auth(Token)
    j = js()
    print(obj.get_dialogs_info(sess,1))
    
    
    

main()
print(datetime.now() - start_time)

