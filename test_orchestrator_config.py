import json
import unittest
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def condition_matches(variable, condition, runtime_state):
    if variable == "budget":
        # Expected state key: budget_remaining_pct (0-100)
        return runtime_state.get("budget_remaining_pct", 100) <= 20

    if variable == "weather":
        # Expected state keys:
        # - aqi (numeric)
        # - torrential_rain (bool)
        aqi = runtime_state.get("aqi", 0)
        torrential_rain = runtime_state.get("torrential_rain", False)
        return aqi > 150 or bool(torrential_rain)

    if variable == "workload":
        # Expected state keys:
        # - unexpected_client_emergency (bool)
        # - sev1_outage (bool)
        return bool(runtime_state.get("unexpected_client_emergency", False)) or bool(
            runtime_state.get("sev1_outage", False)
        )

    raise ValueError(f"Unsupported trigger variable: {variable} ({condition})")


def process_triggers(config, runtime_state):
    active = []
    for trigger in config.get("triggers", []):
        variable = trigger["variable"]
        condition = trigger["condition"]
        if condition_matches(variable, condition, runtime_state):
            active.append(trigger)
    return active


class TestOrchestratorConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config()
        cls.by_variable = {t["variable"]: t for t in cls.config["triggers"]}

    def test_budget_trigger_activates_at_20_percent_or_lower(self):
        active = process_triggers(self.config, {"budget_remaining_pct": 20})
        variables = {t["variable"] for t in active}
        self.assertIn("budget", variables)

        budget_adjustment = self.by_variable["budget"]["adjustment"]
        self.assertIn("transportation", budget_adjustment)
        self.assertIn("gastronomy", budget_adjustment)
        self.assertIn("workspace", budget_adjustment)

    def test_budget_trigger_does_not_activate_above_20_percent(self):
        active = process_triggers(self.config, {"budget_remaining_pct": 21})
        variables = {t["variable"] for t in active}
        self.assertNotIn("budget", variables)

    def test_weather_trigger_activates_on_aqi(self):
        active = process_triggers(self.config, {"aqi": 151, "torrential_rain": False})
        variables = {t["variable"] for t in active}
        self.assertIn("weather", variables)

        weather_adjustment = self.by_variable["weather"]["adjustment"]
        self.assertIn("itinerary", weather_adjustment)
        self.assertIn("failsafe_activation", weather_adjustment)

    def test_weather_trigger_activates_on_torrential_rain(self):
        active = process_triggers(self.config, {"aqi": 50, "torrential_rain": True})
        variables = {t["variable"] for t in active}
        self.assertIn("weather", variables)

    def test_weather_trigger_does_not_activate_in_clear_conditions(self):
        active = process_triggers(self.config, {"aqi": 100, "torrential_rain": False})
        variables = {t["variable"] for t in active}
        self.assertNotIn("weather", variables)

    def test_workload_trigger_activates_on_emergency_or_sev1(self):
        active_emergency = process_triggers(
            self.config, {"unexpected_client_emergency": True, "sev1_outage": False}
        )
        active_sev1 = process_triggers(
            self.config, {"unexpected_client_emergency": False, "sev1_outage": True}
        )

        self.assertIn("workload", {t["variable"] for t in active_emergency})
        self.assertIn("workload", {t["variable"] for t in active_sev1})

        workload_adjustment = self.by_variable["workload"]["adjustment"]
        self.assertIn("itinerary", workload_adjustment)
        self.assertIn("logistics", workload_adjustment)

    def test_workload_trigger_does_not_activate_without_incident(self):
        active = process_triggers(
            self.config, {"unexpected_client_emergency": False, "sev1_outage": False}
        )
        variables = {t["variable"] for t in active}
        self.assertNotIn("workload", variables)

    def test_multiple_triggers_can_activate_together(self):
        active = process_triggers(
            self.config,
            {
                "budget_remaining_pct": 15,
                "aqi": 200,
                "torrential_rain": False,
                "unexpected_client_emergency": False,
                "sev1_outage": True,
            },
        )
        variables = {t["variable"] for t in active}
        self.assertEqual(variables, {"budget", "weather", "workload"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
