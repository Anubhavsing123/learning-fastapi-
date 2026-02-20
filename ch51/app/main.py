from db.db import create_table
from service import *
#create_table()
#user=create_user("snoma","sonam@gmail.com")
create_user("anub","anub@gmail.com")
#print(user)
print(get_all_user())
print(get_user_id(2))
print(get_user_get(1))
