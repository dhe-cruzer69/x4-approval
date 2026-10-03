"""x4-approval — Human-in-the-loop gates for Level 3 actions."""

__version__ = "0.1.0"


def requires_approval(action: str, policy: dict | None = None) -> bool:
    """Return True if action is a hard stop that needs human approval."""
    hard = {
        "delete_repository",
        "modify_secrets",
        "force_push_main",
        "change_visibility",
        "merge_without_review",
        "financial_transaction",
        "policy_bypass",
        "unknown_high_impact",
    }
    if policy and "triggers" in policy:
        hard = set(policy["triggers"])
    return action in hard
