# -*- coding: utf-8 -*-
import json
import os.path
import datetime
from datetime import datetime

now = datetime.now().strftime("%d-%m-%Y") # текущая отформатированная дата и время

def help():
    print("""\tсоздать - создает группу учеников
        добавить - добавляет ученика в группу
        удалить - удаляет ученика из группы
        изменить - добавляет/вычитает лидеркоины у ученика в формате: 'имя количество(цифрами) причина'
        изменить всем - добавляет/вычитает лидеркоины у всей группы
        изменить выбранным - добавляет/вычитает лидеркоины выбранным ученикам. Введите фамилии подряд, разделяя только пробелами
        список - выводит список учеников с лидеркоинами
        ученик - выводит количество лидеркоинов ученика
        выйти - выходит из функции/всей программы
        помощь - выводит команды и их описание"""
    )

def main_script():
    """Основной диалог. Программа предлагает пользователю
    выбрать команду"""
    while 1:
        command = input("Введите команду: ")
        if command.lower() == 'выйти':
            break
        elif command == 'добавить':
            add_student()
        elif command == 'удалить':
            delete_student()
        elif command == 'изменить':
            change_coins()
        elif command == 'изменить всем':
            change_all_students()
        elif command == 'изменить выбранным':
            change_coins_of_choosed_students()
        elif command == 'список':
            student_list()
        elif command == 'ученик':
            student_coins()
        elif command == 'помощь':
            help()
        elif command == 'создать':
            create_group()
        else:
            print("Выберите реальную команду! \n")
            main_script()

def add_student():
    """Добавляет ученика"""
    choose_group()
    while True:
        student_coins = input("Напишите имя ученика и изначальное количество баллов: ").split()
        if student_coins[0].lower() == "выйти":
            break
        group_dic[student_coins[0].title()] = int(student_coins[1])
        with open(group + '.json', 'w', encoding='utf-8') as f:  # перезаписывает словарь в файл
            json.dump(group_dic, f, ensure_ascii=False, sort_keys=True)
        with open(my_path + student_coins[0].title() + '.txt', "a", encoding='utf-8') as f:
            f.write(f"{now} Добавлен(а) {student_coins[0].title()} с {student_coins[1]} лидеркоином(ами). ")
        with open(my_path + group+'.txt', 'w', encoding='utf-8') as f:
            f.write(str(group_dic))
        print(f"{now} Добавлен(а) {student_coins[0].title()} с {student_coins[1]} лидеркоином(ами).")

def delete_student():
    """Удаляет ученика из списка"""
    choose_group()
    student_name = input("Напишите имя ученика, которого хотите удалить: ").title()
    if student_name.lower() == 'q':
        pass
    elif student_name not in group_dic:
        print("Такого ученика нет в списке ")
        delete_student()
    else:
        del group_dic[student_name]
        with open(group + '.json', 'w', encoding='utf-8') as f:  # перезаписывает словарь в файл
            json.dump(group_dic, f, ensure_ascii=False, sort_keys=True)
        print(f"Ученик {student_name} удален.")
        with open(my_path + group + '.txt', 'w', encoding='utf-8') as f:
            f.write(str(group_dic))

def choose_group():
    """Выбирает группу"""
    global group_dic, group, my_path
    group = input("Выберите группу: ")
    if group == "выйти":
        pass
    elif os.path.exists(group + '.json'):
        # импортирует словарь из файла группы
        with open(group + '.json', 'r', encoding='utf-8') as f:
            group_dic = json.load(f)
        my_path = "Лидеркоины\\"+ group + "\\"
        print(f"Выбрана группа {group}")
    else:
        print("Такой группы не существует!")
        choose_group()

