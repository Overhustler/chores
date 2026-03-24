from data.choreList  import ChoreList, chore_resident_restriction

def main():
    chore_list = ChoreList("male_chores", "choreTest.txt")
    resident_one_ristriction_list = chore_list.chore_resident_restriction("resident_one_restriction_list", chore_list.getChores(), {})
    resident_one_ristriction_list

if __name__ == "__main__":
    main()