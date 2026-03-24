class ChoreList:
    def __init__(self, name, chores_file):
        self.name = name
        self.chores = self._create_chores(chores_file)

    def _create_chores(self, chores_file):
        chores = []
        with open(chores_file, 'r') as file:
            for line in file:
                name, time = line.strip().split(',')
                chores.append(Chore(name, time))
        return chores
        
    def getChores(self):       
        return self.chores
    
    def add_chore(self, name, time):
        self.chores.append(Chore(name, time))

    def remove_chore(self, chore):
        self.chores.remove(chore)

class Chore:
    def __init__(self, name, time, person_assigned=None):
        self._name = name
        self._time = time
        self._person_assigned = person_assigned

    def set_name(self, name):
        self._name = name
    def get_name(self):
        return self._name
    
    def set_time(self, time):
        self._time = time
    def get_time(self):
        return self._time
    
    def get_person_assigned(self):
        return self._person_assigned
    def set_person_assigned(self, person_assigned):
        self._person_assigned = person_assigned