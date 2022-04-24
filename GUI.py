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


def import_from_text(event):
    """импортирует лог ученика из его личного файла .txt

    Args:
        event (_type_): фамилия ученика
    """
    global student_log
    with open(f"Лидеркоины\\{folder}\\{event}.txt", encoding="utf-8") as file_txt:
        student_log = file_txt.read()
    

def export_to_text(student_name):
    """экспортирует лог ученика в личный файл .txt

    Args:
        event (_str_): фамилия ученика
    """
    global student_log
    with open(f"Лидеркоины\\{folder}\\{student_name}.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(student_log)


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
    global folder
    import_from_json(event)
    group_layout = []
    folder = event
    for key, value in dic_group.items():
        group_layout.append([sg.Button(key), sg.Text(value)])
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
                      [sg.Button("Добавить/вычесть"), sg.Button("Сохранить изменения"), sg.Button("Отмена")],
                      [sg.Multiline(default_text=student_log,
                                    size=(400, 300), key="SAVE")],
                      ]
    return sg.Window(event, student_layout, finalize=True,  return_keyboard_events=True, size=(500, 800))


def main():
    """основной цикл программы"""
    global student_log
    main_window, group_window, student_window = make_main_window(), None, None
    while True:  # Event Loop
        window, event, values = sg.read_all_windows(timeout=10)
        if event == sg.WIN_CLOSED:
            window.close()
            if window == group_window:
                group_window = None
            elif window == student_window:
                student_window = None
            elif window == main_window:
                break
        elif event in array_groups:
            group_window = make_group_window(event)
        elif group_window:
            if event in dic_group.keys():
                print(event)
                student_window = make_student_window(event)
            if event == "Сохранить изменения":
                student_log = student_window["SAVE"].get()
                export_to_text(student_name)
                window.close()
            elif event == "Отмена":
                window.close()
                

if __name__ == "__main__":
    main_window = make_main_window()
    main()
