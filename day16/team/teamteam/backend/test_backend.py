# team 폴더에서 python -B teamteam/backend/test_backend.py 로 실행합니다.
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import joblib
import pandas as pd
from fastapi.testclient import TestClient
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import Controller
from AppStart import app
from Service import RecoveryService


class RecoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.service = RecoveryService()
        cls.service.load_model()
        cls.team_dir = Path(__file__).resolve().parents[2]
        cls.saved_model = joblib.load(cls.team_dir.parent / "model.pkl")
        cls.sample = {
            "Age": 25, "Gender": "Male", "Training_Duration_Min": 60,
            "Training_Intensity": 7.5, "Sleep_Duration_Hours": 7.5,
            "Stress_Level": "Medium", "Caffeine_Intake_mg": 150, "Muscle_Soreness": 4.5,
        }

    def test_docs_and_schema(self):
        self.assertEqual(self.client.get("/docs").status_code, 200)
        schema = self.client.get("/openapi.json").json()
        self.assertIn("post", schema["paths"]["/api/predict"])
        self.assertEqual(schema["components"]["schemas"]["PredictRequest"]["required"], self.service.columns)
        self.assertEqual(list(schema["components"]["schemas"]["PredictRequest"]["properties"]), self.service.columns)

    def test_frontend_is_served(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn('id="prediction-form"', page.text)
        self.assertIn('id="recovery-value"', page.text)
        self.assertIn('id="r2-value"', page.text)
        self.assertEqual(self.client.get("/app.js").status_code, 200)
        self.assertEqual(self.client.get("/style.css").status_code, 200)

    def test_prediction_matches_saved_pipeline(self):
        response = self.client.post("/api/predict", json=self.sample)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        encoded = dict(self.sample, Gender=0, Stress_Level=2)
        expected = float(self.saved_model.predict(pd.DataFrame([encoded], columns=self.service.columns))[0])
        self.assertAlmostEqual(result["raw_prediction"], expected, places=12)
        self.assertAlmostEqual(result["predicted_recovery_score"], min(100, max(0, expected)), places=12)
        self.assertEqual(result["r2_score"], self.service.metrics["r2_score"])
        self.assertEqual(result["mae"], self.service.metrics["mae"])

    def test_missing_or_null_fields(self):
        self.assertEqual(self.client.post("/api/predict", json={}).status_code, 422)
        for field in self.sample:
            with self.subTest(field=field):
                missing = self.sample.copy()
                del missing[field]
                null_value = {**self.sample, field: None}
                self.assertEqual(self.client.post("/api/predict", json=missing).status_code, 422)
                self.assertEqual(self.client.post("/api/predict", json=null_value).status_code, 422)

    def test_decimals_categories_and_caffeine_zero(self):
        for gender, gender_code in [("Male", 0), ("Female", 1)]:
            for stress, stress_code in [("Low", 1), ("Medium", 2), ("High", 3)]:
                with self.subTest(gender=gender, stress=stress):
                    sample = dict(self.sample, Gender=gender, Stress_Level=stress, Caffeine_Intake_mg=0)
                    response = self.client.post("/api/predict", json=sample)
                    self.assertEqual(response.status_code, 200)
                    encoded = dict(sample, Gender=gender_code, Stress_Level=stress_code)
                    expected = self.saved_model.predict(pd.DataFrame([encoded], columns=self.service.columns))[0]
                    self.assertAlmostEqual(response.json()["raw_prediction"], expected, places=12)

    def test_training_range_is_not_api_limit(self):
        for sample in [
            {"Training_Duration_Min": 9}, {"Training_Duration_Min": 116},
            {"Training_Duration_Min": 60, "Age": 45},
            {"Training_Duration_Min": 60, "Sleep_Duration_Hours": 4},
            {"Training_Duration_Min": 60, "Caffeine_Intake_mg": 401},
        ]:
            with self.subTest(sample=sample):
                response = self.client.post("/api/predict", json={**self.sample, **sample})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.json()["warnings"])

    def test_invalid_inputs(self):
        samples = [
            {"Training_Duration_Min": 0},
            {"Training_Duration_Min": -1}, {"Training_Duration_Min": "60"},
            {"Training_Duration_Min": "abc"}, {"Training_Duration_Min": True},
            {"Training_Duration_Min": 60.5},
            {"Training_Duration_Min": 60, "Training_Intensity": 0.9},
            {"Training_Duration_Min": 60, "Training_Intensity": 10.1},
            {"Training_Duration_Min": 60, "Muscle_Soreness": 0.5},
            {"Training_Duration_Min": 60, "Muscle_Soreness": 10.1},
            {"Training_Duration_Min": 60, "Age": -5},
            {"Training_Duration_Min": 60, "Age": 25.5},
            {"Training_Duration_Min": 60, "Sleep_Duration_Hours": -1},
            {"Training_Duration_Min": 60, "Sleep_Duration_Hours": 25},
            {"Training_Duration_Min": 60, "Caffeine_Intake_mg": -1},
            {"Training_Duration_Min": 60, "Caffeine_Intake_mg": 1.5},
            {"Training_Duration_Min": 60, "Gender": "male"},
            {"Training_Duration_Min": 60, "Gender": "Non-binary"},
            {"Training_Duration_Min": 60, "Stress_Level": "medium"},
            {"Training_Duration_Min": 60, "unexpected": 1},
        ]
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(self.client.post("/api/predict", json={**self.sample, **sample}).status_code, 422)

    def test_nonfinite_and_broken_json(self):
        contents = [
            json.dumps(dict(self.sample, Training_Intensity=float("nan"))),
            json.dumps(dict(self.sample, Training_Intensity=float("inf"))),
            "{broken",
        ]
        for content in contents:
            with self.subTest(content=content):
                response = self.client.post("/api/predict", content=content, headers={"Content-Type": "application/json"})
                self.assertEqual(response.status_code, 422)
                self.assertIn("detail", response.json())

    def test_missing_model_returns_503(self):
        service = RecoveryService()
        service.model_path = service.model_path.with_name("missing-test-model.pkl")
        with patch.object(Controller, "recovery_service", service), self.assertLogs("Controller", level="ERROR"):
            response = self.client.post("/api/predict", json=self.sample)
        self.assertEqual(response.status_code, 503)
        self.assertNotIn(str(service.model_path), response.text)

    def test_column_mismatch_returns_500(self):
        service = RecoveryService()
        service.columns = list(reversed(service.columns))
        with patch.object(Controller, "recovery_service", service), self.assertLogs("Controller", level="ERROR"):
            response = self.client.post("/api/predict", json=self.sample)
        self.assertEqual(response.status_code, 500)

    def test_prediction_failure_hides_internal_details(self):
        with patch.object(Controller, "recovery_service", self.service), patch.object(self.service.model, "predict", side_effect=RuntimeError("internal-test-path")), self.assertLogs("Controller", level="ERROR"):
            response = self.client.post("/api/predict", json=self.sample)
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("internal-test-path", response.text)

    def test_clipping_preserves_original_prediction(self):
        for raw, score in [(-5.0, 0.0), (105.0, 100.0), (0.0, 0.0), (100.0, 100.0)]:
            with patch.object(Controller, "recovery_service", self.service), patch.object(self.service.model, "predict", return_value=[raw]):
                response = self.client.post("/api/predict", json=self.sample)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["raw_prediction"], raw)
            self.assertEqual(response.json()["predicted_recovery_score"], score)
            self.assertEqual(response.json()["score_was_clipped"], raw != score)

    def test_nonfinite_prediction_rejected(self):
        with patch.object(Controller, "recovery_service", self.service), patch.object(self.service.model, "predict", return_value=[float("nan")]), self.assertLogs("Controller", level="ERROR"):
            response = self.client.post("/api/predict", json=self.sample)
        self.assertEqual(response.status_code, 422)

    def test_cors(self):
        for origin in ["http://127.0.0.1:5500", "http://localhost:5500"]:
            response = self.client.options("/api/predict", headers={
                "Origin": origin, "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["access-control-allow-origin"], origin)
        response = self.client.options("/api/predict", headers={"Origin": "http://unapproved.example", "Access-Control-Request-Method": "POST"})
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access-control-allow-origin", response.headers)

    def test_saved_metrics_reproduce_on_holdout(self):
        df = pd.read_csv(self.team_dir / "athlete_recovery_synthetic.csv")
        df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})
        df["Stress_Level"] = df["Stress_Level"].map({"High": 3, "Medium": 2, "Low": 1})
        df = df.dropna()
        _, X_test, _, Y_test = train_test_split(
            df[self.service.columns], df["Recovery_Score"], test_size=0.2, random_state=42,
        )
        predictions = self.saved_model.predict(X_test)
        self.assertAlmostEqual(r2_score(Y_test, predictions), self.service.metrics["r2_score"], places=12)
        self.assertAlmostEqual(mean_absolute_error(Y_test, predictions), self.service.metrics["mae"], places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
