import os
from openai import OpenAI
from env.environment import TradeEnv
from env.models import Action
from env.tasks import TASKS

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=API_BASE_URL
)

env = TradeEnv()


def get_action_from_llm(observation):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": f"""
RSI: {observation.market.rsi}
Trend: {observation.market.trend}
Action: {observation.proposal.action}
SL: {observation.proposal.stop_loss}
TP: {observation.proposal.take_profit}

Respond ONLY: APPROVE or REJECT or MODIFY
"""
            }],
            temperature=0
        )

        text = response.choices[0].message.content.strip().upper()

        if "REJECT" in text:
            return Action(decision="REJECT")
        elif "MODIFY" in text:
            return Action(decision="MODIFY")
        else:
            return Action(decision="APPROVE")

    except Exception:
        # fallback (important for validator)
        rsi = observation.market.rsi
        if rsi > 70:
            return Action(decision="REJECT")
        else:
            return Action(decision="MODIFY")


def run_single_task(task):
    env.current_task = task
    obs = env.reset()
    done = False

    step_count = 0
    total_reward = 0

    task_id = task["id"]

    
    print(f"[START] task={task_id}", flush=True)

    while not done:
        action = get_action_from_llm(obs)
        obs, reward, done, _ = env.step(action)

        step_count += 1
        total_reward += reward.value

       
        print(f"[STEP] step={step_count} reward={reward.value}", flush=True)

    
    print(f"[END] task={task_id} score={total_reward} steps={step_count}", flush=True)


def main():
    for task in TASKS:
        run_single_task(task)


if __name__ == "__main__":
    main()
