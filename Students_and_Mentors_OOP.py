class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        avg_grade = self._calculate_avg_grade()
        return super().__str__() + f"\nСредняя оценка за лекции: {avg_grade}"

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1)



class Reviewer(Mentor):  # Эксперты наследуют от Mentor
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        return super().__str__()

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg_grade = self._calculate_avg_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg_grade}\nКурсы в процессе изучения: {courses_in_progress}\nЗавершенные курсы: {finished_courses}"

    def _calculate_avg_grade(self):
        if not self.grades:
            return 0
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return round(sum(all_grades) / len(all_grades), 1)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._calculate_avg_grade() < other._calculate_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._calculate_avg_grade() == other._calculate_avg_grade()

# Создаем экземпляры
student1 = Student('Баклан', 'Бакланов', 'male')
student1.courses_in_progress += ['Python']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Дося', 'Пельменова', 'female')
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ['Введение в программирование']

lecturer1 = Lecturer('Бобр', 'Курвович')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Женя', 'Куликова')
lecturer2.courses_attached += ['Git']

reviewer1 = Reviewer('Женя', 'Куликова')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Эмилия', 'Мортенс')
reviewer2.courses_attached += ['Git']

# Выставляем оценки
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)

student1.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer1, 'Python', 9)

# Выводим информацию
print(reviewer1)
print(lecturer1)
print(student1)
print(student2)

# Сравниваем студентов
if student1 > student2:
    print(f'У {student1.name} {student1.surname} средняя оценка выше, чем у {student2.name} {student2.surname}')
else:
    print(f'У {student1.name} {student1.surname} средняя оценка не выше, чем у {student2.name} {student2.surname}')

