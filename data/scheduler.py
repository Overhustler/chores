
from random import random


class Scheduler:

    @staticmethod
    def make_chore_list(residents, chore_list):
        return Scheduler.assign_chores(residents, chore_list)

    @staticmethod
    def build_available_chores(residents, chore_list):
        people_available_for_chore = {}
        for chore in chore_list.getChores():
            for resident in residents:
                if resident.resident_restriction.get(chore.get_name(), False) == False:
                    if chore.get_name() not in people_available_for_chore:
                        people_available_for_chore[chore.get_name()] = []
                    people_available_for_chore[chore.get_name()].append(resident)
        return people_available_for_chore
    
    @staticmethod
    def assign_chores(residents, chore_list):
        people_available_for_chore = Scheduler.build_available_chores(residents, chore_list)
        assignment_order = sorted(people_available_for_chore, key=lambda chore: len(people_available_for_chore[chore]))
        chore_assignments = {}
        has_chore = {resident: 0 for resident in residents}
        num_assigned = 0
        total_chores = len(chore_list.getChores())
        for chore in assignment_order:
            available_people = people_available_for_chore[chore]
            random.shuffle(available_people)
            assigned = False
            for person in available_people:
                if has_chore[person] == 0: # Change
                    chore_assignments[chore] = person
                    has_chore[person] += 1
                    num_assigned += 1
                    assigned = True
                    break
            if not assigned:
                for person_second_try in available_people:
                        if has_chore[person_second_try] == 1: # Change
                            chore_assignments[chore] = person_second_try
                            has_chore[person_second_try] += 1
                            num_assigned += 1
                            break
        return chore_assignments



            