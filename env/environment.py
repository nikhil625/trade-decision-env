import random
from env.models import Observation, Reward
from env.tasks import TASKS
from env.grader import grade


class TradeEnv:
    def __init__(self):
        self.current_task = None
        self.done = False

    def reset(self):
        self.current_task = random.choice(TASKS)
        self.done = False

        return Observation(
            market=self.current_task["market"],
            proposal=self.current_task["proposal"],
            history=[]
        )

    def step(self, action):
        score, reason = grade(action, self.current_task)

        self.done = True

        return (
            Observation(
                market=self.current_task["market"],
                proposal=self.current_task["proposal"],
                history=[reason]
            ),
            Reward(value=score, reason=reason),
            self.done,
            {}
        )

    def state(self):
        return self.current_task