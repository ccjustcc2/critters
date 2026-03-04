import random

def print_box(title, lines, width=50):
    print("┌" + "─" * (width - 2) + "┐")
    if title:
        title_str = f" {title} "
        print("│" + title_str.center(width - 2) + "│")
        print("├" + "─" * (width - 2) + "┤")
    for line in lines:
        print("│ " + line.ljust(width - 4) + " │")
    print("└" + "─" * (width - 2) + "┘")

MOVES = {
    "Strike": {"type": "physical", "power": 12, "cost": 0},
    "Power Slam": {"type": "physical", "power": 20, "cost": 0},
    "Quick Jab": {"type": "physical", "power": 10, "cost": 0},
    "Fireball": {"type": "magic", "power": 18, "cost": 10},
    "Arcane Blast": {"type": "magic", "power": 25, "cost": 15},
}

PERSONALITY_MOVES = {
    "Aggressive": ["Strike", "Power Slam"],
    "Nimble": ["Quick Jab", "Strike"],
    "Sturdy": ["Strike", "Power Slam"],
    "Clever": ["Fireball", "Arcane Blast"],
    "Rowdy": ["Strike", "Fireball"],
    "Balanced": ["Strike", "Fireball"],
}

PERSONALITIES = {
    "Aggressive": ({"STR": +2, "AGI": 0, "DEF": -1, "INT": 0}, "Hits hard."),
    "Nimble":     ({"STR": -1, "AGI": +2, "DEF": 0, "INT": 0}, "Fast."),
    "Sturdy":     ({"STR": 0, "AGI": -1, "DEF": +2, "INT": 0}, "Tanky."),
    "Clever":     ({"STR": 0, "AGI": 0, "DEF": 0, "INT": +2}, "Mage."),
    "Rowdy":      ({"STR": +1, "AGI": +1, "DEF": -1, "INT": 0}, "Wild."),
    "Balanced":   ({"STR": 0, "AGI": 0, "DEF": 0, "INT": 0}, "Neutral."),
}

