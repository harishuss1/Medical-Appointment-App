class Notes:

    def __init__(self, id, patient_id, note_taker_id, note_date, note):
        if not isinstance(id, int):
            raise ValueError("ID must be an Integer")
        self.id = id

        if not isinstance(patient_id, int):
            raise ValueError("Patient ID must be an Integer")
        self.patient_id = patient_id

        if not isinstance(note_taker_id, int):
            raise ValueError("Note Taker ID must be an Integer")
        self.note_taker_id = note_taker_id

        if not isinstance(note_date, str):
            raise ValueError("Note date must be a String")
        self.note_date = note_date

        if not isinstance(note, str):
            raise ValueError("Note must be an String")
        self.note = note
