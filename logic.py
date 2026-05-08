import json
from pathlib import Path
from typing import Dict, List, Any
from models import NomadState

CONFIG_PATH = Path("config_paris.json")

def load_config() -> Dict[str, Any]:
    """
    Loads the Parisian orchestration configuration from disk.
    
    Returns:
        Dict[str, Any]: The configuration dictionary containing triggers and rules.
    """
    if not CONFIG_PATH.exists():
        return {"triggers": []}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def check_condition(variable: str, condition: str, state: NomadState) -> bool:
    """
    Evaluates a specific orchestration condition against the current state.
    
    Args:
        variable: The state variable to check (e.g., 'budget', 'weather').
        condition: The logic condition to apply.
        state: The current NomadState object.
        
    Returns:
        bool: True if the condition is met, False otherwise.
    """
    if variable == "budget":
        return state.budget_remaining_pct <= 20
    if variable == "weather":
        return state.aqi > 100 or state.rain
    if variable == "workload":
        return state.emergency or state.high_workload
    return False

def get_adjustments(state: NomadState) -> List[Dict[str, Any]]:
    """
    Processes all triggers based on the current nomad state.
    
    Args:
        state: The current runtime state of the nomad.
        
    Returns:
        List[Dict[str, Any]]: A list of active adjustments (guidance, links, etc).
    """
    config = load_config()
    active = []
    for trigger in config.get("triggers", []):
        if check_condition(trigger["variable"], trigger["condition"], state):
            active.append(trigger)
    return active
