import asyncio
async def add(a,b):
    await asyncio.sleep(1)
    return a+b
async def divide(a,b):
    await asyncio.sleep(1)
    if b==0:
        raise ValueError("Cannot be divide")
    return a/b


    