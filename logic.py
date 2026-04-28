def apply_business_logic(data):

    severity = data.get("issue_severity", "low")
    confidence = data.get("confidence_score", 0.5)
    risk = data.get("risk_flag", "low")

    action = "apology"
    token = {"type": "none", "value": "none"}
    needs_human = False

    if severity == "high":
        action = "refund"
        token = {"type": "coupon", "value": "10%"}
        needs_human = True

    elif severity == "medium":
        action = "coupon"
        token = {"type": "coupon", "value": "10%"}

    if risk == "high":
        action = "escalate"
        needs_human = True

    if confidence < 0.6:
        needs_human = True

    data["recommended_action"] = action
    data["goodwill_token"] = token
    data["needs_human"] = needs_human

    return data