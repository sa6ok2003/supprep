import sqlite3
def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_list (
            name,
            number
            ) """)
    db.commit()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_ref
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
            chanel,
            parametr,
            person
            ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel1','nikolacinema',100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel2', 'filmsmarket',100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel3', 'Alitopprodaj',100))
        db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()


# Cоздание отслеживания подписчиков
    sql.execute(""" CREATE TABLE IF NOT EXISTS stata_parthers ( 
            id BIGINT,
            channel_ref
            ) """)
    db.commit()

    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (0,0))
        db.commit()

# ИНФО О ПАРТНЕРАХ ЧТО БЫ ПРИКРУТИТЬ ИМ СЧЕТЧИК
    sql.execute(""" CREATE TABLE IF NOT EXISTS parthers( 
                id_partn,
                name_channel,
                schet
                ) """)
    db.commit()

    # СЧЕТЧИК ТРАФИКА ОТ КОНКРЕТНОГО ПАРТНЕРА
    sql.execute(""" CREATE TABLE IF NOT EXISTS list_support( 
                    id,
                    name_channel,
                    status
                    ) """)
    db.commit()

    # СОЗДАНИЕ РАЗРЕШЕННЫХ support
    sql.execute(""" CREATE TABLE IF NOT EXISTS utm_support (
                       name,
                       info,
                       status
                       ) """)

    # АРХИВ ВЫПЛАТ
    sql.execute(""" CREATE TABLE IF NOT EXISTS listpay( 
                        data,
                        schetchik
                        ) """)
    db.commit()

def regviplata(data): # Регистрация выплатны
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sum = 0
    y = sql.execute(f"SELECT * FROM parthers").fetchall()
    for i in y:
        a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{i[1]}'").fetchone()[0]
        sum+=int(a)

    sql.execute(f"INSERT INTO listpay VALUES (?,?)", (data,sum)) # РЕГИСТРИРУЕМ ДАТУ И КОЛИЧЕСТВО ОПЛАЧЕННОГО ТРАФИКА
    db.commit()

def cheak_viplats():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    y = sql.execute(f"SELECT * FROM listpay").fetchall()
    return y


def reg_utm_support(utm,info): # Регистрация РАЗРЕШЕННЫХ support
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT name FROM utm_support WHERE name ='{utm}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO utm_support VALUES (?,?,?)", (utm,info,'1'))
        db.commit()
    else:
        return 1
    db.commit()

# РЕГИСТРАЦИЯ ЧЕЛОВЕКА ОТ САППОРТА
def reg_traf_support(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM list_support WHERE id ={id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO list_support VALUES (?,?,?)", (id, f'@{channel}', 0))
        db.commit()


def cheak_support(): # Позваращет ютм метку - Количество чел - Инфо об админе
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c = sql.execute(f"SELECT * FROM utm_support").fetchall()
    ansver = []
    for i in c:
        if i[2] == '1':
            a = sql.execute(f"SELECT COUNT(*) FROM list_support WHERE name_channel ='{i[0]}' ").fetchone()[0]  # Количество всех пользователей
            b1 = sql.execute(f"SELECT COUNT(*) FROM list_support WHERE name_channel ='{i[0]}' and status = 0").fetchone()[0]  # Количество неоплаченных пользователей
            ansver.append([i[0],i[1],a,b1])

    return ansver

# СОЗДАНИЕ ВЫПЛАТЫ = ИЗМЕНЕНИЕ СТАТУСА
def changee_support():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE list_support SET status = 1")
    db.commit()

## НОВОЕ
def cheach_channel_par(id): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers WHERE id_partn ={id}").fetchall()
    return r

def cheach_all_par(): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers").fetchall()
    return r

def info(channel): #Возвращает количество подписок на канал
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{channel}'").fetchone()[0]
    return a


def reg_partners_schet(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id_partn FROM parthers WHERE name_channel ='{channel}' and id_partn ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO parthers VALUES (?,?,?)", (id, channel, 0))
        db.commit()

## КОНЕЦ НОВОГО


###### Количество подписок на каналы партнеров
def reg_pod(id,channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{id}' and channel_ref ='{channel}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (id, channel))
        db.commit()


#Просмотр трафика
def info_chyornaya_vdova(): # Трафик Дена
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'chyornaya_vdova'").fetchone()[0]
    return a

def info_good_film1(): # Трафик Алексея
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'good_film1'").fetchone()[0]
    return a

def info_films_online_everyday(): # Трафик ЮЛИ
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'films_online_everyday'").fetchone()[0]
    return a


def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (name, 1))
        db.commit()
    db.commit()

def reg_channels(text): #Регистрация списка каналов
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    text = text.split()
    for i in text:
        i = i[1:]
        sql.execute(f"SELECT name FROM channel_list WHERE name ='{i}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (i, 1))
            db.commit()
        db.commit()

def proverka_channel(channel_name):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT name FROM channel_list WHERE name ='{channel_name}'").fetchone()
    if a is None:
        return 0
    else:
        return 1

def del_one_channel(name): #Удаление одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        pass
    else:
        sql.execute(f'DELETE FROM channel_list WHERE name ="{name}"')
        db.commit()


def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    list = [c1,c2,c3]
    return list


def obnovatrafika(channel1,channel2,channel3):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"UPDATE trafik SET parametr= '{channel1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel2}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel3}' WHERE chanel = 'channel3'")
    db.commit()