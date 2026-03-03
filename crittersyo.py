# Ahcene amara
# 26/3/3

import random

class Critter(object):
    """A virtual pet with traits and turn-based combat (100 HP scale)."""
    def __init__(self, name, hunger=0, boredom=0, personality=None, strength=5, agility=5, defense=5):
        self.name = name
        self.hunger = hunger
        self.boredom = boredom
        self.personality = personality or ("Balanced", {"STR": 0, "AGI": 0, "DEF": 0}, "Well-rounded with no strong biases.")
        self.strength = max(1, strength)
        self.agility = max(1, agility)
        self.defense = max(1, defense)
        self.max_hp = 100
        self.hp = self.max_hp

    def __pass_time(self):
        self.hunger += 1
        self.boredom += 1

    @property
    def mood(self):
        unhappiness = self.hunger + self.boredom
        if unhappiness < 5:
            m = "happy"
        elif 5 <= unhappiness <= 10:
            m = "okay"
        elif 11 <= unhappiness <= 15:
            m = "frustrated"
        else:
            m = "mad"
        return m

    def talk(self):
        print("I'm {self.name}, a {self.personality[0]} critter. I feel {self.mood} now.\n")
        self.__pass_time()

    def eat(self, food=4):
        print("Burp, thank you!")
        self.hunger -= food
        if self.hunger < 0:
            self.hunger = 0
        self.hp = min(self.max_hp, self.hp + random.randint(1, 3))
        self.__pass_time()

    def play(self, fun=4):
        print("Wee!")
        self.boredom -= fun
        if self.boredom < 0:
            self.boredom = 0
        if self.hp > 1 and random.random() < 0.2:
            self.hp = max(1, self.hp - random.randint(1, 2))
        self.__pass_time()

    def rest(self):
        print("{self.name} takes a nap...")
        self.hp = min(self.max_hp, self.hp + random.randint(8, 14))
        self.boredom = max(0, self.boredom - 2)
        self.__pass_time()

    def stats(self):
        trait_name, mods, desc = self.personality
        print("— {self.name} —")
        print("Trait: {trait_name} ({desc})  Mods: {mods}")
        print("HP: {self.hp}/{self.max_hp}")
        print("STR: {self.strength}  AGI: {self.agility}  DEF: {self.defense}")
        print("Hunger: {self.hunger}  Boredom: {self.boredom}  Mood: {self.mood}")
        print()

    def _mood_mods(self):
        if self.mood == "happy":
            return {"STR": 0, "AGI": 1, "DEF": 0}
        elif self.mood == "okay":
            return {"STR": 0, "AGI": 0, "DEF": 0}
        elif self.mood == "frustrated":
            return {"STR": 1, "AGI": -1, "DEF": 0}
        else:  # mad
            return {"STR": 2, "AGI": -1, "DEF": 0}

    def _attack_roll(self, defender):
        """
        Random damage within a range; crit = max damage + bonus.
        """
        # Attacker with mood
        mood = self._mood_mods()
        att_str = max(1, self.strength + mood["STR"])
        att_agi = max(1, self.agility + mood["AGI"])

        # Defender with mood
        def_mood = defender._mood_mods()
        def_def = max(1, defender.defense + def_mood["DEF"])
        def_agi = max(1, defender.agility + def_mood["AGI"])

        # Dodge
        dodge_chance = min(0.35, 0.05 + def_agi * 0.02)
        if random.random() < dodge_chance:
            return 0, True

        # Build range from STR vs DEF (100 HP feel)
        delta = (att_str * 1.4) - (def_def * 1.0)
        center = 12 + delta * 1.2
        width  = 6 + max(0, abs(delta)) * 0.6

        raw_min = center - width / 2
        raw_max = center + width / 2

        # Slight natural variance to edges
        raw_min -= random.uniform(0.0, 1.5)
        raw_max += random.uniform(0.0, 1.5)

        # Clamp the normal hit band
        min_dmg = max(3, int(round(raw_min)))
        max_dmg = min(28, int(round(raw_max)))
        if max_dmg < min_dmg:
            max_dmg = min_dmg

        # Crits: max + bonus
        crit_chance = min(0.25, 0.05 + att_agi * 0.015)
        is_crit = random.random() < crit_chance
        if is_crit:
            bonus_pct = random.uniform(0.20, 0.40)  # 20–40% of max
            dmg = int(round(max_dmg + max(2, max_dmg * bonus_pct)))
        else:
            dmg = random.randint(min_dmg, max_dmg)

        # Fatigue penalty from hunger+boredom
        fatigue = self.hunger + self.boredom
        fatigue_mult = 1.0 - min(0.35, fatigue / 60.0)
        dmg = max(1, int(round(dmg * fatigue_mult)))

        # Final clamps: allow bigger spikes only on crits
        dmg = max(3, min(40 if is_crit else 28, dmg))
        return dmg, ("CRIT" if is_crit else False)

    def fight(self, opponent):
        print("\n{self.name} ({self.personality[0]}) vs {opponent.name} ({opponent.personality[0]}) — FIGHT!")
        print("{self.name} HP {self.hp}/{self.max_hp}   |   {opponent.name} HP {opponent.hp}/{opponent.max_hp}\n")

        # Initiative by agility (tie-break with random)
        first, second = (self, opponent) if (self.agility, random.random()) > (opponent.agility, random.random()) else (opponent, self)

        round_no = 1
        while self.hp > 0 and opponent.hp > 0:
            print("— Round {round_no} —")
            for attacker, defender in [(first, second), (second, first)]:
                if attacker.hp <= 0 or defender.hp <= 0:
                    break
                dmg, special = attacker._attack_roll(defender)
                if special is True:
                    print("{defender.name} dodged {attacker.name}'s attack!")
                else:
                    label = " (CRIT!)" if special == "CRIT" else ""
                    defender.hp = max(0, defender.hp - dmg)
                    print("{attacker.name} hits {defender.name} for {dmg}{label}. {defender.name} HP: {defender.hp}/{defender.max_hp}")

                attacker.__pass_time()
                defender.__pass_time()

                if defender.hp <= 0:
                    print("\n{attacker.name} wins! (attacker mood: {attacker.mood})")
                    attacker.hp = min(attacker.max_hp, attacker.hp + random.randint(6, 12))
                    return attacker

            round_no += 1

        winner = self if self.hp > 0 else opponent
        print("\n{winner.name} wins!")
        return winner


