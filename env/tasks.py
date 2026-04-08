TASKS = [
    {
        "id": "easy_1",
        "market": {
            "price_history": [100, 102, 104, 106],
            "rsi": 80,
            "ema": 103,
            "trend": "uptrend"
        },
        "proposal": {
            "action": "BUY",
            "stop_loss": 1,
            "take_profit": 2
        },
        "correct_decision": "REJECT"
    },
    {
        "id": "medium_1",
        "market": {
            "price_history": [100, 99, 101, 100],
            "rsi": 50,
            "ema": 100,
            "trend": "sideways"
        },
        "proposal": {
            "action": "BUY",
            "stop_loss": 1,
            "take_profit": 1
        },
        "correct_decision": "REJECT"
    },
    {
        "id": "hard_1",
        "market": {
            "price_history": [100, 105, 103, 108],
            "rsi": 70,
            "ema": 104,
            "trend": "uptrend"
        },
        "proposal": {
            "action": "BUY",
            "stop_loss": 0.2,
            "take_profit": 5
        },
        "correct_decision": "MODIFY"
    }
]