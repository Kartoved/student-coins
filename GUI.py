import PySimpleGUI as sg
import json
import lidercoins


menu_def = [["Выбрать группу", ["начинающие", "средние", "сильные"]]]
array_groups = ["начинающие", "средние", "сильные"]
path = "pet_projects\\"

def import_from_json(event):
    """импортирует фамилии из файла JSON"""
    global dic_group
    try:
        with open(f"{event}.json", mode="r", encoding="utf-8") as file_json:
            dic_group = json.load(file_json)
    except:
        dic_group = {"Базаев": 20, "Данилова": 75, }



def make_main_window():
    """создание основного окна"""
    main_layout = [[sg.Menu(menu_def)],
              [sg.Button("начинающие")],
              [sg.Button("средние")],
              [sg.Button("сильные")],
              ]
    return sg.Window("Лидеркоины", main_layout, finalize=True,  return_keyboard_events=True,)


def make_group_window(event):
    """создаёт окно группы"""
    import_from_json(event)
    print(event)
    group_layout = []   
    for key in dic_group:
        group_layout.append([sg.Button(key)])
    return sg.Window(event, group_layout, finalize=True,  return_keyboard_events=True, size=(500, 500))


def main():
    """основной цикл программы"""
    while True:  # Event Loop
        window, event, values = sg.read_all_windows(timeout=10)
        if event == sg.WIN_CLOSED:
            window.close()
            if window == group_window:
                group_window = None
            elif window == main_window:
                break
        elif event in array_groups:
            group_window = make_group_window(event)


if __name__ == "__main__":
    main_window = make_main_window()
    main()
