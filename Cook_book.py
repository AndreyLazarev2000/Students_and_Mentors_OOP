#
# 1. Программа открывает и читает все переданные файлы, затем они мержатся в 1 объединенный файл.
# 2. Программа открывает файл и читает его построчно. Технические строки и разделители комментируются
# 3. Сначала считывается название блюда.
# 4. Затем считывается количество ингредиентов.
# 5. Для каждого ингредиента считывается строка, которая разбивается на название, количество и единицу измерения.
# 6. Все ингредиенты добавляются в список, который затем добавляется в словарь cook_book под ключом — названием блюда.
# 7. После обработки всех рецептов программа возвращает словарь cook_book
# 8. Объединенный файл сохраняется в файл cook_book, а строки раскомментируются и добавляются разделители для технической информации ========


import os

def read_cook_book(filename):
    cook_book = {}
    max_empty_lines = 20  # Максимальное количество пустых строк подряд

    with open(filename, 'r', encoding='utf-8') as file:
        empty_lines_count = 0  # Счётчик пустых строк

        while True:
            # Читаем строку
            line = file.readline()

            # Если строка пустая, увеличиваем счётчик
            if line.strip() == '':
                empty_lines_count += 1
                # Если достигнут порог пустых строк, завершаем чтение
                if empty_lines_count > max_empty_lines:
                    break
                continue  # Пропускаем пустые строки

            # Если строка не пустая, сбрасываем счётчик
            empty_lines_count = 0

            # Пропускаем закомментированные строки
            if line.strip().startswith('#'):
                continue

            # Читаем название блюда
            dish_name = line.strip()

            # Читаем количество ингредиентов
            try:
                ingredient_count_line = file.readline().strip()
                if not ingredient_count_line:  # Если файл закончился, выходим
                    print("Файл закончился неожиданно.")
                    break
                ingredient_count = int(ingredient_count_line)
            except ValueError:
                print(f"Ошибка: не удалось прочитать количество ингредиентов для блюда '{dish_name}'.")
                break

            # Читаем ингредиенты
            ingredients = []
            for _ in range(ingredient_count):
                ingredient_line = file.readline().strip()
                if not ingredient_line:  # Если файл закончился, выходим
                    print(f"Ошибка: недостаточно ингредиентов для блюда '{dish_name}'.")
                    break
                try:
                    ingredient_name, quantity, measure = ingredient_line.split(' | ')
                    ingredients.append({
                        'ingredient_name': ingredient_name,
                        'quantity': int(quantity),
                        'measure': measure
                    })
                except ValueError:
                    print(f"Ошибка: неверный формат ингредиента в блюде '{dish_name}'.")
                    break

            # Добавляем блюдо в cook_book
            cook_book[dish_name] = ingredients

    return cook_book


def merge_files(filenames, output_filename):
    # Список для хранения информации о файлах (имя файла, количество строк, содержимое)
    files_data = []

    # Читаем каждый файл
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Удаляем пустые строки
            non_empty_lines = [line for line in lines if line.strip()]
            files_data.append({
                'filename': os.path.basename(filename),  # Только имя файла, без пути
                'line_count': len(non_empty_lines),
                'content': non_empty_lines
            })

    # Сортируем файлы по количеству строк
    files_data.sort(key=lambda x: x['line_count'])

    # Записываем результат в объединённый файл
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        for file_data in files_data:
            # Записываем служебную информацию с комментариями
            output_file.write(f"#\n")
            output_file.write(f"#{file_data['filename']}\n")
            output_file.write(f"#{file_data['line_count']} строк\n")
            output_file.write(f"#\n")
            # Записываем содержимое файла
            output_file.writelines(file_data['content'])
            output_file.write(f"\n")


def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}  # Словарь для хранения итогового списка ингредиентов

    # Перебираем каждое блюдо из списка
    for dish in dishes:
        # Проверяем, есть ли такое блюдо в cook_book
        if dish in cook_book:
            # Перебираем ингредиенты блюда
            for ingredient in cook_book[dish]:
                name = ingredient['ingredient_name']
                measure = ingredient['measure']
                quantity = ingredient['quantity'] * person_count  # Умножаем на количество персон

                # Если ингредиент уже есть в списке, суммируем количество
                if name in shop_list:
                    shop_list[name]['quantity'] += quantity
                else:
                    shop_list[name] = {'measure': measure, 'quantity': quantity}
        else:
            print(f"Блюдо '{dish}' отсутствует в cook_book.")

    return shop_list


def print_dict(dictionary, name):
    print(f"{name} = {{")
    for key, value in dictionary.items():
        if isinstance(value, list):  # Если значение — это список (как в cook_book)
            print(f"  '{key}': [")
            for item in value:
                print(f"    {{'ingredient_name': '{item['ingredient_name']}', "
                      f"'quantity': {item['quantity']}, "
                      f"'measure': '{item['measure']}'}},")
            print("    ],")
        else:  # Если значение — это словарь (как в shop_list)
            print(f"  '{key}': {{'measure': '{value['measure']}', 'quantity': {value['quantity']}}},")
    print("}")


def reformat_merged_file(filename):
    # Читаем содержимое файла
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Обрабатываем строки
    new_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            if stripped_line == '#':
                # Если строка содержит только '#', заменяем на разделитель
                new_lines.append("=======\n")
            else:
                # Удаляем символ '#' и оставляем текст
                new_lines.append(stripped_line[1:] + '\n')
        else:
            # Оставляем строку без изменений
            new_lines.append(line)

    # Перезаписываем файл
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


# Список файлов
filenames = [
    r'C:\Users\Predator\Desktop\программируем_книги\учеба_нетология_25_26\Students_and_Mentors_OOP\recipes_1.txt',
    r'C:\Users\Predator\Desktop\программируем_книги\учеба_нетология_25_26\Students_and_Mentors_OOP\recipes_2.txt',
    r'C:\Users\Predator\Desktop\программируем_книги\учеба_нетология_25_26\Students_and_Mentors_OOP\recipes_3.txt'
]

# Объединяем файлы
output_filename = r'C:\Users\Predator\Desktop\программируем_книги\учеба_нетология_25_26\Students_and_Mentors_OOP\cook_book.txt'
merge_files(filenames, output_filename)

# Читаем объединённый файл и формируем cook_book
cook_book = read_cook_book(output_filename)

# Вывод результата
if cook_book:
    for dish, ingredients in cook_book.items():
        print(f"{dish}")
        print(f"{len(ingredients)}")
        for ingredient in ingredients:
            print(f"{ingredient['ingredient_name']} | {ingredient['quantity']} | {ingredient['measure']}")
        print()

    print("\nКулинарная книга:")
    # Красивый вывод словаря cook_book
    print_dict(cook_book, "cook_book")

    # Вызов функции get_shop_list_by_dishes
    shop_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, cook_book)

    print("\nСписок покупок:")
    # Красивый вывод словаря shop_list
    print_dict(shop_list, "shop_list")
else:
    print("Словарь рецептов пуст.")

# Перезаписываем файл, удаляя символы '#'
reformat_merged_file(output_filename)

