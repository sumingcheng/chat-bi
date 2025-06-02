import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.server.api.setup:app", host="0.0.0.0", port=13000, reload=True)
