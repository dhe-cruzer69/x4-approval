from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import secrets

class RiskLevel(str, Enum):
    READ_ONLY = "read_only"
    LOW_REVERSIBLE = "low_reversible"
    EXTERNAL_COMM = "external_communication"
    FINANCIAL = "financial"
    PRODUCTION = "production_mutation"
    DESTRUCTIVE = "destructive"
    UNCERTAIN = "uncertain"

@dataclass
class ApprovalToken:
    token: str
    risk: RiskLevel
    issued_at: datetime
    expires_at: datetime
    action: str

    def is_valid(self) -> bool:
        return datetime.now(timezone.utc) < self.expires_at

class ApprovalGate:
    """Risk-based human-in-the-loop control."""

    AUTO_ALLOW = {RiskLevel.READ_ONLY, RiskLevel.LOW_REVERSIBLE}

    def classify(self, action: str) -> RiskLevel:
        a = action.lower()
        if any(w in a for w in ("delete", "drop", "destroy", "rm ")):
            return RiskLevel.DESTRUCTIVE
        if any(w in a for w in ("pay", "transfer", "charge", "invoice")):
            return RiskLevel.FINANCIAL
        if any(w in a for w in ("deploy", "prod", "production", "release")):
            return RiskLevel.PRODUCTION
        if any(w in a for w in ("email", "slack", "tweet", "post", "notify")):
            return RiskLevel.EXTERNAL_COMM
        if "read" in a or "list" in a or "get" in a:
            return RiskLevel.READ_ONLY
        return RiskLevel.UNCERTAIN

    def require_approval(self, action: str) -> bool:
        return self.classify(action) not in self.AUTO_ALLOW

    def issue_token(self, action: str, ttl_seconds: int = 300) -> ApprovalToken:
        now = datetime.now(timezone.utc)
        return ApprovalToken(
            token=secrets.token_urlsafe(24),
            risk=self.classify(action),
            issued_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            action=action,
        )
