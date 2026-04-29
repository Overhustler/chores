class ChoreList:
    def __init__(self, name: str, chores_file: str) -> None:
        self.name = name
        self.chores = self._create_chores(chores_file)

    def _create_chores(self, chores_file: str) -> list["Chore"]:
        chores = []
        with open(chores_file, 'r') as file:
            for line in file:
                name, time = line.strip().split(',')
                chores.append(Chore(name, time))
        return chores

    def getChores(self) -> list["Chore"]:
        return self.chores

    def add_chore(self, name: str, time: str) -> None:
        self.chores.append(Chore(name, time))

    def remove_chore(self, chore: "Chore") -> None:
        self.chores.remove(chore)


class Chore:
    def __init__(self, name: str, time: str, person_assigned: str | None = None) -> None:
        self._name = name
        self._time = time
        self._person_assigned = person_assigned

    def set_name(self, name: str) -> None:
        self._name = name
    def get_name(self) -> str:
        return self._name

    def set_time(self, time: str) -> None:
        self._time = time
    def get_time(self) -> str:
        return self._time

    def get_person_assigned(self) -> str | None:
        return self._person_assigned
    def set_person_assigned(self, person_assigned: str) -> None:
        self._person_assigned = person_assigned