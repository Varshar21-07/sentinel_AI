from checker.risk_engine import calculate_final_risk

def test_risk_engine_block_override():
    # If rule allows, judge allows, but judge risk is CRITICAL, it should block
    result = calculate_final_risk("ALLOW", "rule ok", "ALLOW", "CRITICAL", "judge ok")
    assert result["final_decision"] == "BLOCK"

def test_risk_engine_rule_block():
    result = calculate_final_risk("BLOCK", "rule fail", "ALLOW", "LOW", "judge ok")
    assert result["final_decision"] == "BLOCK"

def test_risk_engine_all_clear():
    result = calculate_final_risk("ALLOW", "rule ok", "ALLOW", "LOW", "judge ok")
    assert result["final_decision"] == "ALLOW"
