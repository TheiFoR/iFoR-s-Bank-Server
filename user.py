class User:
    empty = True

    name = ""
    rate = 1.0
    loan = 0

    def registered(self) -> bool:
        if self.name == "":
            return False
        return True
