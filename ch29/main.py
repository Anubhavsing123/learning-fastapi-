from table import create_table
from services import *
create_table()
create_user("anu","6576",76788007575)
create_user("raj","6576",76788007575)
create_post(1,1,"hello","my task is completed")
create_post(2,1,"hello ji","my task is completed on rock")
updated_user_email(1,"anub767800757@gmail.com")
#read data
# print(get_user_id(1))
# print(get_user())
print(get_post_id(2))
delete_post(2)

# user = get_user_id(1)
# if user:
#     print(f"User ID: {user[0]}, Name: {user[1]}")

# users = get_user()
# for u in users:
#     print(f"ID: {u[0]}, Name: {u[1]}, Email: {u[2]}, Phone: {u[3]}")