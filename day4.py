"""
day 4 of Advent of Code 2018
by Stefan Kruger
"""

from collections import Counter, defaultdict

import re


class GuardRecord:
    def __init__(self, date, guard):
        self.date = date
        self.guard = guard
        self.asleep = [0] * 60

    def tostr(self):
        s = "".join([
            "#" if sleeping else "."
            for sleeping in self.asleep
        ])
        return f"{self.date} {self.guard} {s}"

    def minutes_asleep(self):
        return sum(self.asleep)


class GuardRota:
    def __init__(self):
        self.rota = []
        self.per_guard = defaultdict(list)

    @classmethod
    def from_list(cls, lines):
        """
        [
            "[1518-11-01 23:51] Guard #1697 begins shift",
            "[1518-05-14 00:14] falls asleep",
            "[1518-08-04 00:49] wakes up",
            "[1518-08-07 00:47] falls asleep"
        ]
        """
        rota = cls()

        shift_start = re.compile(
            r"(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2})]\s+Guard\s+#(\d+)"
        )
        falls_asleep = re.compile(
            r"(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2})]\s+falls\s+asleep"
        )
        wakes_up = re.compile(
            r"(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2})]\s+wakes\s+up"
        )

        guard = None
        sleep_min = None

        for entry in sorted(lines):
            m = shift_start.search(entry)
            if m:
                if guard:
                    rota.add_record(guard)

                guard = GuardRecord(
                    date=f"{m.group(2)}-{m.group(3)}",
                    guard=int(m.group(6))
                )
                continue

            m = falls_asleep.search(entry)
            if m:
                sleep_min = int(m.group(5))
                continue

            m = wakes_up.search(entry)
            if m:
                wake_min = int(m.group(5))
                guard.asleep[sleep_min:wake_min] = [1] * (wake_min - sleep_min)

        rota.add_record(guard)

        return rota

    def add_record(self, guard_record):
        self.rota.append(guard_record)
        self.per_guard[guard_record.guard].append(len(self.rota) - 1)

    def guard_records(self, guard):
        for i in self.per_guard[guard]:
            yield self.rota[i]

    def guards(self):
        """
        Return iterator over all guard ids
        """
        return self.per_guard.keys()

    def part1(self):
        """
        Find guard with the most number of sleep minutes, and the
        minute where this guard slept most frequently over the rota.
        Return the product.
        """
        sleeps = Counter()
        for entry in self.rota:
            sleeps[entry.guard] += entry.minutes_asleep()

        guard = sleeps.most_common(1)[0][0]

        # Find the most commonly slept minute for guard
        sleep_minute = Counter()
        for entry in self.rota:
            if entry.guard == guard:
                for minute, asleep in enumerate(entry.asleep):
                    if asleep:
                        sleep_minute[minute] += 1

        minute = sleep_minute.most_common(1)[0][0]

        return guard * minute

    def part2(self):
        """
        Of all guards, which guard is most frequently asleep on the same
        minute?
        """
        best = (0, None, None)
        for guard_id in self.guards():
            minutes = [0] * 60
            for record in self.guard_records(guard_id):
                for index, asleep in enumerate(record.asleep):
                    if asleep:
                        minutes[index] += 1
            max_idx, count = max(enumerate(minutes), key=lambda v: v[1])
            if count >= best[0]:
                best = (count, guard_id, max_idx)

        return best[1] * best[2]


def read_data(filename="input4.data"):
    """
    Load the raw datafile
    """
    with open(filename) as f:
        lines = f.read().splitlines()

    return lines


if __name__ == "__main__":
    data = read_data()

    rota = GuardRota.from_list(data)

    print(f"Part1: {rota.part1()}")
    print(f"Part2: {rota.part2()}")
