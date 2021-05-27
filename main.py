import socket
import threading
import DBFunctions as dbf
import messageFunctions as msf
import time
import struct


MAXCONNECTIONS = 1000
users = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('192.168.0.103', 3001))

sock.listen(MAXCONNECTIONS)


class MessageHandler(threading.Thread):
    def run(self):
        while True:
            print('------conn------')
            print(self.conn)
            print('--------end conn-------')
            data = self.conn.recv(8192)#.decode('utf16').replace('\0', '')
            message = bytearray(8192)
            command = data[0]
            subcommand1 = data[1]
            subcommand2 = data[2]

            if command == 1:            #Авторизация и регистрация

                if subcommand1 == 1:        #Для авторизации,
                    if subcommand2 == 1:
                        #При авторизации получаем логин и пароль
                        name = data[32:96].decode('utf16').replace('\ucccc', '')
                        password = data[96:160].decode('utf16').replace('\ucccc', '')
                        # Код получения инфы о юзере
                        id = dbf.GetUserId(name, password)
                        if id > 0:
                            self.id = id
                            message[0] = 110
                            message[1] = 1
                        else:
                            message[0] = 110
                            message[1] = 2
                        self.conn.send(message)

                    elif subcommand2 == 2:
                        #При открытии приложения отправляем клиенту инфу о нем
                        userInfo = dbf.GetUserInfoById(self.id)
                        msf.SendMyselfData(self.conn, userInfo)
                        #Инфу о тех, с кем он общался и их чатами
                        usrs = dbf.GetUsersById(self.id)
                        if usrs != -1:
                            for user in usrs:
                                if user[1] == self.id:
                                    msf.SendChatsAndUsersData(self.conn, dbf.GetUserInfoById(user[2]), user[0])
                                else:
                                    msf.SendChatsAndUsersData(self.conn, dbf.GetUserInfoById(user[1]), user[0])
                        time.sleep(2)
                        #Его сообщения
                        messages = dbf.GetMessagesByUserId(self.id)
                        if messages != -1:
                            for mess in messages:
                                msf.SendMessageData(self.conn, mess)

                elif subcommand1 == 2:  #Регистрация
                    if subcommand2 == 1:
                        #При регистрации отправляем результат успешно или нет регистрация
                        fName = data[32:64].decode('utf16').replace('\ucccc', '')
                        lName = data[64:96].decode('utf16').replace('\ucccc', '')
                        pName = data[96:128].decode('utf16').replace('\ucccc', '')
                        email = data[128:160].decode(errors='ignore').replace("\x00", "\uFFFD")
                        phone = data[160:171].decode(errors='ignore').replace("\x00", "\uFFFD")
                        login = data[171:235].decode('utf16').replace('\ucccc', '')
                        password = data[235:299].decode('utf16').replace('\ucccc', '')
                        year = data[299]*100 + data[300]
                        month = data[301]
                        day = data[302]
                        print(login)
                        if (dbf.CheckLogin(login)):
                            message[0] = 111
                            message[1] = 2
                        elif (dbf.CheckPhone(phone)):
                            message[0] = 111
                            message[1] = 3
                        else:
                            dbf.AddNewUser(fName, lName, pName, email, phone, login, password, year, month, day)
                            message[0] = 111
                            message[1] = 1
                        self.conn.send(message)


            elif command == 2:  #Работа с сообщениями
                if subcommand1 == 1:
                    if subcommand2 == 1:    #Отправка нового сообщения

                        ownerId = struct.unpack("q", data[6:14])[0]
                        #ownerId = self.id
                        recipientId = struct.unpack("q", data[14:22])[0]
                        chatId = struct.unpack("q", data[22:30])[0]
                        text = data[32:8192].decode('utf16').replace('\ucccc', '')
                        print(ownerId, recipientId, chatId, text)
                        (messId, datetime) = dbf.AddNewMessage(ownerId, recipientId, chatId, text)


                        for user in users:
                            if not user.is_alive():
                                users.remove(user)
                                continue
                            if user.id == recipientId or user.id == self.id:
                                msf.SendMessageData(user.conn, (messId, ownerId, recipientId, chatId, text, datetime))



            elif command == 3:      #Работа с чатами
                if subcommand1 == 1:    #Создание чата с пользователем
                    phone = data[32:43].decode(errors='ignore').replace("\x00", "\uFFFD")
                    repr(phone)

                    if (dbf.CheckPhone(phone)):
                        userId = dbf.GetUserIdByPhone(phone)[0]
                        if (dbf.CheckChat(self.id, userId)):
                            message[0] = 112
                            message[1] = 3  #Ошибка чат уже присутствует
                        else:
                            chatId = dbf.AddNewChat(self.id, userId)[0]
                            print(chatId)
                            for user in users:
                                if not user.is_alive():
                                    users.remove(user)
                                    continue
                                if user.id == userId:
                                    msf.SendChatsAndUsersData(user.conn, dbf.GetUserInfoById(self.id), chatId)
                                elif user.id == self.id:
                                    msf.SendChatsAndUsersData(user.conn, dbf.GetUserInfoById(userId), chatId)


                            message[0] = 112
                            message[1] = 1  #Сейчас скинется новый чат!

                    else:
                        message[0] = 112
                        message[1] = 2  #Ошибка отсутствует телефон
                    self.conn.send(message)






    @staticmethod
    def sendAll(text):
        print(text)
        for user in users:
            if not user[1].is_alive():
                users.remove(user)
                continue
            user[0].send(text.encode('utf16'))


while True:
    conn, addr = sock.accept()

    print('new accept')
    a = MessageHandler()
    a.conn = conn
    a.id = -1
    a.start()
    users.append(a)




#
#
# import socket
# import threading
#
# MAXCONNECTIONS = 1000
# users = []
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# sock.bind(('127.0.0.1', 3001))
#
# sock.listen(MAXCONNECTIONS)
#
#
# class MessageHandler(threading.Thread):
#     def run(self):
#         while True:
#             data = self.conn.recv(256).decode('utf16').replace('\0', '')
#             self.sendAll(str('\r\n\r\n' + self.name + ': ' + data))
#
#     @staticmethod
#     def sendAll(text):
#         print(text)
#         for user in users:
#             if not user[2].is_alive():
#                 users.remove(user)
#                 continue
#             user[0].send(text.encode('utf16'))
#
#
# while True:
#     conn, addr = sock.accept()
#     name = conn.recv(256).decode('utf16').replace('\0', '')
#     print('New user: ', name)
#     a = MessageHandler()
#     a.name = name
#     a.conn = conn
#     a.start()
#     users.append((conn, name, a))
#     # conn.send(bytes(str('Пользователь' + name + ' присоединился к чату').encode('utf16')))
#     a.sendAll(f'\r\n\r\nПользователь {name} присоединился к чату')
#
# conn.close()