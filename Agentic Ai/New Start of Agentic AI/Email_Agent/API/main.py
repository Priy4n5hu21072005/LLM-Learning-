from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def message_function():
    return {"message":"Hi the fastapi backend is ready to devlop"}
