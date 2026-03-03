# Ahcene amara
# 26/3/3

class Critter (object):
    """A Virtual pet"""
    def __init__(self,name , hunger = 0, boredom = 0):
        self.name = name
        self.hunger = hunger
        self.boredom = boredom

    def __pass_time(self):
        self.hunger += 1
        self.boredom += 1 

    @property
    def mood(self):
        unhappiness = self.hunger + self.boredom
        if unhappiness <5:
            m = "happy"
        elif 5<= unhappiness <= 10:
            m = "okay"
        elif 11 <= unhappiness <= 15:
            m = "frustrated"
        else:
            m = "mad"
        return m
    
    def talk(self):
        print("im", self.name, "and i feel", self.mood, "now.\n")
        self.__pass_time()

    def eat(self, food = 4):
        print("burp, thank you")
        self.hunger -= food
        if self.hunger <0:
            self.hunger = 0
        self.__pass_time()

    def play(self, fun = 4):
        print("wee!")
        self.boredom -= fun
        if self.boredom <0:
            self.boredom = 0
        self.__pass_time()

def main():
    crit_name = input("what do you want to name your critter? ") 
    crit = Critter(crit_name) 

    choice = None
    while choice != "0":
        print("""
        
        Critter caretaker

        0 - quit
        1 - Listen to your critter 
        2 - Feed your critter
        3 - Play with your critter
        
        """)

        choice = input("choice: ")
        print()

        if choice == "0":
            print("good bye. ")
        
        elif choice == "1":
            crit.talk()

        elif choice == "2":
            crit.eat()    

        elif choice == "3":
            crit.play()
        
        else:
            print("\nSorry, but", choice, "isnt a valid choice.")
 
main()
    
