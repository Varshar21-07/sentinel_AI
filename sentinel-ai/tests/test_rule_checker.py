from checker.rule_checker import check_rules

def test_rule_checker_allowed():
    result = check_rules("reset_password")
    assert result["decision"] == "ALLOW"

def test_rule_checker_forbidden():
    result = check_rules("delete_account")
    assert result["decision"] == "BLOCK"
