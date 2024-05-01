class MedicalRoom:
    def __init__(self,room_number, description):
        if not isinstance(room_number, str):
            raise ValueError("Room Number must be a string")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        self.room_number = room_number
        self.description = description

    def __str__(self):
        return f"Room Number: {self.room_number}, Description: {self.description}"