PERSONALITIES = {
    "Aggressive": ({"STR": +2, "AGI": 0, "DEF": -1}, "Hits hard but leaves openings."),
    "Nimble":     ({"STR": -1, "AGI": +2, "DEF": 0}, "Quick on their feet; harder to hit."),
    "Sturdy":     ({"STR": 0, "AGI": -1, "DEF": +2}, "Tough shell; soaks damage."),
    "Clever":     ({"STR": 0, "AGI": +1, "DEF": +1}, "Balanced and opportunistic."),
    "Rowdy":      ({"STR": +1, "AGI": +1, "DEF": -1}, "Chaotic energy, risky swings."),
    "Balanced":   ({"STR": 0, "AGI": 0, "DEF": 0}, "Well-rounded with no strong biases.")
}

def create_random_critter(name=None):
    if name is None or not name.strip():
        name = "Critter{random.randint(1000, 9999)}"

    # Base stats with mild variance
    base = {
        "STR": 5 + random.randint(-1, 1),
        "AGI": 5 + random.randint(-1, 1),
        "DEF": 5 + random.randint(-1, 1)
    }

    trait_name, (mods, desc) = random.choice(list(PERSONALITIES.items()))
    strength = max(1, base["STR"] + mods["STR"])
    agility  = max(1, base["AGI"] + mods["AGI"])
    defense  = max(1, base["DEF"] + mods["DEF"])
    personality = (trait_name, mods, desc)

    c = Critter(name=name, personality=personality,
                strength=strength, agility=agility, defense=defense)
    c.hp = c.max_hp
    return c

def choose_critter(critters, prompt="Choose a critter by number: "):
    if not critters:
        print("No critters yet.\n")
        return None
    for i, c in enumerate(critters, start=1):
        print("{i}) {c.name} — {c.personality[0]}  HP {c.hp}/{c.max_hp}")
    try:
        idx = int(input(prompt))
        if 1 <= idx <= len(critters):
            return critters[idx - 1]
    except ValueError:
        pass
    print("Invalid choice.\n")
    return None


def main():
    # Start with one critter named by the user
    crit_name = input("what do you want to name your critter? ")
    first = create_random_critter(crit_name)
    critters = [first]

    choice = None
    while choice != "0":
        print("""
        
        Critter caretaker

        0 - quit
        1 - Listen to a critter
        2 - Feed a critter
        3 - Play with a critter
        4 - Show all critters & stats
        5 - Add a new random critter
        6 - Make two critters fight
        7 - Let a critter rest
        
        """)

        choice = input("choice: ").strip()
        print()

        if choice == "0":
            print("good bye.")

        elif choice == "1":
            c = choose_critter(critters, "Which critter to listen to? ")
            if c:
                c.talk()

        elif choice == "2":
            c = choose_critter(critters, "Which critter to feed? ")
            if c:
                try:
                    amt = int(input("How much food? (default 4): ") or "4")
                except ValueError:
                    amt = 4
                c.eat(amt)

        elif choice == "3":
            c = choose_critter(critters, "Which critter to play with? ")
            if c:
                try:
                    amt = int(input("How much play? (default 4): ") or "4")
                except ValueError:
                    amt = 4
                c.play(amt)

        elif choice == "4":
            if not critters:
                print("No critters yet.\n")
            else:
                for c in critters:
                    c.stats()

        elif choice == "5":
            name = input("Name your new critter (blank for random): ")
            new_c = create_random_critter(name)
            critters.append(new_c)
            print("Created {new_c.name} — {new_c.personality[0]} with HP {new_c.hp} (STR {new_c.strength}, AGI {new_c.agility}, DEF {new_c.defense})\n")

        elif choice == "6":
            if len(critters) < 2:
                print("You need at least two critters to fight.\n")
            else:
                print("Choose attacker:")
                a = choose_critter(critters)
                if not a:
                    continue
                print("Choose defender:")
                remaining = [c for c in critters if c is not a]
                b = choose_critter(remaining)
                if not b:
                    continue
                a.fight(b)

        elif choice == "7":
            c = choose_critter(critters, "Which critter should rest? ")
            if c:
                c.rest()

        else:
            print("\nSorry, but", choice, "isn't a valid choice.")

if __name__ == "__main__":
    main()