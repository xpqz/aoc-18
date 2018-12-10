"""
day 7 of Advent of Code 2018
by Stefan Kruger
"""
from dataclasses import dataclass, field
from collections import defaultdict
import json
import re

FIXED_TASK_COST = 60


def weight(task):
    return FIXED_TASK_COST + ord(task) - ord("A") + 1


def read_data(filename="input7.data"):
    with open(filename) as f:
        return f.read().splitlines()


def pvl(vertex_list):
    """
    Convert a list of vertexes to a string of task names for output.
    """
    return "".join([str(v) for v in vertex_list])


def parse_data(lines):
    patt = re.compile(r'Step (.) must be finished before step (.) can begin.')
    result = []
    for line in lines:
        m = patt.search(line)
        if m:
            result.append((m.group(1), m.group(2)))

    return result


@dataclass(unsafe_hash=True)
class Vertex:
    """
    Class representing a vertex in a DAG. It holds a "task" (a capital letter)
    and (for part2) a weight.
    """
    task: str
    cost: int = field(init=False)

    def __post_init__(self):
        self.cost = weight(self.task)

    def __str__(self):
        return self.task


@dataclass
class Job:
    """
    Class representing a Job to be processed by a WorkerPool instance. Each job
    is a vertex and a measure of the remaning processing time.
    """
    vertex: Vertex
    remaining: int = field(init=False)

    def __post_init__(self):
        self.remaining = self.vertex.cost

    def tick(self):
        """
        Apply a second's worth of work by decreasing self.remaining.
        """
        self.remaining -= 1
        return self.done()

    def done(self):
        return self.remaining == 0


class WorkerPool:
    """
    Simulation of a concurrency pool.
    """

    def __init__(self, size):
        self.workers = [None] * size
        self.size = size
        self.ticks = 0

    def done(self):
        """
        Return any finished jobs, reaping any done workers.
        """
        finished = []
        for index, job in enumerate(self.workers):
            if job is not None and job.done():
                finished.append(job.vertex)
                self.workers[index] = None

        return finished

    def all_done(self):
        """
        Return True if no workers have active tasks.
        """
        for worker in self.workers:
            if worker is not None and not worker.done():
                return False
        return True

    def tick(self):
        """
        Apply a second's work by subtracting 1 from each of the workers' time
        to completion.
        """
        self.ticks += 1
        for current in self.workers:
            if current is not None and not current.done():
                current.tick()

    def add(self, vertex):
        """
        Add a new worker for a vertex task to the list, if there are any
        available slots.
        Returns False if the work load wasn't accepted (blocking).
        """
        for index, job in enumerate(self.workers):
            if job is None or job.done():
                self.workers[index] = Job(vertex)
                return True

        return False

    def add_task_list(self, vertex_list):
        """
        Add a list of vertexes to be processed. These are allocated in
        alphabetical order to available workers. If the list of available
        workers are shorter than the vertex list, only a subset will be
        accepted into the worker pool.
        """
        accepted = []
        for task in sorted(vertex_list, key=lambda x: x.task):
            if self.add(task):
                accepted.append(task)

        return accepted


class DAG:
    def __init__(self, edge_list):
        self.graph = defaultdict(list)
        self.vertexes = set()
        self.prereqs = defaultdict(list)
        for vertexes in edge_list:
            v1 = Vertex(task=vertexes[0])
            v2 = Vertex(task=vertexes[1])
            self.graph[v1].append(v2)
            self.vertexes.add(v1)
            self.vertexes.add(v2)
            self.prereqs[v2].append(v1)

    def display(self):
        print(json.dumps(self.graph, indent=4))

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]  # Note: no .append()! <3 python :/
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for vertex in self.graph[start]:
            if vertex not in path:
                newpaths = self.find_all_paths(vertex, end, path)
                for newpath in newpaths:
                    paths.append(newpath)

        return paths

    def stepping_order(self):
        (start_list, end) = self.find_start_end()
        paths = []
        for start in start_list:
            paths.extend(self.find_all_paths(start, end))

        order = []
        while True:
            available = {path[0] for path in paths if path}
            if not available:
                break
            for s in sorted(available, key=lambda x: x.task, reverse=True):
                if set(self.prereqs[s]).issubset(order):
                    step = s
            for path in paths:
                if path and path[0] == step:
                    path.remove(step)
            order.append(step)

        return order

    def prerequisites_complete(self, task, prereqs):
        return set(self.prereqs[task]).issubset(prereqs)

    def stepping_order_p2(self, concurrency):
        """
        Find the task path and time taken to process the task graph over
        a set of concurrent workers and a given cost function.

        Task allocation order is determined by the paths, and allocated
        alphabetically to a set of concurrency workers. Workers apply 1 work
        unit per second, until their allocated tasks are completed. Completed
        jobs are added onto the work order list in the order they are completed
        by the workers, and alphabetically if multiple workers complete in the
        same second.

        Return the computed task order, and the total number of seconds taken
        to complete all jobs.
        """

        (start_list, end) = self.find_start_end()
        paths = []
        for start in start_list:
            paths.extend(self.find_all_paths(start, end))

        order = []
        workers = WorkerPool(concurrency)

        while True:
            # Find the next set of potential tasks as given by the first
            # element in any non-empty path.
            available = {path[0] for path in paths if path}

            # End criterion: no remaining tasks, and all workers have completed
            # their running tasks.
            if not available and workers.all_done():
                break

            # Find the sub-set of available tasks where all their prerequisites
            # are completed, as given by the task graph.
            workable = [
                vertex
                for vertex in available
                if self.prerequisites_complete(vertex, order)
            ]

            # Assign workable tasks alphabetically to any available workers.
            # Note that this may block, so the accepted task list may be
            # shorter than the workable list (or empty).
            accepted = workers.add_task_list(workable)

            # If our workers accepted any new tasks, we remove those from the
            # graph's paths, as they are now under processing.
            for step in accepted:
                for path in paths:
                    if path and path[0] == step:
                        path.remove(step)

            # Perform one unit of work across all active workers.
            workers.tick()

            # Find any completed tasks, and add those to the running order.
            completed = workers.done()
            if completed:
                order.extend(completed)

        return (order, workers.ticks)

    def find_start_end(self):
        """
        Assume single endpoint. Note: start is a list!
        """
        has_deps = set()
        is_dep = set()
        for vertex in self.vertexes:
            if vertex in self.graph:
                has_deps.add(vertex)
                for node in self.graph[vertex]:
                    is_dep.add(node)

        return (list(has_deps - is_dep), list(is_dep - has_deps)[0])


if __name__ == "__main__":
    concurrent_workers = 5
    data = read_data()
    # # --- TEST DATA
    # data = [
    #     "Step C must be finished before step A can begin.",
    #     "Step C must be finished before step F can begin.",
    #     "Step A must be finished before step B can begin.",
    #     "Step A must be finished before step D can begin.",
    #     "Step B must be finished before step E can begin.",
    #     "Step D must be finished before step E can begin.",
    #     "Step F must be finished before step E can begin."
    # ]
    # FIXED_TASK_COST = 0
    # concurrent_workers = 2
    # # --- TEST DATA END

    dag = DAG(parse_data(data))
    print(f'Part1: {pvl(dag.stepping_order())}')

    order, seconds = dag.stepping_order_p2(concurrent_workers)
    print(
        f'Part2: {pvl(order)} took {seconds} seconds with '
        f'{concurrent_workers} workers and a fixed task cost '
        f'of {FIXED_TASK_COST}'
    )
