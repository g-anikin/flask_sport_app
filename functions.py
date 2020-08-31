from DatabaseInterface import DatabaseInterface
from flask import request


def generate_all_body_part_from_db_lst(db):
    connect_to_db = DatabaseInterface(db)
    a = connect_to_db.select_parts()
    all_body_part_from_db = []
    for i in a:
        for j in i[0].split(','):
            all_body_part_from_db.append(j)
    all_body_part_from_db = set(all_body_part_from_db)
    all_body_part_from_db = list(all_body_part_from_db)
    all_body_part_from_db.sort()
    return all_body_part_from_db


def generate_body_parts_lst_from_checkbox_lst(all_body_part_from_db):
    body_parts_lst_from_checkbox = []
    for i in all_body_part_from_db:
        if len(request.form.getlist(i)) != 0:
            body_parts_lst_from_checkbox.append(request.form.getlist(i)[0])
    return body_parts_lst_from_checkbox


def generate_select_string_for_random(body_parts_lst_from_checkbox):
    select_str0 = 'select name, body_part, about, pic_link from exercises where '
    select_str1 = ''
    for i in body_parts_lst_from_checkbox:
        select_str1 = select_str1 + f'body_part like "%{i}%" or '
    select_str1 = select_str1[:-4]
    select_str = select_str0 + select_str1
    return select_str

if __name__ == '__main__':
    generate_random_html()