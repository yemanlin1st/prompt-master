import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "omega_promptforge_compile.py"
spec = importlib.util.spec_from_file_location("omega_promptforge_compile", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class PromptForgeCompilerTests(unittest.TestCase):
    def test_geofabric_activation_and_source_preservation(self):
        source = (
            "Connect with Google Maps and alternatives, use GitHub, keep it sovereign, "
            "inclusive, dynamic and reusable across the account."
        )
        result = module.compile_source(source)
        self.assertEqual(result["source_prompt"], source)
        self.assertIn("geofabric", result["run_record"]["activated_domain_packs"])
        self.assertIn(source, result["compiled_prompt"])
        self.assertIn("REQUIRES_AUTHORIZATION", result["run_record"]["intent_classes"])
        self.assertNotIn(result["run_record"]["maturity"], {"PRODUCTION_QUALIFIED", "LIVE"})

    def test_unrelated_prompt_does_not_activate_geofabric(self):
        source = "Rewrite this short paragraph in professional English."
        result = module.compile_source(source)
        self.assertNotIn("geofabric", result["run_record"]["activated_domain_packs"])
        self.assertEqual(result["source_prompt"], source)

    def test_empty_prompt_fails(self):
        with self.assertRaises(ValueError):
            module.compile_source("   ")

    def test_minimum_evidence_defaults_to_verify(self):
        result = module.compile_source("Design a secure enterprise workflow.")
        gates = result["run_record"]["quality_gates"]
        self.assertEqual(gates["intent_fidelity"], "PASS")
        self.assertEqual(gates["security"], "TO_VERIFY")
        self.assertEqual(gates["operationality"], "TO_VERIFY")


if __name__ == "__main__":
    unittest.main()
