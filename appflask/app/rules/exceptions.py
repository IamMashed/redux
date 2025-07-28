

class AssessmentException(Exception):
    description = "Assessment Exception"

    def get_description(self):
        return self.description


class NotEnoughCompsException(AssessmentException):
    description = "No Comps were found for the given Subject Property using criteria"


class SubjectLacksDataException(AssessmentException):
    description = "Subject property does not have enough information for CMA"
