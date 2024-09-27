import json

from nandboxbots.data.Chat import Chat
from nandboxbots.data.SignupUser import SignupUser


class WhiteList:
    __KEY_WHITELIST = "whitelist"
    __KEY_EOP = "eop"
    __KEY_USERS = "users"
    __KEY_CHAT = "chat"

    eop = None
    chat = None
    users = []

    def __init__(self, dictionary):
        whitelist_dict = dictionary[self.__KEY_WHITELIST] if self.__KEY_WHITELIST in dictionary.keys() else {}

        self.eop = str(whitelist_dict[self.__KEY_EOP]) if self.__KEY_EOP in whitelist_dict.keys() else None
        self.chat = Chat(whitelist_dict.get(self.__KEY_CHAT, {}))

        users_arr_obj = whitelist_dict[self.__KEY_USERS] if self.__KEY_USERS in whitelist_dict.keys() else []
        self.users = [SignupUser({})] * len(users_arr_obj)
        for i in range(len(users_arr_obj)):
            self.users[i] = SignupUser(users_arr_obj[i])

    def to_json_obj(self):

        dictionary = {}

        if self.users is not None:
            users_arr = []
            for i in range(len(self.users)):
                users_arr.append(self.users[i].to_json_obj())

            dictionary[self.__KEY_USERS] = users_arr

        if self.chat is not None:
            _, chat_dict = self.chat.to_json_obj()
            dictionary[self.__KEY_CHAT] = chat_dict

        if self.eop is not None:
            dictionary[self.__KEY_EOP] = self.eop

        return json.dumps(dictionary), dictionary
