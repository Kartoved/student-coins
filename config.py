import json
from datetime import datetime

# менюшка в главном окне
main_menu = [["Добавить/удалить группу",
              ["Добавить группу", "Удалить группу"]]]
add_student_menu = [["Добавить ученика", ["Добавить ученика"]]]

# подгрузка списка групп из JSON
try:
    with open("groups.json", "r", encoding='utf-8') as f:
        groups_array = json.load(f)
except FileNotFoundError:
    groups_array = []
    with open('groups.json', 'w') as f:
        json.dump(groups_array, f)

# текущая отформатированная дата и время
now = datetime.now().strftime("%d-%m-%Y")
