import psycopg2
from contextlib import closing

params = "dbname=CourseDB user=postgres password=1251 host=localhost"
#Вернет user_id пользователя по логину-паролю или -1
def GetUserId(login, password):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT Id FROM Users WHERE login=%s and password=%s', (login, password))
            id = cursor.fetchone()
            if id:
                return id[0]
    return -1

#Вернет инфо о юзере по id
def GetUserInfoById(id):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM Users WHERE Id=%s', (str(id),))
            info = cursor.fetchone()
            if info:
                return info
    return -1


#Вернет инфо о юзере по телефону
def GetUserInfoByPhone(phone):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM Users WHERE phone=%s', (str(phone),))
            info = cursor.fetchone()
            if info:
                return info
    return -1


#Вернет инфо о юзере по телефону
def GetUserIdByPhone(phone):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT id FROM Users WHERE phone=%s', (str(phone),))
            info = cursor.fetchone()
            if info:
                return info
    return -1

#Вернет массив объектов chatId userId userId..., где один из userId - нащ
def GetUsersById(id):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select * from chats where user1Id=%s or user2Id=%s', (str(id), str(id)))
            info = cursor.fetchall()
            if info:
                return info
    return -1

#Вернет массив сообщений юзера по id
def GetMessagesByUserId(id):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select * from messages where ownerId=%s or recipientId=%s', (str(id), str(id)))
            info = cursor.fetchall()
            if info:
                return info
    return -1



#Добавит новое сообщение и вернет messageId
def AddNewMessage(ownerId, recipientId, chatId, text ,isOwnDel = False, isRecDel = False, isRecV = False):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'insert into messages (ownerid, recipientid, chatid, message, datetime, isownerdeleted, '
                           f'isrecipientdeleted, isrecipientviewed) values '
                           f'(%s,%s,%s, %s, NOW()::timestamp, false, false, false)',
                           (str(ownerId), str(recipientId), str(chatId), text))
            conn.commit()
            cursor.execute(f'select id, datetime from messages where ownerid=%s and recipientid=%s and chatid=%s'
                           f'order by datetime desc',
                           (str(ownerId), str(recipientId), str(chatId)))
            info = cursor.fetchone()
            return info



#Проверит логин и вернет True если он присутствует или False если нет
def CheckLogin(login):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select id from users where login=%s', (login,))
            info = cursor.fetchone()
            if info:
                return True
            return False


#Проверит телефон и вернет True если он присутствует или False если нет
def CheckPhone(phone):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select id from users where phone=%s', (phone,))
            info = cursor.fetchone()
            if info:
                return True
            return False

#Добавляет нового юзера в базу данных
def AddNewUser(fName, lName, pName, email, phone, login, password, year, month, day):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'insert into users (fname, lname, pname, email, phone, login, '
                           f'password, birthday) values '
                           f'(%s,%s,%s,%s,%s,%s,%s,%s)',
                           (str(fName), str(lName), str(pName), str(email), str(phone),
                            str(login), str(password), str(f'{year}-{month}-{day}')))
            conn.commit()


def CheckChat(userId1, userId2):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'select * from chats where user1Id=%s and user2Id=%s or user1Id=%s and user2Id=%s',
                           (str(userId1), str(userId2), str(userId2), str(userId1)))
            info = cursor.fetchone()
            if info:
                return True
            return False


#Добавит новый чат
def AddNewChat(userId1, userId2):
    with closing(psycopg2.connect(params)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'insert into chats (user1Id, user2Id) values (%s,%s)',
                           (str(userId1), str(userId2)))
            conn.commit()
            cursor.execute(f'select id from chats where user1Id=%s and user2Id=%s',
                           (str(userId1), str(userId2)))
            info = cursor.fetchone()
            return info