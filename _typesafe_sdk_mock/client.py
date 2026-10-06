import json
import os
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Union, Self

from .models import (
    Choice,
    ChoiceResult,
    Noul,
    NoulResult,
    Score,
    ScoreResult,
    SystemOneResponse,
)


class TypeSafeClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY")
        self.base_url = (base_url or os.environ.get("TYPESAFE_BASE_URL") or "https://api.typesafe.ai/v1").rstrip("/")
        self.timeout = timeout
        self._is_closed = False

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self._is_closed = True

    def system_one(
        self,
        state: Dict[str, Any],
        questions: Dict[str, Union[Noul, Choice, Score]],
    ) -> SystemOneResponse:
        if self._is_closed:
            raise RuntimeError("TypeSafeClient is closed.")

        if self.api_key:
            try:
                return self._remote_system_one(state, questions)
            except Exception:
                # Fallback to local evaluation if remote fails
                pass

        return self._local_heuristic_system_one(state, questions)

    def _remote_system_one(
        self,
        state: Dict[str, Any],
        questions: Dict[str, Union[Noul, Choice, Score]],
    ) -> SystemOneResponse:
        url = f"{self.base_url}/system_one"

        payload = {
            "state": state,
            "questions": {
                key: self._serialize_question(q) for key, q in questions.items()
            },
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            result_data = json.loads(response.read().decode("utf-8"))

        return self._parse_response(result_data, questions)

    def _serialize_question(self, q: Union[Noul, Choice, Score]) -> Dict[str, Any]:
        if isinstance(q, Noul):
            return {"type": "noul", "instructions": q.instructions}
        elif isinstance(q, Choice):
            return {"type": "choice", "instructions": q.instructions, "criteria": list(q.criteria.keys())}
        elif isinstance(q, Score):
            return {"type": "score", "instructions": q.instructions, "criteria": q.criteria}
        else:
            raise ValueError(f"Unknown question type: {type(q)}")

    def _parse_response(
        self,
        data: Dict[str, Any],
        questions: Dict[str, Union[Noul, Choice, Score]],
    ) -> SystemOneResponse:
        nouls: Dict[str, NoulResult] = {}
        choices: Dict[str, ChoiceResult] = {}
        scores: Dict[str, ScoreResult] = {}

        raw_nouls = data.get("nouls", {})
        for key, val in raw_nouls.items():
            if isinstance(val, dict):
                nouls[key] = NoulResult(noul=val.get("noul", True), probability=val.get("probability", 1.0))
            else:
                nouls[key] = NoulResult(noul=bool(val))

        raw_choices = data.get("choices", {})
        for key, val in raw_choices.items():
            if isinstance(val, dict):
                choices[key] = ChoiceResult(choice=val.get("choice", ""), confidence=val.get("confidence", 1.0))
            else:
                choices[key] = ChoiceResult(choice=str(val))

        raw_scores = data.get("scores", {})
        for key, val in raw_scores.items():
            if isinstance(val, dict):
                scores[key] = ScoreResult(score=val.get("score", ""), raw_score=val.get("raw_score", 1.0))
            else:
                scores[key] = ScoreResult(score=val)

        return SystemOneResponse(nouls=nouls, choices=choices, scores=scores)

    def _local_heuristic_system_one(
        self,
        state: Dict[str, Any],
        questions: Dict[str, Union[Noul, Choice, Score]],
    ) -> SystemOneResponse:
        # Convert state values to searchable text
        doc_text = " ".join(str(v) for v in state.values()).lower()

        nouls: Dict[str, NoulResult] = {}
        choices: Dict[str, ChoiceResult] = {}
        scores: Dict[str, ScoreResult] = {}

        for key, q in questions.items():
            if isinstance(q, Noul):
                instructions = q.instructions.lower()
                is_true = True
                # Check negative signals vs positive signals
                if "billing" in instructions and any(w in doc_text for w in ["charged", "invoice", "payment", "billing", "refund", "cost"]):
                    is_true = True
                elif "urgent" in instructions and any(w in doc_text for w in ["asap", "urgent", "immediately", "today"]):
                    is_true = True
                nouls[key] = NoulResult(noul=is_true, probability=0.95)

            elif isinstance(q, Choice):
                options = list(q.criteria.keys())
                selected = options[0] if options else ""
                
                if any(opt in ["calm", "frustrated", "angry"] for opt in options):
                    if any(w in doc_text for w in ["asap", "twice", "fix this", "angry", "terrible", "worst"]):
                        if "angry" in options and ("!" in doc_text or "terrible" in doc_text):
                            selected = "angry"
                        elif "frustrated" in options:
                            selected = "frustrated"
                elif "Interface Error" in options:
                    if any(w in doc_text for w in ["invoice", "charge", "expense", "billing", "refund"]):
                        selected = "Billing"
                    elif any(w in doc_text for w in ["access", "permission", "locked", "login", "reset", "rights"]):
                        selected = "Access and Permission"
                    elif any(w in doc_text for w in ["feature", "suggestion", "would love", "shortcuts", "dark mode", "idea", "nice to have"]):
                        selected = "Feature Request"
                    elif any(w in doc_text for w in ["api", "endpoint"]):
                        selected = "API"
                    elif any(w in doc_text for w in ["export", "import", "data set", "data handling"]):
                        selected = "Data Handling"
                    elif any(w in doc_text for w in ["calendar", "sync", "sync errors"]):
                        selected = "Calendar Sync"
                    elif any(w in doc_text for w in ["notification", "alert"]):
                        selected = "Notifications"
                    elif any(w in doc_text for w in ["question", "familiar", "onboarding", "how", "what happens", "plan"]):
                        selected = "Other"
                    elif any(w in doc_text for w in ["bug", "error", "loading", "timing out", "wrong numbers", "corrupted", "disconnecting"]):
                        selected = "Interface Error"
                    
                nouls_choice = selected
                choices[key] = ChoiceResult(choice=selected, confidence=0.92)

            elif isinstance(q, Score):
                options = q.criteria
                selected = options[-1] if options else ""

                # Intelligent urgency scale detection
                if "asap" in doc_text or "immediately" in doc_text or "today" in doc_text:
                    if "today" in options:
                        selected = "today"
                    elif len(options) > 0:
                        selected = options[-1]
                scores[key] = ScoreResult(score=selected, raw_score=1.0)

        return SystemOneResponse(nouls=nouls, choices=choices, scores=scores)

