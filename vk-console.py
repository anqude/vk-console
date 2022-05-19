#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk_api  # ~ библиотека вк
import os  # ~ для отчистки экрана
import time  # ~ для задержки
import datetime  # ~ для времени отправки сообщения
import os  # ~ для работы с консолью

class Logics(object):

    def auth(self, personal_token):
        try:
            vk_session = vk_api.VkApi(token=personal_token)  # ~ логинимся по токену
            vk = vk_session.get_api()
            return vk
        except:
            return 1

    def message_send(self, personal_id, message_text, session):
        try:
            session.messages.send(peer_id=personal_id, message=message_text, random_id=0)
            return personal_id, message_text
        except:
            return 2

    def get_info_about_me(self, session, arg): #(all id first_name last_name full_name) есть возможность указать несколько аргументов
        try:
            my_id = session.account.getProfileInfo().get("id")
            first_name = str(session.account.getProfileInfo().get("first_name"))
            last_name =  str(session.account.getProfileInfo().get("last_name"))
            fullname = first_name + " " + last_name
            all = {"id":my_id, "first_name":first_name, "last_name": last_name}
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
            return 3
        
    def message_get(personal_id, count_, session):
        try:
            t = session.messages.getHistory(count=count_, peer_id=personal_id, rev=0)
            return t
        except:
            return 4

    def message_view(t,us_ids , arg=""):
        try:
            for i in range(len(t.get("items"))-1, -1, -1):
                # получение даты и времени в unix-time
                dateun = t.get("items")[i].get("date")
                date = datetime.datetime.fromtimestamp(
                    dateun)  # перевод даты в нормальный вид
                text = str(us_ids().get(t.get("items")[i].get("from_id"))) + " "+date.strftime(
                    '%Y-%m-%d %H:%M:%S')+": "+t.get("items")[i].get("text")
                message_id = str(t.get("items")[i].get("id"))
                result_all = text, message_id
                if arg == "all":
                    return result_all
                else:
                    return text
                
        except:
            return 5
            


class Console(object):
    def view(title, text, input_text):
        try:
            os.system("cls")
            print(title,"\n\n")
            print(text)
            a = input(input_text)
            return a
        except:
            return 101



def main():
    obj = Logics()
    sess = obj.auth(input("введите персональный токен(https://vkhost.github.io/): "))
    console = Console()
    

main()
