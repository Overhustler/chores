from choreList import Chore, ChoreList


class Resident:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        chorelist: ChoreList,
        last_week_chores: list[Chore] | None = None
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.resident_restriction: dict[str, bool] = _initialize_restrictions(chorelist)
        self.last_week_chore_list: list[Chore] = last_week_chores if last_week_chores is not None else []

    def getDisplayName(self) -> str:
        return self.first_name + " " + self.last_name[0] + "."

    def set_last_week_chore_list(self, last_week: list[Chore]) -> None:
        self.last_week_chore_list = last_week

    def get_last_week_chore_list(self) -> list[Chore]:
        return self.last_week_chore_list

    def restrictions_including_last_week(self) -> dict[str, bool]:
        return add_last_week_to_restrictions(self.resident_restriction, self.last_week_chore_list)


class Singles(Resident):
    def __init__(self, first_name: str, last_name: str, chorelist: ChoreList, bed_number: int) -> None:
        self.bed_number = bed_number
        super().__init__(first_name, last_name, chorelist)


class FamilyResident(Resident):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        chorelist: ChoreList,
        pod_number: int,
        room_number: int,
        last_week_pod_chores: list[Chore] | None,
        pod_chores: ChoreList
    ) -> None:
        self.pod_number = pod_number
        self.room_number = room_number
        self.last_week_pod_chores: list[Chore] = last_week_pod_chores if last_week_pod_chores is not None else []
        self.pod_restriction: dict[str, bool] = _initialize_restrictions(pod_chores)
        super().__init__(first_name, last_name, chorelist)

    def update_pod_restrictions(self, pod_restriction_list: list[Chore]) -> None:
        self.pod_restriction = update_restrictions_for_list(self.pod_restriction, pod_restriction_list)


def _initialize_restrictions(chore_list: ChoreList) -> dict[str, bool]:
    restriction_list: dict[str, bool] = {}
    for chore in chore_list.getChores():
        restriction_list[chore.get_name()] = False
    return restriction_list


def update_restrictions_for_list(restrictions: dict[str, bool], restrictions_list: list[Chore]) -> dict[str, bool]:
    chore_names = {chore.get_name() for chore in restrictions_list}
    keys_to_delete = [key for key in restrictions if key not in chore_names]
    for key in keys_to_delete:
        del restrictions[key]
    for chore in restrictions_list:
        if chore.get_name() not in restrictions:
            restrictions[chore.get_name()] = False
    return restrictions


def restrictions(restrictions: dict[str, bool], restrictions_list: list[Chore]) -> dict[str, bool]:
    for chore in restrictions:
        if chore in restrictions_list and restrictions[chore] == False:
            restrictions[chore] = True
    return restrictions


def add_last_week_to_restrictions(
    restriction_list: dict[str, bool],
    last_week_chore_list: list[Chore]
) -> dict[str, bool]:
    num_chores: int = len(restriction_list)
    num_restrictions: int = sum(restriction_list.values())
    temp_restriction: dict[str, bool] = restriction_list.copy()
    last_week_names = [chore.get_name() for chore in last_week_chore_list]
    for chore in restriction_list:
        if num_restrictions + 1 == num_chores:
            break
        if chore in last_week_names:
            temp_restriction[chore] = True
            num_restrictions += 1
    return temp_restriction