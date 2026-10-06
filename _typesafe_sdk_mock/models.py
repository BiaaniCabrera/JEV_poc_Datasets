from dataclasses import dataclass, field
from typing import Any, Dict, List, Union, Optional

@dataclass
class Noul:
    instructions: str

@dataclass
class Choice:
    instructions: str
    criteria: Dict[str, Any]

@dataclass
class Score:
    instructions: str
    criteria: List[str]

@dataclass
class NoulResult:
    noul: Union[bool, float]
    probability: float = 1.0

@dataclass
class ChoiceResult:
    choice: str
    confidence: float = 1.0

@dataclass
class ScoreResult:
    score: Union[str, float]
    raw_score: float = 1.0

@dataclass
class SystemOneResponse:
    nouls: Dict[str, NoulResult] = field(default_factory=dict)
    choices: Dict[str, ChoiceResult] = field(default_factory=dict)
    scores: Dict[str, ScoreResult] = field(default_factory=dict)

