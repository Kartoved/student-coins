import json


# функции импорта и экспорта файлов
def import_from_json(folder: str):
    """импортирует фамилии из файла JSON"""
    global students_dic
    try:
        with open(f"{folder}.json", mode="r", encoding="utf-8") as file_json:
            students_dic = json.load(file_json)
    except:
        students_dic = {}


def export_to_json(folder: str):
    """экспортирует данные учеников в виде словаря JSON"""
    with open(f"{folder}.json", mode="w") as file_json:
        json.dump(students_dic, file_json, sort_keys=True)


def import_from_text(student_name: str):
    """импортирует лог ученика из его личного файла .txt"""
    global student_log
    with open(f"лидеркоины/{folder}/{student_name}.txt", encoding="utf-8") as file_txt:
        student_log = file_txt.read()


def export_to_text(student_name: str, student_log: str):
    """экспортирует лог ученика в личный файл .txt"""
    with open(f"лидеркоины/{folder}/{student_name}.txt", "w", encoding="utf-8") as file_txt:
        file_txt.write(student_log)
        

def create_group(name_of_new_group: str):
    """создаёт новую группу и добавляет её в файл JSON    """
    global main_layout, groups_array
    os.mkdir(f"лидеркоины//{name_of_new_group}")
    groups_array.append(name_of_new_group)
    with open("groups.json", "w", encoding="utf-8") as f:
        json.dump(groups_array, f, ensure_ascii=False, sort_keys=True)
    open(f"{name_of_new_group}.json", "w").close()
    new_group_window["ADD_GROUP_INPUT"].update(value="")
    new_group_window["ADD_GROUP_TEXT"].update(
        value=f"Группа {name_of_new_group} была создана")


def create_student(student_name):  # доделать эту функцию. Пока тут тупо копипаст
    students_dic[student_name] = 0
    # create_student(adding_student_window["ADD_STUDENT_INPUT"].get())
    open(f"лидеркоины//{folder}//{student_name}.txt", "w+")
    export_to_json(folder=folder)
    adding_student_window["ADD_STUDENT_INPUT"].update(value="")
    adding_student_window["ADD_STUDENT_TEXT"].update(
        value=f"Ученик {student_name} был добавлен")
    return students_dic
