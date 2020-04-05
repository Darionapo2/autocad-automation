

from Global import msp, doc

class DocumentReader:

    @classmethod
    def get_all_entities(cls) -> list:
        all_entities = doc.entities.__iter__()
        return [e for e in all_entities]
