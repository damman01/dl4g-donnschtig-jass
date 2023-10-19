from jass.game.game_observation import GameObservation
from fastapi import FastAPI, Request, Response, status
from backend import select_trump as backend_select_trump

app = FastAPI()


@app.post("/select_trump")
async def select_trump(request: Request):
    try:
        body_json: str = await request.json()
        obs = GameObservation.from_json(body_json)
        if obs is not None:
            print(f"Successfully read in game observation.")

        trump = backend_select_trump(obs)

        if trump != -1:
            print(f"Successfully set trump.")

        return {"trump": trump}
    except Exception as exception:
        response = Response()
        print(f"An unexpected exception occurred: {exception}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
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



