import random
from choreList import ChoreList
from resident import Resident


class Scheduler:

    @staticmethod
    def make_chore_list(residents: list[Resident], chore_list: ChoreList) -> dict[str, Resident]:
        return Scheduler.assign_chores(residents, chore_list)

    @staticmethod
    def build_available_chores(residents: list[Resident], chore_list: ChoreList) -> dict[str, list[Resident]]:
        people_available_for_chore: dict[str, list[Resident]] = {}
        for chore in chore_list.getChores():
            for resident in residents:
                if resident.resident_restriction.get(chore.get_name(), False) == False:
                    if chore.get_name() not in people_available_for_chore:
                        people_available_for_chore[chore.get_name()] = []
                    people_available_for_chore[chore.get_name()].append(resident)
        return people_available_for_chore

    @staticmethod
    def assign_chores(residents: list[Resident], chore_list: ChoreList) -> dict[str, Resident]:
        people_available_for_chore: dict[str, list[Resident]] = Scheduler.build_available_chores(residents, chore_list)
        assignment_order: list[str] = sorted(people_available_for_chore, key=lambda chore: len(people_available_for_chore[chore]))
        chore_assignments: dict[str, Resident] = {}
        has_chore: dict[Resident, int] = {resident: 0 for resident in residents}
        num_assigned: int = 0
        total_chores: int = len(chore_list.getChores())
        max_chores_per_person: int = -(-total_chores // len(residents))  # ceiling division

        for chore in assignment_order:
            available_people: list[Resident] = people_available_for_chore[chore]
            random.shuffle(available_people)
            for threshold in range(max_chores_per_person):
                for person in available_people:
                    if has_chore[person] == threshold:
                        chore_assignments[chore] = person
                        has_chore[person] += 1
                        num_assigned += 1
                        break
                if chore in chore_assignments:
                    break
            if num_assigned == total_chores:
                return chore_assignments

        return chore_assignments
            