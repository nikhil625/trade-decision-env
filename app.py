from fastapi import FastAPI
from env.environment import TradeEnv
from env.models import Action

app = FastAPI()

env = TradeEnv()


# ✅ Root endpoint (IMPORTANT for Hugging Face & validator)
@app.get("/")
def root():
    return {"message": "Trade Decision Environment API is running"}


# Reset environment
@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()


# Step function
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


# State endpoint
@app.get("/state")
def state():
    return env.state()
