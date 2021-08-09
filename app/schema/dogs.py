class DogDoc():
    name: str
    age: int

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __repr__(self):
        return str(self.__dict__)
