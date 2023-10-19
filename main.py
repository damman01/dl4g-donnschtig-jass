from fastapi import FastAPI, Response, status

app = FastAPI()


@app.post("/select_trump")
async def select_trump():
    response = Response()
    #select trump
    response.status_code = status.HTTP_200_OK
    return response


@app.post("/play_card")
async def play_card():
    response = Response()
    #play card
    response.status_code = status.HTTP_200_OK
    return response


@app.post("/game_info")
async def game_info():
    response = Response()
    # process game info
    response.status_code = status.HTTP_200_OK
    return response



