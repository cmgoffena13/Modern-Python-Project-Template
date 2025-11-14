class GrainValidationError(Exception):
    error_type = "Grain Validation Error"


class AuditFailedError(Exception):
    error_type = "Audit Failed"


class ValidationThresholdExceededError(Exception):
    error_type = "Validation Threshold Exceeded"


PIPELINE_EXCEPTIONS = {
    GrainValidationError,
    AuditFailedError,
    ValidationThresholdExceededError,
}
