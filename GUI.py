from datetime import datetime
import os
import json
import PySimpleGUI as sg

# менюшка в главном окне
main_menu = [["Добавить/удалить группу", ["Добавить группу", "Удалить группу"]]]
add_student_menu = [["Добавить ученика", ["Добавить ученика"]]]

# подгрузка списка групп из JSON
try:
    with open("groups.json", "r") as f:
        groups_array = json.load(f)
except:
    groups_array = ["начинающие", "средние", "сильные"]

# текущая отформатированная дата и время
now = datetime.now().strftime("%d-%m-%Y")


# функции импорта и экспорта файлов
def import_from_json(folder):
    """импортирует фамилии из файла JSON

    Args:
        event (_str_): словарь с учениками
    """
    global students_dic
    try:
        with open(f"{folder}.json", mode="r", encoding="utf-8") as file_json:
            students_dic = json.load(file_json)
    except:
        students_dic = {"Базаев": 20, "Данилова": 75, }


def export_to_json(folder):
    """экспортирует данные учеников в виде словаря JSON

    Args:
        folder (_str_): папка группы
    """
    with open(f"{folder}.json", mode="w", encoding="utf-8") as file_json:
        json.dump(students_dic, file_json, ensure_ascii=False, sort_keys=True)


def import_from_text(student_name):
    """импортирует лог ученика из его личного файла .txt

    Args:
        student_name (_type_): фамилия ученика
    """
    global student_log
    with open(f"Лидеркоины/{folder}/{student_name}.txt", encoding="utf-8") as file_txt:
        student_log = file_txt.read()


