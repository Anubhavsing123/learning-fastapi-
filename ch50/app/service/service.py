from app.db.config import session
from app.user.model import User
from sqlalchemy import select
async def create_user(nam:str,email:str):
    async with session() as sess:
        user=User(name=nam,email=email)
        sess.add(user)
        await sess.commit()
async def get_all():
    async with session() as sess:
        tmt=select(User)
        user=await sess.scalars(tmt)
        return user.all()
    


