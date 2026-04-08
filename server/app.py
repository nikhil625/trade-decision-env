from fastapi import FastAPI
from env.environment import TradeEnv
from env.models import Action

app = FastAPI()
env = TradeEnv()


@app.get("/")
def root():
    return {"message": "Trade Decision Environment API is running"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()


@app.post("/step")
def step(action: dict):
    act = Action(**action)
    obs, reward, done, info = env.step(act)

    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()