from fastapi import FastAPI

app = FastAPI()


@app.get('/healthz')
def healthz():
    return 'OK'

@app.get('/sunrise')
def sunrise():
    return '06:00'