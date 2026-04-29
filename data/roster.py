from choreList import Chore, ChoreList
from resident import Resident
from scheduler import Scheduler

class Roster:
    def __init__(
        self,
        residents: list[Resident] | None = None,
        ChoreList: ChoreList | None = None
    ) -> None:
        self.residents: list[Resident] = list(residents) if residents is not None else []
        self.ChoreList: ChoreList = ChoreList if ChoreList is not None else [] # type: ignore
        self.scheduler: Scheduler = Scheduler()

    def add_resident(self, resident: Resident) -> None:
        self.residents.append(resident)

    def remove_resident(self, resident: Resident) -> None:
        self.residents.remove(resident)

    def update_resident_list(self, resident_list: list[Resident]) -> None:
        for resident in self.residents.copy():
            if resident not in resident_list:
                self.remove_resident(resident)
        for resident in resident_list:
            if resident not in self.residents:
                self.add_resident(resident)

    def update_chore_list(self, ChoreList: ChoreList) -> None:
        update_a_chore_or_pod_list(self, ChoreList)


class FamilyRoster(Roster):
    def __init__(
        self,
        residents: list[Resident] | None = None,
        ChoreList: ChoreList | None = None,
        pod_chore_list: ChoreList | None = None,
        pods: list | None = None
    ) -> None:
        self.pod_chore_list: ChoreList | None = pod_chore_list # type: ignore
        self.pods: list = pods if pods is not None else []
        super().__init__(residents, ChoreList)

    def update_pod_chore_list(self, pod_chore_list: ChoreList) -> None:
        update_a_chore_or_pod_list(self, pod_chore_list)


def assign_chores(roster: Roster) -> None:
    reset_chores(roster)

    c_list: dict[str, Resident] = roster.scheduler.make_chore_list(roster.residents, roster.ChoreList)

    for chore in roster.ChoreList.getChores():
        if chore.get_name() in c_list:
            chore.set_person_assigned(c_list[chore.get_name()])


def reset_chores(roster: Roster) -> None:
    temp_last_week_chore_list: dict[Resident, list[Chore]] = {resident: [] for resident in roster.residents}

    for chore in roster.ChoreList.getChores():
        person = chore.get_person_assigned()
        if person is not None:
            temp_last_week_chore_list[person].append(chore)

    for resident in roster.residents:
        resident.set_last_week_chore_list(temp_last_week_chore_list[resident])

    for chore in roster.ChoreList.getChores():
        chore.set_person_assigned(None)


def update_a_chore_or_pod_list(roster: Roster, chore_list: ChoreList) -> None:
    existing_chores = roster.ChoreList.getChores()
    new_chores = chore_list.getChores()
    
    for chore in new_chores:
        if chore not in existing_chores:
            roster.ChoreList.add_chore(chore.get_name(), chore.get_time())
    for chore in existing_chores:
        if chore not in new_chores:
            roster.ChoreList.remove_chore(chore)
    for resident in roster.residents:
        resident.update_restrictions(chore_list.getChores()) # type: ignore
    
