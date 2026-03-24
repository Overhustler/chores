

class Resident:
    def __init__(self, first_name, last_name, chorelist, last_week_chores=None):
        self.first_name = first_name
        self.last_name = last_name
        self.resident_restriction = _initialize_restrictions(chorelist)
        self.last_week_chore_list = last_week_chores if last_week_chores is not None else []

    def getDisplayName(self):
        return self.first_name + " " + self.last_name[0] + "."

    def set_last_week_chore_list(self, last_week):
        self.last_week_chore_list = last_week

    def get_last_week_chore_list(self):
        return self.last_week_chore_list  

    def restrictions_including_last_week(self):
        return add_last_week_to_restrictions(self.resident_restriction, self.last_week_chore_list)
    

    
class Singles(Resident):
    def __init__(self, first_name, last_name, chorelist, bed_number):
        self.bed_number = bed_number
        super().__init__(first_name, last_name, chorelist)

class FamilyResident(Resident):
    def __init__(self, first_name, last_name, chorelist, pod_number, room_number, last_week_pod_chores, pod_chores):
        self.pod_number = pod_number
        self.room_number = room_number
        self.last_week_pod_chores = last_week_pod_chores if last_week_pod_chores is not None else []
        self.pod_restriction = _initialize_restrictions(pod_chores)
        super().__init__(first_name, last_name, chorelist)
    
    def update_pod_restrictions(self, pod_restriction_list):
        self.pod_restriction = update_restrictions_for_list(self.pod_restriction, pod_restriction_list)

def _initialize_restrictions(chore_list):
    restriction_list = {}
    for chore in chore_list.getChores():
        restriction_list[chore.get_name()] = False
    return restriction_list

def update_restrictions_for_list(restrictions, restrictions_list):
    for chore in restrictions:
        if chore.name not in restrictions_list:
            del restrictions[chore.name]
    for chore.name in restrictions_list:
        if chore not in restrictions:
            restrictions[chore.name] = False
    return restrictions

def restrictions(restrictions, restrictions_list):
    for chore in restrictions: 
        if chore in restrictions_list and restrictions[chore] == False:
            restrictions[chore] = True
    return restrictions

def add_last_week_to_restrictions(restriction_list, last_week_chore_list):
    num_chores = len(restriction_list)
    num_restrictions = sum(restriction_list.values())
    temp_restriction = restriction_list.copy()
    for chore in restriction_list:
        if num_restrictions + 1 == num_chores:
            break
        if chore in last_week_chore_list:
            temp_restriction[chore] = True
            num_restrictions += 1
    return temp_restriction 