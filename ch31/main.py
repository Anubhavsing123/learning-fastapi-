from service import create_user,create_post,join_user_post
from table import create_table
create_table()
create_user("anu","6576",76788007575)
create_user("raj","6576",76788007575)
create_post(1,"hello","my task is completed")
create_post(1,"hello ji","my task is completed on rock")
create_post(1,"no to world","my job is over now you")
create_post(2,"no to meat","only veg")
create_post(2,"no to wine","mke country wine free")
print(join_user_post())
