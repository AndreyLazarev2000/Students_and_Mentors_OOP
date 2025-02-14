#First commit#

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = None

        @property
        def average_grade(self):
            grades = [elem for num in self.grades.values() for elem in num]
            return sum(grades) / len(grades)

        def __str__(self):
            return f'''Имя: {self.name}
    Фамилия: {self.surname}
    Средняя оценка за домашние задания: {self.average_grade}
    Курсы в процессе изучения: {self.courses_in_progress}
    Завершенные курсы: {self.finished_courses}'''


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def __str__(self):
        text = f'Имя: {self.name} \nФамилия: {self.surname}'
        return text

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and \
                course in self.courses_attached and \
                course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.finished_courses += ['Git']
best_student.courses_in_progress += ['Python']
best_student.grades['Git'] = [10, 10, 10, 10, 10]
best_student.grades['Python'] = [10, 10]

print(best_student.finished_courses)
print(best_student.courses_in_progress)
print(best_student.grades)

cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
print(cool_mentor.courses_attached)

st1 = Student('Курва', 'Бобрович', 'Female')
st2 = Student('Бобр', 'Курвович', 'Male')
print(st1.name, st1.surname)
print(st2.name, st2.surname)
