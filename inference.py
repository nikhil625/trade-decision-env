import os
from openai import OpenAI
from env.environment import TradeEnv
from env.models import Action

# Read environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=API_BASE_URL
)

env = TradeEnv()


def get_action_from_llm(observation):
    prompt = f"""
You are a trading decision evaluator.

Your job is to decide:
APPROVE, REJECT, or MODIFY

---

Examples:

Case 1:
RSI = 80, BUY → REJECT (overbought)

Case 2:
Sideways market, weak signal → REJECT

Case 3:
Trade direction is correct but stop_loss < 0.5 or take_profit > 4 → MODIFY (do NOT reject)

Case 4:
Everything reasonable → APPROVE

---

Now evaluate:

Market:
Price History: {observation.market.price_history}
RSI: {observation.market.rsi}
Trend: {observation.market.trend}

Trade:
Action: {observation.proposal.action}
Stop Loss: {observation.proposal.stop_loss}
Take Profit: {observation.proposal.take_profit}

---

Rules:
- RSI > 70 and BUY → REJECT
- Sideways market → REJECT
- stop_loss < 0.5 OR take_profit > 4 → MODIFY
- Otherwise → APPROVE

---

Answer ONLY:
APPROVE or REJECT or MODIFY
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = response.choices[0].message.content.strip().upper()

    if "REJECT" in text:
        return Action(decision="REJECT")
    elif "MODIFY" in text:
        return Action(decision="MODIFY")
    else:
        return Action(decision="APPROVE")


def run_episode():
    obs = env.reset()
    done = False
    total_reward = 0

    print("\nTask:", env.state()["id"])

    while not done:
        action = get_action_from_llm(obs)
        obs, reward, done, _ = env.step(action)

        print("Action:", action)
        print("Reward:", reward)

        total_reward += reward.value

    return total_reward


def run_all_tasks(num_runs=5):
    scores = []

    for i in range(num_runs):
        score = run_episode()
        print(f"Run {i+1}: Score = {score}")
        scores.append(score)

    avg_score = sum(scores) / len(scores)

    print("\nAverage Score:", avg_score)

    return avg_score


if __name__ == "__main__":
    final_score = run_all_tasks()
    print("\nFinal Benchmark Score:", final_score)