from app.data_import.florida import FloridaAssessmentProcessor


class PalmbeachAssessmentProcessor(FloridaAssessmentProcessor):
    def __init__(self, nap_file_name: str, nal_file_name: str, persist: bool, to_file: bool):
        super(PalmbeachAssessmentProcessor, self).__init__(
            provider_name='palmbeach',
            nap_file_name=nap_file_name,
            nal_file_name=nal_file_name,
            persist=persist,
            to_file=to_file
        )
