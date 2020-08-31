from flask import Flask, render_template, request, redirect, url_for, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from random import choice
from DatabaseInterface import DatabaseInterface
from functions import generate_all_body_part_from_db_lst, generate_body_parts_lst_from_checkbox_lst, \
    generate_select_string_for_random

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "secret"

users = {'root': {'password': 'secret'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    try:
        if request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('index_page'))
    except KeyError:
        return render_template('bad_login.html')
    return render_template('bad_login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index_page():
    return render_template('index.html')
    # return redirect(url_for('login'))


@app.route('/table')
@login_required
def show_all():
    connect_to_db = DatabaseInterface('exercise.db')
    return render_template('index.html', table=1, items=connect_to_db.select_from_db())


@app.route('/body_parts')
@login_required
def select_parts():
    connect_to_db = DatabaseInterface('exercise.db')
    body_parts_lst = []
    for i in connect_to_db.select_parts():
        split_body_part = i[0].split(',')
        for j in split_body_part:
            body_parts_lst.append(j)
    body_parts_lst = set(body_parts_lst)
    body_parts_lst = list(body_parts_lst)
    body_parts_lst.sort()
    number_of_ids = []
    for i in range(1, len(body_parts_lst) + 1):
        number_of_ids.append(i)
    a = list(zip(number_of_ids, body_parts_lst))
    return render_template('index.html', table=2, items=a)


@app.route('/random', methods=['post', 'get'])
@login_required
def random():
    message = ''
    all_body_part_from_db = generate_all_body_part_from_db_lst('exercise.db')
    if request.method == 'POST':
        '''all_body_part_from_db - список для всех body_part из базы, разделенный по одной и отсортированный'''
        body_parts_lst_from_checkbox = generate_body_parts_lst_from_checkbox_lst(all_body_part_from_db)
        '''body_parts_lst_from_checkbox - список с отмеченными чекбоксами body_part'''
        select_str = generate_select_string_for_random(body_parts_lst_from_checkbox)
        '''select_str - селект-запрос с отмеченными чекбоксами body_part'''
        '''Проверка на корректное amount'''
        amount = request.form.get('amount')
        if amount.isdigit() and amount != 0:
            connect_to_db = DatabaseInterface('exercise.db')
            table = connect_to_db.select_query(select_str)
            s = ''
            rand_lst = []
            if int(amount) <= len(table):
                while len(rand_lst) != int(amount):
                    rand_lst.append(choice(table))
                    rand_lst = set(rand_lst)
                    rand_lst = list(rand_lst)
                return render_template('random.html', items=all_body_part_from_db, random_list=rand_lst, table=1)
            else:
                message = f'IN DATABASE YOU HAVE ONLY {len(table)} STRINGS. PLEASE ENTER LESS THAN {len(table) + 1}.'
        else:
            message = "You need to enter only positive digits"
    return render_template('random.html', items=all_body_part_from_db, message=message)


@app.route('/insert', methods=['post', 'get'])
@login_required
def insert_exercise():
    message = ''
    if request.method == 'POST':
        name = request.form.get('name')
        body_part = request.form.get('body_part')
        about = request.form.get('about')
        pic_link = request.form.get('pic_link')
        connect_to_db = DatabaseInterface('exercise.db')
        all_rows = connect_to_db.select_for_insert()
        if name == '' or body_part == '' or about == '' or pic_link == '':
            message = 'You need to enter all values'
            return render_template('insert.html', message=message)
        else:
            if (name, body_part, about, pic_link) not in all_rows:
                connect_to_db.add_exercise(name, body_part, about, pic_link)
                message = f'String with {name}, {body_part}, {about}, {pic_link} added to DB'
                return render_template('insert.html', message=message)
            else:
                message = 'This data is already in table'
                return render_template('insert.html', message=message)
    return render_template('insert.html', message=message)


@app.route('/delete', methods=['post', 'get'])
@login_required
def delete_exercise():
    message = ''
    if request.method == 'POST':
        id_number = request.form.get('id_number')
        connect_to_db = DatabaseInterface('exercise.db')
        connect_to_db.select_id()
        if id_number.isdigit():
            if (int(id_number),) in connect_to_db.select_id():
                connect_to_db.delete_exercise(id_number)
                message = f'String with ID = {id_number} deleted from DB'
            else:
                message = f'String with ID = {id_number} does not exists!'
        else:
            message = 'You need to enter positive digit!'
    return render_template('delete.html', message=message)


if __name__ == '__main__':
    app.run()
