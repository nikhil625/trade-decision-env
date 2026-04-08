def grade(action, task):
    correct = task["correct_decision"]

    if action.decision == correct:
        return 1.0, "Correct decision"

    if action.decision == "MODIFY" and correct == "REJECT":
        return 0.5, "Partial credit"

    return 0.0, "Incorrect decision"