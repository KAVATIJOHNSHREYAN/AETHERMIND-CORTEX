"""
AetherMind Cortex Decision Intelligence Engine
Provides Multi-Criteria Decision Analysis (MCDA), weighted option scoring, risk assessment, and decision history tracking.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from database.connection import DBConnection
from core.logger import get_logger

logger = get_logger("DecisionEngine")

class DecisionEngine:
    """Decision Intelligence Engine supporting MCDA weighted scoring and alternative ranking."""

    def __init__(self, db_conn: Optional[DBConnection] = None):
        self.db_conn = db_conn or DBConnection()

    def evaluate_decision(
        self,
        topic: str,
        options: List[str],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Executes Multi-Criteria Decision Analysis (MCDA) over candidate options.
        Criteria: Speed, Cost, Maintainability, Scalability, Risk.
        """
        if not options:
            return {"error": "No options provided."}

        default_weights = {
            "speed": 0.2,
            "cost": 0.2,
            "maintainability": 0.25,
            "scalability": 0.25,
            "risk": 0.1
        }
        w = weights or default_weights

        scored_options = []
        for idx, opt_name in enumerate(options):
            # Compute heuristic scores based on option traits
            is_simple = any(k in opt_name.lower() for k in ["sqlite", "script", "simple", "fast", "local"])
            is_enterprise = any(k in opt_name.lower() for k in ["postgres", "microservice", "distributed", "cloud", "k8s"])

            speed_score = 90.0 if is_simple else 65.0
            cost_score = 95.0 if is_simple else 60.0
            maintain_score = 90.0 if not is_enterprise else 75.0
            scale_score = 95.0 if is_enterprise else 70.0
            risk_score = 85.0 if is_simple else 70.0

            total_score = (
                speed_score * w["speed"] +
                cost_score * w["cost"] +
                maintain_score * w["maintainability"] +
                scale_score * w["scalability"] +
                risk_score * w["risk"]
            )
            total_score = round(total_score, 1)

            risk_level = "Low" if total_score >= 85.0 else ("Medium" if total_score >= 70.0 else "High")
            pros = "High speed, simple local setup, low maintenance overhead." if is_simple else "High scalability, production reliability, enterprise ready."
            cons = "Limited distributed horizontal scaling." if is_simple else "Higher operational complexity & resource requirements."

            scored_options.append({
                "option_name": opt_name,
                "score": total_score,
                "risk_level": risk_level,
                "pros": pros,
                "cons": cons
            })

        # Rank options descending by score
        scored_options.sort(key=lambda x: x["score"], reverse=True)
        recommended = scored_options[0]

        decision_id = str(uuid.uuid4())
        confidence = min(98.0, round(recommended["score"] + 5.0, 1))

        # Save to SQLite
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO decisions (id, topic, recommended_option, confidence_score) VALUES (?, ?, ?, ?)",
                    (decision_id, topic, recommended["option_name"], confidence)
                )
                for opt in scored_options:
                    cursor.execute(
                        "INSERT INTO decision_options (id, decision_id, option_name, score, risk_level, pros, cons) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (str(uuid.uuid4()), decision_id, opt["option_name"], opt["score"], opt["risk_level"], opt["pros"], opt["cons"])
                    )
            logger.info(f"Saved decision evaluation [{decision_id}] for topic: '{topic}'")
        except Exception as e:
            logger.error(f"Failed to save decision record: {e}")

        return {
            "decision_id": decision_id,
            "topic": topic,
            "recommended_option": recommended["option_name"],
            "confidence_score": confidence,
            "ranked_options": scored_options
        }

    def list_saved_decisions(self) -> List[Dict[str, Any]]:
        """Lists historical saved decision evaluations."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, topic, recommended_option, confidence_score, feedback_rating, created_at FROM decisions ORDER BY created_at DESC")
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Failed to list saved decisions: {e}")
            return []

    def update_decision_feedback(self, decision_id: str, rating: int) -> bool:
        """Updates user feedback rating (1-5 stars) for continuous learning."""
        try:
            with self.db_conn.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE decisions SET feedback_rating = ? WHERE id = ?", (rating, decision_id))
            logger.info(f"Updated feedback rating for decision [{decision_id}]: {rating} stars")
            return True
        except Exception as e:
            logger.error(f"Failed to update decision feedback: {e}")
            return False
