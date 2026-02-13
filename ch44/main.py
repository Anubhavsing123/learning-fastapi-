from model import create_table
import asyncio
from service import *

async def main():
    # create table
    # await create_table()
    # print(await create_user("anubhav","as9183181@gmail.com",76788007575))
    # print(await create_user("Avinash","anub765788@gmail.com",7678800757))
    # print(await create_user("Kanchan","anub7657880@gmail.com",76788007570))
    # print(await get_user_by_id(1))
    # print(await get_user_all())
    # print(await update_user(2,"anub7678899@gamil.com"))
    print(await delete_user(3))



asyncio.run(main())
