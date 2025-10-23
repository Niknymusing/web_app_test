from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/hello")
def read_hello():
    timestamp = datetime.datetime.now().isoformat()
    return f"Hello, World! - Test {timestamp}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
