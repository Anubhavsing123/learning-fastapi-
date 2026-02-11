
import asyncio
from service import *
async def main():
    #create a table
    # await create_table()
    #create user data in the table
    await create_user("soname","anub7678800758@gmail.com","7985854331")
    # await create_user("anubhav","anub7678800757@gmail.com","7678800757")
    # await create_user("shanu","niii#","34567890")
    # print(await get_user_id(2))
    #print(await get_all_user())
    #print(await updated_email(3,"shanu@123gmail.com"))
    #await delete_user(3)
asyncio.run(main())