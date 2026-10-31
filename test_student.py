
from database import create_table
from student import add_student, view_students, search_student

create_table()

print(add_student("Rahul Kumar", "MCA101", "MCA", 1))

print("\nAll Students:")
for student in view_students():
    print(student)

print("\nSearch Result:")
print(search_student("MCA101"))
