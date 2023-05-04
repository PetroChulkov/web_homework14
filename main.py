import uvicorn
from ipaddress import ip_address
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from src.routes import contacts, auth, users
import redis.asyncio as redis
from src.conf.config import settings
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500', 'http://localhost:5500'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]

@app.get("/")
def read_root():
    """
    The default route for the application.
        """
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)