def export_to_text(student_name, student_log):
    """экспортирует лог ученика в личный файл .txt

    Args:
        student_name (_str_): фамилия ученика
        student_log: лог ученика
    """
    with open(f"Лидеркоины/{folder}/{student_name}.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(student_log)

1
# функции добавления учеников и групп
def create_adding_group_window():
    layout = [
        [sg.Input(size=20, key="ADD_GROUP_INPUT")],
        [sg.Button("Добавить группу", key="ADD_GROUP_BUTTON")],
        [sg.Text("", key="ADD_GROUP_TEXT")]
    ]
    return sg.Window(title="Добавление группы", layout=layout,
                     finalize=True,  return_keyboard_events=True, size=(500, 200))


def create_group(name_of_new_group):
    """создаёт новую группу и добавляет её в файл JSON

    Args:
        name_of_new_group (_str_): имя новой группы
    """
    global main_layout, groups_array
    groups_array.append(name_of_new_group)
    with open("groups.json", "w", encoding="utf-8") as f:
        json.dump(groups_array, f, ensure_ascii=False, sort_keys=True)
    open(f"{name_of_new_group}.json", "w").close()
    new_group_window["ADD_GROUP_INPUT"].update(value="")
    new_group_window["ADD_GROUP_TEXT"].update(
        value=f"Группа {name_of_new_group} была создана")


def create_student(name_of_student): #доделать эту функцию. Пока тут тупо копипаст 
    students_dic[name_of_student] = 0
    # create_student(adding_student_window["ADD_STUDENT_INPUT"].get())
    export_to_json(folder=folder)
    adding_student_window["ADD_STUDENT_INPUT"].update(value="")
    adding_student_window["ADD_STUDENT_TEXT"].update(
        value=f"Ученик {name_of_student} был добавлен")
    return students_dic


def create_deletegroup_window():
    global deletegroup_layout
    deletegroup_layout = []
    for group in groups_array:
        deletegroup_layout.append(
            [sg.Button(f"удалить {group}")])
    deletegroup_layout.append([sg.Text(text="", key="DELETE_STATUS_TEXT")])
    return sg.Window(title="Удаление группы", layout=deletegroup_layout,
                     finalize=True,  return_keyboard_events=True, size=(300, 300))


def delete_group(name_of_group):
    """удаляет группу из файла groups.json и стирает её файл JSON

    Args:
        name_of_group (_str_): имя удаляемой группы
    """
    
    os.remove(f"{name_of_group}.json")
    groups_array.remove(name_of_group)
    with open("groups.json", "w", encoding="utf-8") as f:
        json.dump(groups_array, f, ensure_ascii=False, sort_keys=True)
    deletegroup_window["DELETE_STATUS_TEXT"].update(
        value=f"{name_of_group} была удалена")
    # deletegroup_layout.remove(sg.Button(f"удалить {name_of_group}"))
    # deletegroup_window.refresh()

def create_adding_student_window():
    layout = [
        [sg.Input(size=20, key="ADD_STUDENT_INPUT")],
        [sg.Button("Добавить ученика", key="ADD_STUDENT_BUTTON")],
        [sg.Text("", key="ADD_STUDENT_TEXT")]
    ]
    return sg.Window(title="Добавление ученика", layout=layout,
                     finalize=True,  return_keyboard_events=True, size=(500, 200))

def delete_student():
    pass
# другие функции


def change_coins(change_coins_window):
    """изменяет баллы

    Args:
        number_of_coins (_int_): количество монеток
    """
    number_of_coins = int(change_coins_window["COINS_INPUT"].get())
    for_what = change_coins_window["FOR_WHAT_INPUT"].get()
    students_dic[student_name] = students_dic[student_name] + \
        number_of_coins
    export_to_json(folder)
    create_message(student_name, number_of_coins, for_what)
    change_coins_window["FOR_WHAT_INPUT"].update(value="")
    change_coins_window["COINS_INPUT"].update(value="")


def how_much_coins(quantity_of_coins):
    """проверяет, сколько коинов надо зачислить. Работает для кнопок быстрого зачисления

    Args:
        quantity_of_coins (_int_): количество баллов

    Return:
        for_what (_str_): за что получил баллы
    """
    if quantity_of_coins == 2:
        for_what = "посещение"
    elif quantity_of_coins == 5:
        for_what = "победу"
    elif quantity_of_coins == 10:
        for_what = "участие в онлайн турнире"
    return for_what


def simple_change_coins(student_name, quantity_of_coins):
    """прибавляет/вычитает баллы по кнопке

    Args:
        student_name (_str_): имя студента
        quantity_of_coins (_int_): количество баллов
    """
    for_what = how_much_coins(quantity_of_coins)
    students_dic[student_name] = students_dic[student_name] + quantity_of_coins
    group_window["STATUS"].update(
        value=f"{now} {student_name} зачислено {quantity_of_coins} коинов за {for_what}")
    export_to_json(folder)
    create_message(student_name, quantity_of_coins, for_what)
    group_window[f"{student_name} quantity_of_coins_COINS"].update(
        students_dic[student_name])


def create_message(student_name, quantity_of_coins_of_coins, for_what):
    """создает сообщение о новой операции в текстовом логе и отображает изменения в окне STUDENT_LOG

    Args:
        student_name (_str_): имя ученика
        quantity_of_coins_of_coins (_int_): количество коинов
        for_what (_str_): за что получил
    """
    with open(f"Лидеркоины/{folder}/{student_name}.txt", "a", encoding="utf-8") as file_txt:
        file_txt.write(
            f"\n{now} {student_name} {quantity_of_coins_of_coins} за {for_what}. Сейчас у него/неё {students_dic[student_name]}")
    group_window["STATUS"].update(
        f"\n{now} {student_name} {quantity_of_coins_of_coins} за {for_what}. \nСейчас у него/неё {students_dic[student_name]}")
    if student_window:
        import_from_text(student_name)
        student_window["STUDENT_LOG"].update(student_log)


# фунции создания окон
def create_main_window():
    """создание основного окна"""
    global main_layout
    main_layout = [[sg.Menu(main_menu)]]
    for group in groups_array:
        main_layout.append([sg.Button(group)])
    return sg.Window(title="Лидеркоины", layout=main_layout, finalize=True,  return_keyboard_events=True, size=(500, 500), resizable=True)


def create_group_window(event):
    """создаёт окно группы

    Args:
        event (_str_): имя папки группы

    Returns:
        _window_: окно группы
    """
    global btn_list, folder
    folder = event
    btn_list = []
    import_from_json(folder)
    group_layout = [[sg.Menu(add_student_menu)],
                    [sg.Text(" \n ", key="STATUS")]]
    for name, value in students_dic.items():
        group_layout.append([sg.Button(name, size=(15, 0)), sg.Text(value, key=f"{name} quantity_of_coins_COINS", size=(5, 0)),
                             sg.Button("2", key=f"2 {name}", size=(3, 0)),
                             sg.Button("5", key=f"5 {name}", size=(3, 0)),
                             sg.Button("10", key=f"10 {name}", size=(3, 0))])
        btn_list.append(f"2 {name}")
        btn_list.append(f"5 {name}")
        btn_list.append(f"10 {name}")
    return sg.Window(folder, group_layout, finalize=True,  return_keyboard_events=True, )


def create_student_window(event):
    """создаёт окно карточки ученика

    Args:
        event (_str_): имя ученика на кнопке

    Returns:
        _window_: окно карточки ученика
    """
    global student_log, student_name
    import_from_text(event)
    student_name = event
    student_layout = [[sg.Text(event), sg.Text(students_dic[event])],
        [sg.Button("Добавить/вычесть"), sg.Button("Сохранить изменения"), sg.Button("Отмена")],
        [sg.Multiline(default_text=student_log,
                    size=(400, 300), key="STUDENT_LOG")],
        ]
    return sg.Window(event, student_layout, finalize=True,  return_keyboard_events=True, size=(500, 800))


def create_change_coins_window():
    """создаётся окошко добавления или вычитания коинов
    """
    change_coins_layout = [
        [sg.Input(size=(10, 10), key="COINS_INPUT"),
         sg.Input(key="FOR_WHAT_INPUT")],
        [sg.Button("Добавить")],
    ]
    return sg.Window("Добавить/вычесть", change_coins_layout,
                     finalize=True,  return_keyboard_events=True)

# основной цикл программы


def main():
    global group_window, student_window, new_group_window, deletegroup_window, adding_student_window
    group_window, student_window, change_coins_window, new_group_window, deletegroup_window = \
        None, None, None, None, None
        
    adding_student_window = None
    while True:
        window, event, values = sg.read_all_windows()
        # закрытие окна
        if event == sg.WIN_CLOSED:
            window.close()
            if window == main_window:
                break
            if window == student_window:
                student_window = False
        else:
            if event == "Добавить группу":
                new_group_window = create_adding_group_window()
            elif event == "Удалить группу":
                deletegroup_window = create_deletegroup_window()
            # выбор группы
            elif event in groups_array:
                group_window = create_group_window(event)
            if event == "Добавить ученика":
                adding_student_window = create_adding_student_window()
            # создание других окон и обработка кнопок
            if group_window:
                if event in students_dic.keys():
                    student_window = create_student_window(event)
                elif event in btn_list:
                    coins_and_name = event.split()
                    print(coins_and_name)
                    simple_change_coins(coins_and_name[1], int(coins_and_name[0]))
            if new_group_window and event == "ADD_GROUP_BUTTON":
                create_group(new_group_window["ADD_GROUP_INPUT"].get())
            if adding_student_window and event == "ADD_STUDENT_BUTTON":
                create_student(adding_student_window["ADD_STUDENT_INPUT"].get())
            if deletegroup_window:
                if len(event.split()) > 1 and event.split()[1] in groups_array:
                    delete_group(event.split()[1])
            # обработка кнопок окна карточки ученика
            if event == "Сохранить изменения":
                export_to_text(
                    student_name, student_window["STUDENT_LOG"].get())
                window.close()
            elif event == "Добавить/вычесть":
                change_coins_window = create_change_coins_window()
            elif event == "Отмена":
                window.close()
            # окно зачисления и обработка его кнопок
            elif change_coins_window:
                if event == "Добавить":
                    change_coins(change_coins_window)


if __name__ == "__main__":
    main_window = create_main_window()
    main()

# TODO сделай возможность добавлять учеников
# FIXME запретить ввод букв в инпут изменения коинов
# FIXME если сделать быстрое добавление баллов после ручного добавления программа вылетает
