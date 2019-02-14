from dataclasses import dataclass
from enum import Enum
import heapq
from itertools import chain
import re

class Team(Enum):
    IMMUNE = 0
    INFECTION = 1

class AttackType(Enum):
    FIRE = 0
    BLUDGEONING = 1
    SLASHING = 2
    COLD = 3
    RADIATION = 4

@dataclass(frozen=True)
class Attack:
    kind: AttackType
    damage: int

@dataclass(frozen=True)
class Unit:
    hitpoints: int
    immunity: set
    weakness: set
    attack: Attack

@dataclass(unsafe_hash=True)
class Group:
    kind: Team
    unit: Unit
    initiative: int
    count: int
    gid: int = -1

    def effective_power(self):
        return self.unit.attack.damage * self.count

    def damage_taken(self, attacker):
        if attacker.unit.attack.kind in self.unit.immunity:
            return 0

        base_damage = attacker.effective_power()
        if attacker.unit.attack.kind in self.unit.weakness:
            return base_damage * 2

        return base_damage

    def attack(self, defender):
        damage = defender.damage_taken(self)

        killed = damage // defender.unit.hitpoints

        if killed > defender.count:
            killed = defender.count

        defender.count -= killed

        return killed, damage

@dataclass(frozen=True)
class FightRoster:
    attacker: Group
    defender: Group

class Cohort:
    def __init__(self):
        self.groups = []

    def alive(self):
        for group in self.groups:
            if group.count:
                return True

        return False

    def add_group(self, group):
        self.groups.append(group)
        group.gid = len(self.groups) - 1

    def attack_order(self):
        for group in sorted(self.groups, key=lambda x: (x.effective_power(), x.initiative), reverse=True):
            if group.count > 0:
                yield group

    def select_targets(self, defenders):
        taken = set()
        selection = []
        for ag in self.attack_order():
            targets = []
            for tg in defenders.groups:
                if tg.gid not in taken and tg.count > 0:
                    damage = tg.damage_taken(ag)
                    if damage > 0:
                        targets.append((damage, tg.effective_power(), tg.initiative, ag.gid, tg.gid))

            for (damage, _, _, agid, tgid) in sorted(targets, reverse=True):
                if tgid not in taken:
                    taken.add(tgid)
                    selection.append(FightRoster(
                        attacker=self.groups[agid],
                        defender=defenders.groups[tgid]
                    ))
                    break

        return selection

    def info(self):
        total = 0
        for i, group in enumerate(self.groups):
            if group.count > 0:
                total += group.count
                print(f"{group.kind} group {i+1} contains {group.count} units")
        if total > 0:
            print(f"Total remaining units: {total}")

def read_data(filename="data/input24.data"):
    with open(filename) as f:
        return f.read().splitlines()

def attack_type(name):
    return {
        "fire": AttackType.FIRE,
        "bludgeoning": AttackType.BLUDGEONING,
        "slashing": AttackType.SLASHING,
        "cold": AttackType.COLD,
        "radiation": AttackType.RADIATION
    }[name]

def parse_profile(line):
    match = re.search(r"\(([^\)]+)\)", line)
    profile = {}
    if match:
        spec = match.group(1)
        parts = spec.split(";")
        for p in parts:
            part = p.strip()
            for w in {"weak", "immune"}:
                if part.startswith(f"{w} to "):
                    profile[w] = {
                        attack_type(x.strip(" "))
                        for x in p[len(f"{w} to "):].split(",")
                    }

    return profile

def parse_attack(line):
    match = re.search(
        r"with an attack that does (\d+) ([^\s]+) damage at initiative (\d+)", line
    )

    assert match

    (damage, name, initiative) = (int(match.group(1)), match.group(2), int(match.group(3)))

    return Attack(
        kind=attack_type(name),
        damage=damage,
    ), initiative

def parse_troop_strength(line):
    data = list(map(int, re.findall(r"-?\d+", line)))[:-2]
    return {
        "count": data[0],
        "hitpoints": data[1]
    }

def parse_data(lines):
    immune = Cohort()
    infection = Cohort()

    cohort = immune
    team = Team.IMMUNE
    max_initiative = -1
    for line in lines[1:]:
        if line == "":
            continue
        if line == "Infection:":
            cohort = infection
            team = Team.INFECTION
            continue

        profile = parse_profile(line)
        attack, initiative = parse_attack(line)
        troop = parse_troop_strength(line)

        cohort.add_group(Group(
            kind=team,
            unit=Unit(
                hitpoints=troop["hitpoints"],
                immunity=profile.get("immune", set()),
                weakness=profile.get("weak", set()),
                attack=attack
            ),
            initiative=initiative,
            count=troop["count"]
        ))

        if initiative > max_initiative:
            max_initiative = initiative

    return immune, infection, max_initiative

def fight(immune, infection, max_initiative):
    # 1. Select targets.
    immune_targets = immune.select_targets(infection)
    infection_targets = infection.select_targets(immune)

    attack_queue = []

    immune.info()
    infection.info()
    print()

    # 2. Deal damage in (global) decreasing order of initiative
    for roster in chain(infection_targets, immune_targets):
        damage = roster.defender.damage_taken(roster.attacker)  # note: can't cache this!
        print(f"{roster.attacker.kind} group {roster.attacker.gid+1} would deal defending group {roster.defender.gid+1} {damage} damage")
        heapq.heappush(attack_queue, (max_initiative-roster.attacker.initiative, roster.attacker, roster.defender))

    print()

    while attack_queue:
        (_, attacker, defender) = heapq.heappop(attack_queue)

        hp, cx = defender.unit.hitpoints, defender.count

        killed, damage = attacker.attack(defender)

        print(f"{attacker.kind} group {attacker.gid+1} attacks defending group {defender.gid+1}, inflicting {damage} killing {killed} units (was hp: {hp} count: {cx})")


if __name__ == "__main__":

    print()

    # immune, infection, max_initiative = parse_data(read_data("data/test24.data"))

    immune, infection, max_initiative = parse_data(read_data())

    i= 1
    while immune.alive() and infection.alive():
        print(f"------------ FIGHT {i} ------------")
        fight(immune, infection, max_initiative)
        i += 1
        print()

    print(f"------------ WINNER ------------")
    immune.info()
    infection.info()
