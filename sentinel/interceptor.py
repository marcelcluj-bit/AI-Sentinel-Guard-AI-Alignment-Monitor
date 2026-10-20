import hashlib
import time
from typing import Dict, Any

class AIGatekeeperSentinel:
    def __init__(self, agent_id: str, max_allowed_violations: int = 3):
        self.agent_id = agent_id
        self.max_violations = max_allowed_violations
        self.violation_counter = 0
        self.is_active = True

    def _analyze_prompt_safety(self, action: Dict[str, Any]) -> tuple[bool, str]:
        """Analyzes proposed agent action for safety violations or system command injections."""
        forbidden_keywords = ["rm -rf", "DROP TABLE", "eval(", "exec(", "export PRIVATE_KEY"]
        command = str(action.get("command", ""))
        
        for kw in forbidden_keywords:
            if kw in command:
                return False, f"Forbidden instruction detected: '{kw}'"
        
        return True, "Passed safety checks"

    def evaluate_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_active:
            raise PermissionError("Agent execution HALTED by Kill-Switch.")

        passed, reason = self._analyze_prompt_safety(action)
        exec_hash = hashlib.sha256(str(action).encode('utf-8')).hexdigest()

        if not passed:
            self.violation_counter += 1
            print(f"[ALERT] Safety Violation ({self.violation_counter}/{self.max_violations}): {reason}")
            
            if self.violation_counter >= self.max_violations:
                self.is_active = False
                print("[KILL-SWITCH TRIGGERED] Agent terminated locally.")

        return {
            "agent_id": self.agent_id,
            "execution_hash": exec_hash,
            "passed": passed,
            "reason": reason,
            "timestamp": time.time()
        }

# Example Usage
if __name__ == "__main__":
    sentinel = AIGatekeeperSentinel(agent_id="agent_alpha_01")
    
    # Safe Action
    res1 = sentinel.evaluate_action({"command": "SELECT * FROM analytics_db WHERE id = 1"})
    print("Execution 1:", res1)

    # Unsafe Action
    res2 = sentinel.evaluate_action({"command": "rm -rf /var/log/system"})
    print("Execution 2:", res2)
