import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    COACH = "coach"
    TRAINER = "trainer"

class StudentCategory(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED_JUNIOR = "advanced"
    ADVANCED_SENIOR = "advanced_senior"
    ADULT = "adult"


