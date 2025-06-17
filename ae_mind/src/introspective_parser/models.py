"""Pydantic data models for introspective parser."""

from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime


class Token(BaseModel):
    """Single token representation."""

    text: str
    lemma: Optional[str] = None
    pos: Optional[str] = None
    dep: Optional[str] = None


class Sentence(BaseModel):
    """Sentence made of tokens."""

    text: str
    tokens: List[Token]


class LinguisticBlock(BaseModel):
    """Container for linguistic data for one sentence."""

    sentence: Sentence
    tokens: List[str]
    lemmas: List[str]
    pos_tags: List[str]
    dependencies: List[str]
    speaker_id: Optional[str] = None
    utterance_id: Optional[str] = None


class PsychologicalInsight(BaseModel):
    """Basic psychological insight holder."""

    mbti: Optional[str] = None
    emotions: List[str] = []


class ASLTag(BaseModel):
    """Placeholder model for ASL semantic tags."""

    tag: str
    value: str


class PsychologicalBlock(BaseModel):
    """Comprehensive psychological analysis result for an utterance."""

    utterance_id: str
    speaker_id: str
    mbti_type: str
    mbti_confidence: float
    mbti_dimensions: Dict[str, float]
    emotion_primary: str
    emotion_confidence: float
    emotion_scores: Dict[str, float]
    cognitive_axis: str
    cognitive_functions: Dict[str, float]
    timestamp: datetime
    model_versions: Dict[str, str]


class BehavioralAuditBlock(BaseModel):
    """Behavioral and rhetorical analysis summary for a speaker."""

    speaker_id: str
    manipulative_phrases: List[str]
    rational_score: float
    emotional_score: float
    narrative_shift_index: float
    manipulation_scores: Dict[str, float]
    timestamp: datetime = datetime.utcnow()


class SpeakerProfile(BaseModel):
    """Aggregated longitudinal profile of a speaker."""

    speaker_id: str
    utterances: List[str]
    mbti_distribution: Dict[str, int]
    emotion_trends: Dict[str, List[float]]
    dominant_cognitive_functions: Dict[str, float]
    time_series: Dict[datetime, Dict[str, Optional[str]]]
    linguistic_summary: Dict[str, Optional[str]]
    psychological_blocks: List[PsychologicalBlock]
    linguistic_blocks: List[LinguisticBlock]
    behavioral_audit: BehavioralAuditBlock | None = None



class IntrospectiveInput(BaseModel):
    """Container linking linguistic and psychological blocks."""

    linguistic_block: Dict
    psychological_block: Dict
    speaker_metadata: Dict


class EthicalVectorBlock(BaseModel):
    """Ethical evaluation output for discourse."""

    human_rights_dignity: float
    environmental_sustainability: float
    diversity_inclusivity: float
    peaceful_just_societies: float
    algorithmic_fairness: float
    narrative_responsibility: float
    children_digital_protection: float
    strategic_vectors: List[str]
    ideological_shifts: Dict[str, float]
    narrative_coherence_score: float
    provenance: Dict[str, Any]