class Critter(object):
    def __init__(self, name, hunger=0, boredom=0,
                 personality=None, strength=5, agility=5,
                 defense=5, intelligence=5):
        self.name = name
        self.hunger = hunger
        self.boredom = boredom
        self.personality = personality or (
            "Balanced", {"STR": 0, "AGI": 0, "DEF": 0, "INT": 0}, "Well-rounded."
        )
        self.strength = max(1, strength)
        self.agility = max(1, agility)
        self.defense = max(1, defense)
        self.intelligence = max(1, intelligence)
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mana = 30 + (self.intelligence * 5)
        self.mana = self.max_mana
        self.level = 1
        self.xp = 0
        self.xp_to_next = 20
        self.moves = PERSONALITY_MOVES[self.personality[0]]

    def _pass_time(self):
        self.hunger += 1
        self.boredom += 1

    @property
    def mood(self):
        unhappiness = self.hunger + self.boredom
        if unhappiness < 5:
            return "happy"
        elif unhappiness <= 10:
            return "okay"
        elif unhappiness <= 15:
            return "frustrated"
        return "mad"

    def talk(self):
        print(f"\nI'm {self.name}, a {self.personality[0]} critter. I feel {self.mood}.")
        self._pass_time()

    def eat(self, food=4):
        print("\nBurp, thank you!")
        self.hunger = max(0, self.hunger - food)
        self.hp = min(self.max_hp, self.hp + random.randint(1, 3))
        self._pass_time()

    def play(self, fun=4):
        print("\nWee!")
        self.boredom = max(0, self.boredom - fun)
        self._pass_time()

    def rest(self):
        print(f"\n{self.name} takes a nap...")
        self.hp = min(self.max_hp, self.hp + random.randint(8, 14))
        self.mana = min(self.max_mana, self.mana + random.randint(5, 10))
        self.boredom = max(0, self.boredom - 2)
        self._pass_time()

    def stats(self):
        trait_name, mods, desc = self.personality
        lines = [
            f"Trait: {trait_name} ({desc})",
            f"Level: {self.level}  XP: {self.xp}/{self.xp_to_next}",
            f"HP: {self.hp}/{self.max_hp}",
            f"Mana: {self.mana}/{self.max_mana}",
            "",
            f"STR: {self.strength}  AGI: {self.agility}",
            f"DEF: {self.defense}  INT: {self.intelligence}",
            "",
            f"Hunger: {self.hunger}",
            f"Boredom: {self.boredom}",
            f"Mood: {self.mood}"
        ]
        print_box(self.name.upper(), lines)

    def gain_xp(self, amount):
        print(f"\n{self.name} gains {amount} XP!")
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next = int(self.xp_to_next * 1.5)
        str_gain = random.randint(1, 2)
        agi_gain = random.randint(1, 2)
        def_gain = random.randint(1, 2)
        int_gain = random.randint(1, 2)
        self.strength += str_gain
        self.agility += agi_gain
        self.defense += def_gain
        self.intelligence += int_gain
        hp_gain = random.randint(5, 10)
        self.max_hp += hp_gain
        self.hp = self.max_hp
        self.max_mana += int_gain * 5
        self.mana = self.max_mana
        print_box("LEVEL UP!", [
            f"{self.name} reached Level {self.level}!",
            f"+{str_gain} STR  +{agi_gain} AGI",
            f"+{def_gain} DEF  +{int_gain} INT",
            f"+{hp_gain} Max HP"
        ])

    def fight(self, opponent, ai_opponent=False):
        print_box("BATTLE START!", [f"{self.name}  VS  {opponent.name}"])
        self.hp = self.max_hp
        opponent.hp = opponent.max_hp
        self.mana = self.max_mana
        opponent.mana = opponent.max_mana
        attacker, defender = (
            (self, opponent)
            if self.agility >= opponent.agility
            else (opponent, self)
        )
        while self.hp > 0 and opponent.hp > 0:
            print_box(
                f"{attacker.name}'s TURN",
                [
                    f"HP: {attacker.hp}/{attacker.max_hp}",
                    f"Mana: {attacker.mana}/{attacker.max_mana}",
                    "",
                    f"Enemy: {defender.name}",
                    f"Enemy HP: {defender.hp}/{defender.max_hp}"
                ],
                width=60
            )
            move_lines = []
            for i, move in enumerate(attacker.moves, 1):
                m = MOVES[move]
                move_lines.append(f"{i}) {move} (Cost: {m['cost']})")
            print_box("CHOOSE MOVE", move_lines, width=60)
            if ai_opponent and attacker == opponent:
                move_name = choose_ai_move(attacker, defender)
                print(f"AI chooses {move_name}!")
            else:
                try:
                    choice = int(input("Select move: ")) - 1
                    move_name = attacker.moves[choice]
                except:
                    print("Invalid choice.")
                    continue
            move = MOVES[move_name]
            if attacker.mana < move["cost"]:
                print("Not enough mana!")
                continue
            attacker.mana -= move["cost"]
            base_power = move.get("power", 5)
            if move["type"] == "physical":
                damage = base_power + attacker.strength * 2
            else:
                damage = base_power + attacker.intelligence * 2
            damage -= defender.defense
            damage = max(3, damage)
            dodge_chance = defender.agility * 0.015
            if random.random() < dodge_chance:
                print(f"\n{defender.name} dodged the attack!")
                attacker, defender = defender, attacker
                continue
            crit_chance = attacker.agility * 0.02
            if random.random() < crit_chance:
                damage *= 2
                print("CRITICAL HIT!")
            hits = 1
            extra_hit_chance = attacker.agility * 0.02
            if random.random() < extra_hit_chance:
                hits += 1
            if random.random() < extra_hit_chance * 0.5:
                hits += 1
            if random.random() < extra_hit_chance * 0.25:
                hits += 1
            hits = min(hits, 3)
            total_damage = 0
            for _ in range(hits):
                defender.hp = max(0, defender.hp - damage)
                total_damage += damage
            print(f"\n{attacker.name} uses {move_name}!")
            print(f"It hits {hits} time(s) for {total_damage} total damage!")
            if defender.hp <= 0:
                print_box("VICTORY!", [f"{attacker.name} wins!"])
                attacker.gain_xp(15)
                defender.gain_xp(5)
                return attacker
            attacker, defender = defender, attacker

