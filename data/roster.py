from scheduler import Scheduler

class Roster:
    def __init__(self, residents=None, ChoreList=None):
        self.residents = residents if residents is not None else []
        self.ChoreList = ChoreList if ChoreList is not None else []
        self.scheduler = Scheduler()
    def add_resident(self, resident):
        self.residents.append(resident)

    def remove_resident(self, resident):
        self.residents.remove(resident)

    def update_resident_list(self, resident_list):
        for resident in self.residents:
            if resident not in resident_list:
                self.remove_resident(resident)
        for resident in resident_list:
            if resident not in self.residents:
                self.add_resident(resident)

    def update_chore_list(self, ChoreList):
        update_a_chore_or_pod_list(self, ChoreList)

class familyRoster(Roster):
    def __init__(self, residents=None, ChoreList=None, pod_chore_list=None, pods=None):
        self.pod_chore_list = pod_chore_list if pod_chore_list is not None else []
        self.pods = pods if pods is not None else []
        super().__init__(residents, ChoreList) 

    def update_pod_chore_list(self, pod_chore_list):
        update_a_chore_or_pod_list(self, pod_chore_list)
    
def assign_chores(roster):
    reset_chores(roster)

    c_list =  roster.scheduler.make_chore_list(roster.residents, roster.ChoreList)

    for chore in roster.ChoreList.getChores():
        if chore.get_name() in c_list:
            chore.set_person_assigned(c_list[chore.get_name()])


def reset_chores(roster):
    temp_last_week_chore_list = {}

    for chore in roster.ChoreList.getChores():
        if chore.get_person_assigned() not in temp_last_week_chore_list:
            temp_last_week_chore_list[chore.get_person_assigned()] = chore.get_name()
        else:
            temp_last_week_chore_list[chore.get_person_assigned()].append(chore.get_name())

    for resident in roster.residents:
        resident.set_last_week_chore_list(temp_last_week_chore_list[resident])

    for chore in roster.ChoreList.getChores():
        chore.set_person_assigned(None)

def update_a_chore_or_pod_list(roster, choreList):
        for chore in choreList.getChores():
            if chore not in choreList.getChores():
                choreList.add_chore(chore)
        for chore in choreList.getChores():
            if chore not in choreList.getChores():
                choreList.remove_chore(chore)
        for resident in roster.residents:
            resident.update_restrictions(choreList.getChores())
