import sqlite3, datetime, time


def connect():
    conn = sqlite3.connect('stat.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def db():
    conn, cursor = connect()
    try:
        cursor.execute(
            "create table users ('user_id' integer,'name' text,'date' text,'ref_code' text,'invite_by' text,'balance' text,'discount' integer,'ref_earn' text)")
        conn.commit()
    except:
        pass
    try:
        cursor.execute("create table check_qiwi ('user_id' integer,'code' integer,number text)")
        conn.commit()
    except:
        pass
    try:
        cursor.execute(
            """create table easypay_global_check (user_id integer,receiptId integer,amount integer)""")
        conn.commit()
        cursor.execute("insert into easypay_global_check values(1111,1,1)")
        conn.commit()
    except:
        pass
    try:
        cursor.execute("""create table check_id (id integer)""")
        conn.commit()
        cursor.execute("insert into check_id values(1111)")
        conn.commit()
    except:
        pass
    try:
        cursor.execute("""create table promo_code (promo text,bonus text)""")
        conn.commit()
    except:
        pass
    try:
        cursor.execute("create table buy_log (user_id integer,date text,product text")
        conn.commit()
    except:
        pass

    try:
        cursor.execute(
            'create table catalog (catalog_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,name text not null,parent_catalog_id integer)')
        conn.commit()
        cursor.execute(
            'create table product (product_id integer not null PRIMARY KEY AUTOINCREMENT,catalog_id integer not null,name text not null,descriptions text,cost NUMERIC)')
        conn.commit()
        cursor.execute('create table address (link text,product_id integer,person_id integer)')
        conn.commit()
        cursor.execute('insert into address values("test",0,0)')
        conn.commit()
    except Exception as e:
        print(e)
    try:
        qiwi_text = '⚠️ Пополните баланс QIWI:\n\n📱 Номер:  {number}\n💬 Коментарий:  {code}\n💲 Сумма  от 1 до 15000'
        easypay_text = '💸Пополнение баланса\n\n⚠️Оплата EasyPay\n\n👉Номер кошелька: {number}\n\n👉Отправьте в чат ID перевода и сумму платежа как на фото\n https://ibb.co/RSHhTjm \n'
        global24_text = '💸Пополнение баланса\n\n⚠️Оплата GlobalMoney\n\n👉Номер кошелька: {number}\n\n👉Отправьте в чат ID перевода и сумму платежа как на фото\n https://ibb.co/RSHhTjm \n'
        apirone_ltc = '💸Пополнение баланса\n\n⚠️Оплата GlobalMoney\n\n👉Номер кошелька: {number}\n\n👉Отправьте в чат ID перевода и сумму платежа как на фото\n https://ibb.co/RSHhTjm \n'
        info_message = """Информация:\n\nТут будет какая-либо информация о боте, админах, товарах и тд."""

        cursor.execute("""create table config (bot_url text,money_value text,referral_percent integer,
        info_message text,need_global24 integer,need_qiwi integer,need_easypay integer,need_promo integer,
        qiwi_text text,easypay_text text,global24_text text)""")
        conn.commit()

        cursor.execute('insert into config values(0,"USD",5,?,1,1,1,1,?,?,?)',
                       (info_message, qiwi_text, easypay_text, global24_text,))
        conn.commit()
    except:
        pass
    try:
        cursor.execute("""create table adm_id (value integer)""")
        conn.commit()
        cursor.execute('create table kur_id (value integer)')
        conn.commit()
        cursor.execute('create table channel_id (value text)')
        conn.commit()
        cursor.execute('create table qiwi (number text,token text)')
        conn.commit()
        cursor.execute('create table easypay (value integer)')
        conn.commit()
        cursor.execute('create table global24 (value integer)')
        conn.commit()
    except:
        pass
    try:
        cursor.execute('create table purchases (user_id integer,date text,product text)')
        conn.commit()
    except:
        pass

    cursor.close()
    conn.close()


def add_adm(id):
    conn, cursor = connect()
    cursor.execute('insert into adm_id values(?)', (id,))
    conn.commit()
    cursor.close()
    conn.close()


def remove_adm(id):
    conn, cursor = connect()
    try:
        cursor.execute('delete from adm_id where value=?', (id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def add_kur(id):
    conn, cursor = connect()
    cursor.execute('insert into kur_id values(?)', (id,))
    conn.commit()
    cursor.close()
    conn.close()


def remove_kur(id):
    conn, cursor = connect()
    try:
        cursor.execute('delete from kur_id where value=?', (id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def get_value(text, where="none", are="none", base='config'):
    conn, cursor = connect()
    try:
        if where == "none" and are == "none":
            message = cursor.execute(f'select {text} from {base}').fetchone()[0]
            return message
        elif where != 'none' and are != 'none':
            msg = cursor.execute(f'select {text} from {base} where {where}="{are}"').fetchone()[0]
            return msg
        else:
            m = cursor.execute(text).fetchone()[0]
            return m
    except:
        pass
    cursor.close()
    conn.close()


def get_valuedata(text):
    conn, cursor = connect()
    try:
        m = cursor.execute(text).fetchone()[0]
        return m
    except:
        pass
    cursor.close()
    conn.close()


def getLastWeekCount():
    date = datetime.date
    lsdsr = "select count(*) from purchases where "
    for i in range(0, 7):
        t = date.fromtimestamp(time.time() - i * 24 * 3600).isoformat()
        str = "date like '" + t + "%'"
        if i < 6:
            str = str + " or "
        lsdsr = lsdsr + str
    return lsdsr


def get_value_long(text):
    conn, cursor = connect()
    try:
        return cursor.execute(text).fetchone()[0]
    except:
        pass
    cursor.close()
    conn.close()


def get_values(text, where="none", are="none", base='config'):
    conn, cursor = connect()
    try:
        if where == "none" and are == "none":
            message = cursor.execute(f'select {text} from {base}').fetchall()
            return message
        elif where != 'none' and are != 'none':
            return cursor.execute(f'select {text} from {base} where {where}={are}').fetchall()
        else:
            pass
    except:
        pass
    cursor.close()
    conn.close()


def get_values_long(text):
    conn, cursor = connect()
    try:
        return cursor.execute(text).fetchall()
    except:
        pass
    cursor.close()
    conn.close()


def set_ref_code(user_id, code):
    conn, cursor = connect()
    cursor.execute('update users set invite_by=? where invite_by=?', (user_id, code,))
    conn.commit()
    cursor.execute('update users set ref_code=? where user_id = ?', (user_id, user_id,))
    conn.commit()
    cursor.close()
    conn.close()


def set_payments_value(type='need_qiwi'):
    conn, cursor = connect()
    if get_value(type) == 1:
        try:
            cursor.execute(f'update config set {type}=0')
            conn.commit()
        except Exception as e:
            print(e)
    else:
        try:
            cursor.execute(f'update config set {type}=1')
            conn.commit()
        except:
            pass
    cursor.close()
    conn.close()


def add_replenish(type='easypay', number=None, token=None):
    conn, cursor = connect()
    try:
        if token is None:
            cursor.execute(f'insert into {type} values(?)', (number,))
            conn.commit()
        else:
            cursor.execute(f'insert into {type} values(?,?)', (number, token,))
            conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def remove_replanish(type='easypay', number=None):
    conn, cursor = connect()
    try:
        if type != 'qiwi':
            cursor.execute(f'delete from {type} where value=?', (number,))
            conn.commit()
        else:
            cursor.execute(f'delete from {type} where number=?', (number,))
            conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def add_promo(promo, bonus):
    conn, cursor = connect()
    try:
        cursor.execute('insert into promo_code values(?,?)', (promo, bonus,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def set_discount(user_id, count):
    conn, cursor = connect()
    try:
        cursor.execute('update users set discount = ? where user_id=?', (count, user_id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def set_balance(user_id, count):
    conn, cursor = connect()
    try:
        cursor.execute('update users set balance = ? where user_id=?', (count, user_id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def remove_product(product_id, count):
    conn, cursor = connect()
    try:
        cursor.execute(
            f'delete from address where person_id in (select person_id from address where product_id={product_id} limit {count})')
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def update_value(set, value):
    conn, cursor = connect()
    cursor.execute(f'update config set {set}="{value}"')
    conn.commit()
    cursor.close()
    conn.close()