def choose_ai_move(ai, enemy):
    trait = ai.personality[0]
    if trait == "Aggressive":
        return max(ai.moves, key=lambda m: MOVES[m]["power"])
    elif trait == "Clever":
        magic_moves = [m for m in ai.moves if MOVES[m]["type"] == "magic" and ai.mana >= MOVES[m]["cost"]]
        if magic_moves:
            return max(magic_moves, key=lambda m: MOVES[m]["power"])
        return ai.moves[0]
    elif trait == "Sturdy":
        affordable = [m for m in ai.moves if ai.mana >= MOVES[m]["cost"]]
        return affordable[0] if affordable else ai.moves[0]
    elif trait == "Nimble":
        return random.choice(ai.moves)
    elif trait == "Rowdy":
        physical = [m for m in ai.moves if MOVES[m]["type"] == "physical"]
        if physical:
            return random.choice(physical)
        return random.choice(ai.moves)
    else:
        affordable = [m for m in ai.moves if ai.mana >= MOVES[m]["cost"]]
        return random.choice(affordable) if affordable else ai.moves[0]

def create_random_critter(name=None):
    if not name or not name.strip():
        name = f"Critter{random.randint(1000,9999)}"
    base = {k: 5 + random.randint(-1, 1) for k in ["STR", "AGI", "DEF", "INT"]}
    trait_name, (mods, desc) = random.choice(list(PERSONALITIES.items()))
    return Critter(
        name,
        personality=(trait_name, mods, desc),
        strength=max(1, base["STR"] + mods["STR"]),
        agility=max(1, base["AGI"] + mods["AGI"]),
        defense=max(1, base["DEF"] + mods["DEF"]),
        intelligence=max(1, base["INT"] + mods["INT"]),
    )

def choose_critter(critters, prompt="Choose: "):
    if not critters:
        return None
    lines = []
    for i, c in enumerate(critters, 1):
        lines.append(f"{i}) {c.name}  | Lv {c.level} | HP {c.hp}/{c.max_hp}")
    print_box("SELECT CRITTER", lines)
    try:
        index = int(input(prompt)) - 1
        if 0 <= index < len(critters):
            return critters[index]
    except:
        pass
    print("Invalid choice.\n")
    return None

def main():
    critters = [create_random_critter(input("Name your critter: "))]
    while True:
        print_box("MAIN MENU", [
            "1) Talk",
            "2) Feed",
            "3) Play",
            "4) Stats",
            "5) New Critter",
            "6) Fight (Player vs AI)",
            "7) Rest",
            "0) Quit"
        ])
        choice = input("Choice: ")
        if choice == "0":
            break
        elif choice == "1":
            c = choose_critter(critters)
            if c: c.talk()
        elif choice == "2":
            c = choose_critter(critters)
            if c: c.eat()
        elif choice == "3":
            c = choose_critter(critters)
            if c: c.play()
        elif choice == "4":
            for c in critters:
                c.stats()
        elif choice == "5":
            critters.append(create_random_critter(input("Name: ")))
        elif choice == "6":
            if len(critters) < 2:
                ai_critter = create_random_critter(f"AI_{random.randint(100,999)}")
                player = choose_critter(critters, "Attacker: ")
                if player:
                    player.fight(ai_critter, ai_opponent=True)
            else:
                a = choose_critter(critters, "Attacker: ")
                if not a: continue
                b_candidates = [c for c in critters if c != a]
                b = random.choice(b_candidates)
                a.fight(b, ai_opponent=True)
        elif choice == "7":
            c = choose_critter(critters)
            if c: c.rest()

if __name__ == "__main__":
    main()