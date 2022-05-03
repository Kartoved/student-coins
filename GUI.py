from array import array
from posixpath import split
import PySimpleGUI as sg
import json
import lidercoins


menu_def = [["Выбрать группу", ["начинающие", "средние", "сильные"]]]
array_groups = ["начинающие", "средние", "сильные"]


def import_from_json(event):
    """импортирует фамилии из файла JSON

    Args:
        event (_str_): словарь с учениками
    """
    global dic_group
    try:
        with open(f"{event}.json", mode="r", encoding="utf-8") as file_json:
            dic_group = json.load(file_json)
    except:
        dic_group = {"Базаев": 20, "Данилова": 75, }


def export_to_json():
    """экспортирует данные учеников в виде словаря JSON
    """
    with open(f"{folder}.json", mode="w", encoding="utf-8") as file_json:
        json.dump(dic_group, file_json, ensure_ascii=False, sort_keys=True)


def import_from_text(student_name):
    """импортирует лог ученика из его личного файла .txt

    Args:
        student_name (_type_): фамилия ученика
    """
    global student_log
    with open(f"Лидеркоины\\{folder}\\{student_name}.txt", encoding="utf-8") as file_txt:
        student_log = file_txt.read()


def export_to_text(student_name):
    """экспортирует лог ученика в личный файл .txt

    Args:
        student_name (_str_): фамилия ученика
    """
    with open(f"Лидеркоины\\{folder}\\{student_name}.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(student_log)


def make_change_coins_window():
    """создаётся окошко добавления или вычитания коинов
    """
    change_coins_layout = [
        [sg.Input(size=(10, 10), key="COINS"), sg.Input()],
        [sg.Button("Изменить")],
    ]
    return sg.Window("Добавить/вычесть", change_coins_layout,
                     finalize=True,  return_keyboard_events=True,)


def change_coins(change_coins_window):
    """изменяет баллы

    Args:
        number_of_coins (_int_): количество монеток
    """
    number_of_coins = int(change_coins_window["COINS"].get())
    print(number_of_coins)
    dic_group[student_name] = dic_group[student_name] + \
        number_of_coins
    export_to_json()


def simple_change_coins(student_name, quantity):
    """прибивляет/вычитает баллы по кнопке

    Args:
        student_name (_str_): имя студента
        quantity (_int_): количество баллов
    """
    dic_group[student_name] = dic_group[student_name] + quantity
    group_window["STATUS"].update(value=f"{student_name} зачислено {quantity} коинов")
    export_to_json()


def make_main_window():
    """создание основного окна"""
    main_layout = [[sg.Menu(menu_def)],
                   [sg.Button("начинающие")],
                   [sg.Button("средние")],
                   [sg.Button("сильные")],
                   ]
    return sg.Window("Лидеркоины", main_layout, finalize=True,  return_keyboard_events=True,)


def make_group_window(event):
    """создаёт окно группы

    Args:
        event (_str_): имя папки

    Returns:
        _window_: окно группы 
    """
    global folder, btn_list
    btn_list = []
    import_from_json(event)
    group_layout = [[sg.Text("", key="STATUS")]]
    folder = event
    for name, value in dic_group.items():
        group_layout.append([sg.Button(name), sg.Text(value),
                             sg.Button("2", key=f"2 {name}"), 
                             sg.Button("5", key=f"5 {name}"), 
                             sg.Button("-50", key=f"-50 {name}"), ])
        btn_list.append(f"2 {name}")
        btn_list.append(f"5 {name}")
        btn_list.append(f"-50 {name}")
    return sg.Window(event, group_layout, finalize=True,  return_keyboard_events=True, )


def make_student_window(event):
    """создаёт окно карточки ученика

    Args:
        event (_str_): имя ученика на кнопке

    Returns:
        _window_: окно карточки ученика
    """
    global student_log, student_name
    import_from_text(event)
    student_name = event
    student_layout = [[sg.Text(event), sg.Text(dic_group[event])],
                      [sg.Button(
                          "Добавить/вычесть"), sg.Button("Сохранить изменения"), sg.Button("Отмена")],
                      [sg.Multiline(default_text=student_log,
                                    size=(400, 300), key="SAVE")],
                      ]
    return sg.Window(event, student_layout, finalize=True,  return_keyboard_events=True, size=(500, 800))


def main():
    """основной цикл программы
    """
    global group_window
    main_window, group_window, student_window, change_coins_window = make_main_window(), None, None, None
    while True:  # Event Loop
        window, event, values = sg.read_all_windows()
        # закрытие окна
        if event == sg.WIN_CLOSED:
            window.close()
            if window == main_window:
                break
        # выбор группы
        elif event in array_groups:
            group_window = make_group_window(event)
        elif group_window:
            if event in dic_group.keys():
                student_window = make_student_window(event)
            elif event in btn_list:
                coins_and_name = event.split()
                simple_change_coins(coins_and_name[1], int(coins_and_name[0]))
        if event == "Сохранить изменения":
            student_log = student_window["SAVE"].get()
            export_to_text(student_name)
            window.close()
        elif event == "Добавить/вычесть":
            change_coins_window = make_change_coins_window()
        elif event == "Отмена":
            window.close()
        # окно зачисления
        elif change_coins_window:
            if event == "Изменить":
                change_coins(change_coins_window)


if __name__ == "__main__":
    main_window = make_main_window()
    main()

#TODO сделай обновление лидеркоинов в ГУИ
#TODO доделай окошко зачисления. Надо сделать поле "за что"
#TODO доделай рефакторинг
#TODO нужна ли менюшка??
#TODO сделай уведомление, что баллы зачислены при нажатии на кнопку
