from fastapi import FastAPI

app = FastAPI(title="CMS WD Eventos Landing page", version="1.0.0", description="CMS WD Eventos Landing page")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/health/database")
async def health_check_database():
    return {"status": "ok"}

@app.get("/health/storage")
async def health_check_storage():
    return {"status": "ok"}