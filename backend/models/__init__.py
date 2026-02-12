"""
Modèles SQLAlchemy
Toutes les tables de la base de données
"""

from backend.models.user import User
from backend.models.user_config import UserConfig
from backend.models.exercise import Exercise
from backend.models.session_template import SessionTemplate
from backend.models.planning import Planning
from backend.models.training_session import TrainingSession
from backend.models.route import Route
from backend.models.goal_category import GoalCategory
from backend.models.running_session import RunningSession
from backend.models.program import Program
from backend.models.stats_cache import StatsCache
from backend.models.password_reset import PasswordResetToken
from backend.models.email_verification import EmailVerificationToken

__all__ = [
    "User",
    "UserConfig",
    "Exercise",
    "SessionTemplate",
    "Planning",
    "TrainingSession",
    "Route",
    "GoalCategory",
    "RunningSession",
    "Program",
    "StatsCache",
    "PasswordResetToken",
    "EmailVerificationToken",
]