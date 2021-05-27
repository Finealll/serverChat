import struct

#Создает и отправляет сообщение о себе
def SendMyselfData(conn, data):
    id = struct.pack("q", data[0])
    fName = data[1].encode('utf16')
    lName = data[2].encode('utf16')
    msg = bytearray(104)
    #Задаем начальные параметры
    msg[0] = 1
    msg[1] = 1
    msg[2] = 2
    #Копируем id
    count = 32
    for i in id:
        msg[count] = i
        count += 1
    #Копируем имя
    count = 40
    for i in fName:
        msg[count] = i
        count += 1
    #Копируем фаилию
    count = 72
    for i in lName:
        msg[count] = i
        count += 1
    #Отправляем клиенту
    conn.send(msg)

# Создает сообщение о знакомом юзере
def SendAboutUserData(conn, data):
    id = struct.pack("q", data[0])
    fName = data[1].encode('utf16')
    lName = data[2].encode('utf16')
    msg = bytearray(104)
    # Задаем начальные параметры
    msg[0] = 1
    msg[1] = 1
    msg[2] = 1
    # Копируем id
    count = 32
    for i in id:
        msg[count] = i
        count += 1
    # Копируем имя
    count = 40
    for i in fName:
        msg[count] = i
        count += 1
    # Копируем фамилию
    count = 72
    for i in lName:
        msg[count] = i
        count += 1
    # Отправляем клиенту
    conn.send(msg)

# Создает сообщение о чате юзера
def SendAboutChatData(conn, chatId, userId):
    chatId = struct.pack("q", chatId)
    userId = struct.pack("q", userId)
    msg = bytearray(48)
    # Задаем начальные параметры
    msg[0] = 1
    msg[1] = 1
    msg[2] = 3
    # Копируем chatId
    count = 32
    for i in chatId:
        msg[count] = i
        count += 1
    # Копируем userId
    count = 40
    for i in userId:
        msg[count] = i
        count += 1
    # Отправляем клиенту
    conn.send(msg)

# Создает сообщение о юзеру
def SendMessageData(conn, message):
    ownerId = struct.pack("q", message[1])
    recipientId = struct.pack("q", message[2])
    chatId = struct.pack("q", message[3])
    messageId = struct.pack("q", message[0])

    msg = bytearray(8192)
    # Задаем начальные параметры
    msg[0] = 1
    msg[1] = 1
    msg[2] = 4
    # Копируем ownerId
    count = 6
    for i in ownerId:
        msg[count] = i
        count += 1
    # Копируем recipientId
    count = 14
    for i in recipientId:
        msg[count] = i
        count += 1
    # Копируем chatId
    count = 22
    for i in chatId:
        msg[count] = i
        count += 1
    # Копируем messageId
    count = 30
    for i in messageId:
        msg[count] = i
        count += 1
    # Копируем дату и время в формате ГГ(по 2)МДЧМС
    msg[38] = int(message[5].year/100)
    msg[39] = int(message[5].year%100)
    msg[40] = int(message[5].month)
    msg[41] = int(message[5].day)
    msg[42] = int(message[5].hour)
    msg[43] = int(message[5].minute)
    msg[44] = int(message[5].second)
    #Копируем текст сообщения
    count = 92
    for i in message[4].encode('utf16'):
        msg[count] = i
        count += 1

    # Отправляем клиенту
    conn.send(msg)



#Создает и отправляет сообщение о себе
def SendChatsAndUsersData(conn, data, chatId):
    id = struct.pack("q", data[0])
    fName = data[1].encode('utf16')
    lName = data[2].encode('utf16')
    chatId = struct.pack("q", chatId)
    msg = bytearray(104)
    #Задаем начальные параметры
    msg[0] = 1
    msg[1] = 1
    msg[2] = 5
    #Копируем chatId
    count = 24
    for i in chatId:
        msg[count] = i
        count += 1
    #Копируем id
    count = 32
    for i in id:
        msg[count] = i
        count += 1
    #Копируем имя
    count = 40
    for i in fName:
        msg[count] = i
        count += 1
    #Копируем фаилию
    count = 72
    for i in lName:
        msg[count] = i
        count += 1
    #Отправляем клиенту
    conn.send(msg)
