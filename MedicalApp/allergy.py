class Allergy:
    def __init__(self, id, name, description):
        if not isinstance(id, int):
            raise ValueError("Id must be an integer")
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"
