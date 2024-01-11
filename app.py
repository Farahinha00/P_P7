from fastapi import FastAPI

app = FastAPI()
/health

@app.get("/")
async def root():
    return {"message": "Hello World"}
