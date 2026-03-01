class Custom:
    def __init__(self,app,prefix="LOG"):
        self.app=app
        self.prefix=prefix
    async def __call__(self,scope,recive,send):
        print(f"{self.prefix} :Before processing request (scope:{scope["method"]})")
        await self.app(scope,recive,send)
        print(f"{self.prefix}:After processing request")
    