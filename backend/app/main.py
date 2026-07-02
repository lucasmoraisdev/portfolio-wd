from fastapi import FastAPI

app = FastAPI(title="CMS WD Eventos Landing page", version="1.0.0", description="CMS WD Eventos Landing page")

@app.get("/health")
async def health_check():
    return {"status": "ok"}