def change_coins():
    """Изменяет количество баллов у ученика"""
    choose_group()
    while 1:
        student_change_coins = input("Кому, сколько и за что лидеркоинов? ").split()
        student_change_coins[0] = student_change_coins[0].title()
        if student_change_coins[0].lower() == "выйти":
            break
        try:
            student_change_coins[1] = int(student_change_coins[1])
        except ValueError:
            print("Введите число лидеркоинов цифрами!")
            continue
        
        if student_change_coins[0].title() not in group_dic:
            question = input("Такого ученика нет в списке! Желаете его добавить? да/нет ")
            if question.lower() == 'да':
                add_student()
            else:
                continue
        else:
            group_dic[student_change_coins[0]] = group_dic[student_change_coins[0]] + int(student_change_coins[1])
            with open(group + '.json', 'w', encoding='utf-8') as f:  # перезаписывает словарь в файл
                json.dump(group_dic, f, ensure_ascii=False, sort_keys=True)
            with open(my_path + student_change_coins[0] + '.txt', "a", encoding='utf-8') as f:
                f.write(f"\n{now} {student_change_coins[0].title()} зачислено {student_change_coins[1]} лидеркоин(ов\а) за {' '.join(student_change_coins[2:])}.")
                f.write(f" Сейчас у него(ее) {group_dic[student_change_coins[0]]}")
            with open(my_path + group + '.txt', 'w', encoding='utf-8') as f:
                f.write(str(group_dic))
            print(f"\n{now} {student_change_coins[0].title()} зачислено {student_change_coins[1]} лидеркоин(ов\а) за {' '.join(student_change_coins[2:])}")
            print(f"Сейчас у него(ее) {group_dic[student_change_coins[0]]}")

def student_list():
    """Выводит список всех учеников
    в группе с их лидеркоинами"""
    choose_group()
    print(group_dic)

def student_coins():
    """Выводит количество лидеркоинов ученика"""
    choose_group()
    while 1:
        name_of_student = input("Введите имя ученика: ").title()
        if name_of_student.lower() == 'выйти':
            break
        elif name_of_student not in group_dic:
            print("Такого ученика нет в списке!")
        else:
            print(f"{name_of_student} имеет {group_dic[name_of_student]} лидеркоинов")

def change_all_students():
    """Изменяет лидеркоины всех учеников в группе"""
    # TODO Почему-то выходит со второго раза. Разобраться 
    choose_group()
    how_much = int(input("Сколько баллов зачисляем всей группе? "))
    for_what = input("За что? ") # TODO сделать так, чтобы на выйти выходил из программы
    for key, value in group_dic.items():
        value = value + how_much
        group_dic[key] = group_dic[key] + how_much
        with open(my_path + str(key) + '.txt', "a", encoding='utf-8') as f:
            f.write(
                f"\n{now} {str(key).title()}  {how_much} лидеркоин(ов\а) за {for_what}")
            f.write(
                f" Сейчас у него(ее) {value}")
    print(f"Группе {group}  {how_much} за {for_what}")
    with open(group + '.json', 'w', encoding='utf-8') as f:  # перезаписывает словарь в файл
        json.dump(group_dic, f, ensure_ascii=False, sort_keys=True)
    with open(my_path + group + '.txt', 'w', encoding='utf-8') as f:
        f.write(str(group_dic))

def change_coins_of_choosed_students():
    choose_group()
    choosed_students = input("Введите фамилии учеников\n").split()
    how_much = int(input("Сколько лидеркоинов зачисляем? "))
    for_what = input("За что? ")
    for choosed_student in choosed_students:
        if choosed_student.title() in group_dic:
            group_dic[choosed_student.title()] += how_much
            value = group_dic[choosed_student.title()]
        with open(my_path + choosed_student.title() + '.txt', "a", encoding='utf-8') as f:
            f.write(
                f"\n{now} {choosed_student.title()} зачислено {how_much} коин(ов\а) за {for_what}")
            f.write(
                f" Сейчас у него(нее) {value}")
    print(f"{choosed_students} зачислено {how_much} за {for_what}")
    with open(group + '.json', 'w', encoding='utf-8') as f:  # перезаписывает словарь в файл
        json.dump(group_dic, f, ensure_ascii=False, sort_keys=True)
    with open(my_path + group + '.txt', 'w', encoding='utf-8') as f:
        f.write(str(group_dic))
        
def create_group():
    """Создает новую группу"""
    while 1:
        new_group = input("Введите имя новой группы: ")
        if new_group == "выйти":
            break
        empty_dic = {}
        with open(new_group + ".json", "w", encoding='utf-8') as f:
            json.dump(empty_dic, f, ensure_ascii=False, sort_keys=True)
        os.mkdir(f'{new_group}')
        with open(new_group + "\\" + new_group + ".txt", "w", encoding='utf-8') as f:
            f.write(str(empty_dic))
        print(f"Новая группа {new_group} создана")
        wanna_add_students = input("Хотите добавить учеников? да/нет ")
        if wanna_add_students == "да":
            add_student()

main_script()
