import unittest
from pathlib import Path

from epistemic_alignment import models
from epistemic_alignment.artifacts import load_dossier


FIXTURE = Path(__file__).parents[1] / "templates/alignment"


class ThinBoundaryTests(unittest.TestCase):
    def test_dossier_loads_manifest_without_parsing_documents(self):
        dossier = load_dossier(FIXTURE)
        self.assertEqual(dossier.manifest["schema_version"], "1.0")
        self.assertIn("charter.md", dossier.snapshot_paths)
        self.assertIn("review.md", dossier.snapshot_paths)

    def test_semantic_entity_model_is_absent(self):
        self.assertFalse(hasattr(models, "Entity"))
        self.assertFalse(hasattr(models, "ValidationReport"))
