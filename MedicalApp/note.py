class Note:
    def __init__(self, id, patient_id, note_taker_id, note_date, note):
        if not isinstance(id, int):
            raise TypeError("Illegal type for id")
        if not isinstance(patient_id, int):
            raise TypeError("Illegal type for patient id")
        if not isinstance(note_taker_id, int):
            raise TypeError("Illegal type for note taker id")
        if not isinstance(note_date, str):
            raise TypeError("Illegal type for note date")
        if not isinstance(note, str):
            raise TypeError("Illegal type for note")

        self.id = id
        self.patient_id = patient_id
        self.note_taker_id = note_taker_id
        self.note = note
