class Package:
    id: int = None
    data: dict = None

    def __init__(self, id: int, data: dict):
        self.id = id
        self.data = data
