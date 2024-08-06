class Exceptions(Exception):
    def __init__(self, text: str):
        self.text = text


class PracticeException(Exceptions):
    ...


class UserException(Exceptions):
    ...
