import json
import sys

LIST_ACTIONS=[("L", "Список книг"),
             ("N", "Добавить новую книгу"),
             ("D", "Удалить книгу"),
             ("U", "Редактировать статус книги"),
             ("F", "Найти книгу по реквизитам"),
             ("E", "Завершить работу")
             ]
LIST_FIELDS=[("id", "Код книги","I"),
              ("title", "Название книги", "S"),
              ("author", "Автор книги", "S"),
              ("year", "Год", "I"),
              ("status","Состояние", "S")
              ]

VALID_LIT_ACTIONS=["L", "l", "N", "n", "D", "d", "E", "e", "U", "u", "F", "f"]


def max_id():
    MAX_ID=0
    if data:
        for key in data:
            if int(key) > MAX_ID:
                    MAX_ID = int(key)
    return MAX_ID


def list_book():
    print(f"{LIST_FIELDS[0][1]:<10} | {LIST_FIELDS[1][1]: <40} | {LIST_FIELDS[2][1]: <30} | {LIST_FIELDS[3][1]: <4} | {LIST_FIELDS[4][1]:<10}")
    print("=" * 105)
    for key in data:
            print(f"{key:<10} | {data[key]["title"]: <40} | {data[key]["author"]: <30} | {data[key]["year"]: <4} | {data[key]["status"]:<10}")
    print("=" * 105)


def add_book(list_values, next_id):
    values={}
    for i in range(len(list_values)):
        values[LIST_FIELDS[i+1][0]]=int(list_values[i]) if LIST_FIELDS[i+1][2]=="I" else list_values[i]
    values["status"]="в наличии"
    data[next_id]=values
    return "Инфо о книге добавлена!"


def del_book(key):
    res=data.pop(key)
    return "Инфа о книге с названием <" + res["title"] + "> удалена"


def update_status_book(key, val):
    data[key]["status"]=val
    return "Статус книги названием <" + data[key]["title"] + "> изменен"


def find_book(f_values):
    lits=["x", "X", "х", "Х"]
    list_criteria=[]
    for i in range(len(f_values)):
        if f_values[i] not in lits:
            list_criteria.append([LIST_FIELDS[i+1][0],int(f_values[i]) if LIST_FIELDS[i+1][2]=="I" else f_values[i]])
    res="По заданным критериям книга не найдена!"
    for key in data:
        counter = 0
        for i in range(len(list_criteria)):
            if data[key][list_criteria[i][0]]==list_criteria[i][1]:
                counter+=1
        if counter==len(list_criteria):
            res = f"{key:<10} | {data[key]["title"]: <40} | {data[key]["author"]: <30} | {data[key]["year"]: <4} | {data[key]["status"]:<10}"
    return res


with open('test.json', 'r', encoding="UTF-8") as fd:
    data = json.load(fd)
NEXT_ID=max_id()+1
print(NEXT_ID)
while True:
    print("Выберите действие, для этого введите один из предложенных символов:")
    for el in LIST_ACTIONS:
        print(el[0] + '-' + el[1])
    mode = input('Ваш выбор: ')
    if not (mode) or mode not in VALID_LIT_ACTIONS:
        print("Ошибка!")
        continue
    mode=mode.upper()
    while True:
        if mode=="L":
            list_book()
            break
        if mode=="E":
            print("Goodbay!")
            with open('test.json', 'w') as fd:
                json.dump(data, fd, sort_keys=True)
            sys.exit()
            break
        if mode=="N":
            s_values = []
            for i in range(1,4):
                while True:
                    s_val = input('Введите значение для поля <' + LIST_FIELDS[i][1] + '>: ')
                    if s_val:
                        if LIST_FIELDS[i][2] == "I" and not s_val.isdigit():
                            print("Значение должно быт числом! Введите корректное значение")
                            continue
                        s_values.append(s_val)
                        break
                    else:
                        continue
            print(add_book(s_values, str(NEXT_ID)))
            NEXT_ID += 1
            break
        if mode=="D":
            while True:
                s_val = input('Введите значение для поля <' + LIST_FIELDS[0][1] + '>: ')
                if s_val:
                    if LIST_FIELDS[0][2] == "I" and not s_val.isdigit():
                        print("Значение должно быть числом! Введите корректное значение")
                        continue
                    if not (data.get(s_val, 0)):
                        print("Книги с таким кодом не существует! Введите другой")
                        continue
                    break
                else:
                    continue
            print(del_book(s_val))
            break
        if mode == "U":
            while True:
                s_val = input('Введите значение для поля <' + LIST_FIELDS[0][1] + '>: ')
                if s_val:
                    if LIST_FIELDS[0][2] == "I" and not s_val.isdigit():
                        print("Значение должно быть числом! Введите корректное значение")
                        continue
                    if not (data.get(s_val, 0)):
                        print("Книги с таким кодом не существует! Введите другой")
                        continue
                    break
                else:
                    continue
            s_id=s_val
            while True:
                s_val=input("Введите значение для поля статус (<в наличии> или <выдана>)")
                if not s_val or s_val not in ("в наличии","выдана"):
                    print("Введите корректное значение!")
                    continue
                break
            print(update_status_book(s_id, s_val))
            break
        if mode=="F":
            lits = ["x", "X", "х", "Х"]
            print("Введите критерии для поиска (для пропуска реквизита ставим <х>)")
            find_values = []
            for i in range(1, 4):
                while True:
                    s_val = input('Введите значение для поля <' + LIST_FIELDS[i][1] + '>: ')
                    if not s_val:
                        continue
                    else:
                        if s_val not in lits:
                            if LIST_FIELDS[i][2] == "I" and not s_val.isdigit():
                                print("Значение должно быть числом! Введите корректное значение")
                                continue
                        break
                find_values.append(s_val)
            print(find_book(find_values))
            break
