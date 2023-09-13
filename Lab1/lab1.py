from flask import Flask, request
import psycopg2 as pg

app = Flask(__name__)

# подключение к бд
conn = pg.connect(user='postgres', password='', host='localhost', port='5432', database='Test')
cursor = conn.cursor()


# функция добавления данных по регионам
def add_region_bd(id, name):
    cursor.execute("""insert into region (id, name)
                                         values (%(id)s, %(name)s);""",
                   {"id": id, "name": name})
    conn.commit()


# функция добавления данных с объектом налогооблажения
def add_tax_param_bd(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate):
    cursor.execute("""insert into tax_param (
                                        id,
                                        city_id, 
                                        from_hp_car, 
                                        to_hp_car, 
                                        from_production_year_car, 
                                        to_production_year_car, 
                                        rate)
                                         values (
                                         %(id)s, 
                                         %(city_id)s, 
                                         %(from_hp_car)s, 
                                         %(to_hp_car)s, 
                                         %(from_production_year_car)s, 
                                         %(to_production_year_car)s, 
                                         %(rate)s);""",
                   {
                       "id": id,
                       "city_id": city_id,
                       "from_hp_car": from_hp_car,
                       "to_hp_car": to_hp_car,
                       "from_production_year_car": from_production_year_car,
                       "to_production_year_car": to_production_year_car,
                       "rate": rate})
    conn.commit()


# Задание 1 endpoint POST добавления информации о регионе
@app.route('/v1/add/region', methods=['POST'])
def add_region():
    # Проверка на полноту входящих данных если чего то не хвататет возвращает сообщение об ошибке
    if 'id' not in request.json or 'city_name' not in request.json:
        error_body = {'reason': 'id и/или name пуст(ы)'}
        return error_body, 400

    # Запись данных в переменные по ключу (то что в [])
    id = request.json['id']
    name = request.json['city_name']

    # получение данных из бд
    cursor.execute("""Select id from region""")
    region = cursor.fetchall()

    # проверка региона
    if id in region:
        return '400 BAD REQUEST'
    else:
        add_region_bd(id, name)
        return '200'


# Задание 2 endpoint добавления объекта налогообложения POST
@app.route('/v1/add/tax-param', methods=['POST'])
def add_tax_param():
    # Проверка на полноту входящих данных если чего то не хвататет возвращает сообщение об ошибке
    if 'id' not in request.json or 'city_id' not in request.json or 'from_hp_car' not in request.json or 'to_hp_car' not in request.json or 'from_production_year_car' not in request.json or 'to_production_year_car' not in request.json or 'rate' not in request.json:
        error_body = {'reason': 'Одно/несколько поле(й) пуст(ы)'}
        return error_body, 400

    # Запись входящих данных в переменные по ключу (то что в [])
    city_id = request.json['city_id']

    # получение данных из бд
    cursor.execute("""Select * from region where id = %(id)s""", {'id': city_id})
    region = cursor.fetchone()

    if region is None:
        return '400 BAD REQUEST'

    # Запись входящих данных в переменные по ключу (то что в [])
    id = request.json['id']
    city_id = request.json['city_id']
    from_hp_car = request.json['from_hp_car']
    to_hp_car = request.json['to_hp_car']
    from_production_year_car = request.json['from_production_year_car']
    to_production_year_car = request.json['to_production_year_car']
    rate = request.json['rate']

    # получение данных из бд
    cursor.execute("""Select id from tax_param""")
    region = cursor.fetchall()

    # проверка данных о объектах налогооблажения
    if id in region:
        return '400 BAD REQUEST'
    else:
        add_tax_param_bd(id, city_id, from_hp_car, to_hp_car, from_production_year_car, to_production_year_car, rate)
        return '200'


# Задание 3 endpoint добавления автомобиля
@app.route('/v1/add/auto', methods=['POST'])
def add_auto():
    # Проверка на полноту входящих данных если чего-то не хвататет возвращает сообщение об ошибке
    if 'id' not in request.json or 'city_id' not in request.json or 'tax_id' not in request.json or 'name' not in request.json or 'horse_power' not in request.json or 'production_year' not in request.json:
        error_body = {'reason': 'Одно/несколько поле(й) пуст(ы)'}
        return error_body, 400

    city_id = request.json['city_id']

    # получение данных из бд
    cursor.execute("Select * from region where id = %(id)s", {'id': city_id})
    region = cursor.fetchone()

    # Запись входящих данных в переменные по ключу (то что в [])
    tax_id = request.json['tax_id']
    horse_power = request.json['horse_power']
    production_year = request.json['production_year']

    # получение данных из бд по заданным параметрам
    cursor.execute("""Select rate from tax_param where id = %(id)s
                        and %(horse_power)s <= to_hp_car 
                        and %(horse_power)s > from_hp_car
                        and  %(production_year)s <= to_production_year_car
                        and  %(production_year)s > from_production_year_car
                        """, {'id': tax_id, 'horse_power': horse_power, 'production_year': production_year})
    rate = cursor.fetchone()

    # проверка данных о объектах налогооблажения и региноах в бд
    if region is None or rate is None:
        return '400 BAD REQUEST'

    # подсчёт налога
    id = request.json['id']
    name = request.json['name']
    tax = rate[0] * horse_power

    # Запись в бд информации по автомобилю
    cursor.execute("""insert into auto (
                                                id,
                                                city_id, 
                                                tax_id, 
                                                name, 
                                                horse_power, 
                                                production_year, 
                                                tax)
                                                 values (
                                                 %(id)s,
                                                 %(city_id)s, 
                                                 %(tax_id)s, 
                                                 %(name)s, 
                                                 %(horse_power)s, 
                                                 %(production_year)s, 
                                                 %(tax)s);""",
                   {
                       "id": id,
                       "city_id": city_id,
                       "tax_id": tax_id,
                       "name": name,
                       "horse_power": horse_power,
                       "production_year": production_year,
                       "tax": tax})
    conn.commit()
    return '200'


# Задание 4 endpoint получения информации по всем автомобилям
@app.route('/v1/auto/<id>', methods=['GET'])
def auto(id):
    cursor.execute("SELECT * FROM auto WHERE id=(%s)", (int(id),))
    auto = cursor.fetchone()
    message = {"Auto": f"{auto}"}
    return message


if __name__ == '__main__':
    app.run(debug=True)
