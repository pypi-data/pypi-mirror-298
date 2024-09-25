from enum import Enum


class FeatureTypes(Enum):
    CODE_REVIEW = "code_review"
    DESCRIPTION_SUMMARIZE = "description_summarize"
    SAST_EXPLAIN = "sast_explain"
    SECRET_DETECTION = "secret_detection"
