import re
import heapq


def get_input():
    return [
        "Step S must be finished before step V can begin.",
        "Step J must be finished before step T can begin.",
        "Step N must be finished before step Q can begin.",
        "Step O must be finished before step H can begin.",
        "Step I must be finished before step C can begin.",
        "Step Y must be finished before step R can begin.",
        "Step K must be finished before step B can begin.",
        "Step A must be finished before step C can begin.",
        "Step B must be finished before step D can begin.",
        "Step W must be finished before step T can begin.",
        "Step E must be finished before step V can begin.",
        "Step Q must be finished before step L can begin.",
        "Step U must be finished before step P can begin.",
        "Step R must be finished before step C can begin.",
        "Step V must be finished before step M can begin.",
        "Step X must be finished before step P can begin.",
        "Step G must be finished before step T can begin.",
        "Step T must be finished before step Z can begin.",
        "Step Z must be finished before step M can begin.",
        "Step F must be finished before step C can begin.",
        "Step M must be finished before step L can begin.",
        "Step D must be finished before step C can begin.",
        "Step H must be finished before step L can begin.",
        "Step L must be finished before step P can begin.",
        "Step P must be finished before step C can begin.",
        "Step S must be finished before step Q can begin.",
        "Step M must be finished before step P can begin.",
        "Step S must be finished before step T can begin.",
        "Step U must be finished before step T can begin.",
        "Step X must be finished before step H can begin.",
        "Step Q must be finished before step G can begin.",
        "Step Y must be finished before step U can begin.",
        "Step H must be finished before step C can begin.",
        "Step O must be finished before step F can begin.",
        "Step S must be finished before step P can begin.",
        "Step B must be finished before step E can begin.",
        "Step S must be finished before step D can begin.",
        "Step R must be finished before step X can begin.",
        "Step Z must be finished before step D can begin.",
        "Step J must be finished before step C can begin.",
        "Step Z must be finished before step F can begin.",
        "Step K must be finished before step T can begin.",
        "Step T must be finished before step H can begin.",
        "Step E must be finished before step H can begin.",
        "Step D must be finished before step L can begin.",
        "Step O must be finished before step A can begin.",
        "Step V must be finished before step T can begin.",
        "Step V must be finished before step X can begin.",
        "Step Q must be finished before step X can begin.",
        "Step O must be finished before step K can begin.",
        "Step L must be finished before step C can begin.",
        "Step W must be finished before step H can begin.",
        "Step I must be finished before step T can begin.",
        "Step M must be finished before step H can begin.",
        "Step V must be finished before step G can begin.",
        "Step K must be finished before step P can begin.",
        "Step E must be finished before step X can begin.",
        "Step V must be finished before step C can begin.",
        "Step Y must be finished before step W can begin.",
        "Step J must be finished before step G can begin.",
        "Step B must be finished before step C can begin.",
        "Step B must be finished before step Z can begin.",
        "Step K must be finished before step R can begin.",
        "Step Y must be finished before step V can begin.",
        "Step X must be finished before step G can begin.",
        "Step J must be finished before step K can begin.",
        "Step A must be finished before step M can begin.",
        "Step T must be finished before step M can begin.",
        "Step W must be finished before step D can begin.",
        "Step G must be finished before step F can begin.",
        "Step A must be finished before step B can begin.",
        "Step W must be finished before step F can begin.",
        "Step Y must be finished before step P can begin.",
        "Step B must be finished before step V can begin.",
        "Step N must be finished before step G can begin.",
        "Step J must be finished before step H can begin.",
        "Step S must be finished before step L can begin.",
        "Step A must be finished before step R can begin.",
        "Step X must be finished before step D can begin.",
        "Step Y must be finished before step M can begin.",
        "Step H must be finished before step P can begin.",
        "Step F must be finished before step D can begin.",
        "Step S must be finished before step G can begin.",
        "Step K must be finished before step C can begin.",
        "Step W must be finished before step Z can begin.",
        "Step A must be finished before step Z can begin.",
        "Step O must be finished before step Y can begin.",
        "Step U must be finished before step C can begin.",
        "Step X must be finished before step M can begin.",
        "Step Y must be finished before step A can begin.",
        "Step F must be finished before step P can begin.",
        "Step J must be finished before step Y can begin.",
        "Step R must be finished before step G can begin.",
        "Step Y must be finished before step Q can begin.",
        "Step D must be finished before step P can begin.",
        "Step O must be finished before step U can begin.",
        "Step O must be finished before step I can begin.",
        "Step E must be finished before step L can begin.",
        "Step G must be finished before step Z can begin.",
        "Step T must be finished before step F can begin.",
        "Step Q must be finished before step F can begin.",
    ]


class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.parents = []

    def __str__(self):
        return f"Node({self.name})"


class Graph:
    def __init__(self, nodes, workers=5, base_task_duration=60):
        self.workers = workers
        self.base_task_duration = base_task_duration
        self._nodes = {}

        for parent, children in nodes.items():
            parent = self[parent]
            for child in children:
                child = self[child]
                child.parents.append(parent)
                if child.name not in parent.children:
                    parent.children[child.name] = child
        root = Node('root')
        for name, node in self._nodes.items():
            if not node.parents:
                root.children[name] = node
        self.root = root

    def __getitem__(self, item) -> Node:
        if item not in self._nodes:
            self._nodes[item] = Node(item)
        return self._nodes[item]

    @property
    def order(self):
        _order = ''
        available = list(self.root.children.items())
        heapq.heapify(available)
        while available:
            name, node = heapq.heappop(available)
            _order += name
            self.add_tasks(_order, available, node)
        return _order

    @staticmethod
    def add_tasks(_completed, available, node):
        for name, child in node.children.items():
            if set(_completed) >= set([parent.name for parent in child.parents]):
                heapq.heappush(available, (name, child))

    @property
    def execution_time(self):
        workers = {worker: {'task': None, 'remaining': 0} for worker in range(self.workers)}
        _time = 0
        _done = ''
        available = list(self.root.children.items())
        heapq.heapify(available)
        while any([worker['task'] is not None for worker in workers.values()]) or available:
            self._assign_work(workers, available)
            duration, finished = self._work(workers)
            _time += duration
            for node in finished:
                _done += node.name
            for node in finished:
                self.add_tasks(_done, available, node)
        return _time

    def task_duration(self, node):
        return self.base_task_duration + (bytearray(node.name.upper(), 'ascii')[0] - 64)

    def _assign_work(self, workers, available):
        for worker in workers.values():
            if worker['task'] is None and available:
                _, node = heapq.heappop(available)
                worker['task'] = node
                worker['remaining'] = self.task_duration(node)

    def _work(self, workers):
        finished = []
        duration = min([worker['remaining'] for worker in workers.values() if worker['task']])
        for worker in workers.values():
            if worker['task'] is not None:
                worker['remaining'] -= duration
        for worker in workers.values():
            if worker['task'] and worker['remaining'] == 0:
                finished.append(worker['task'])
                worker['task'] = None
        return duration, finished


def get_graph():
    regex = re.compile(r"Step (?P<node>\w) must be finished before step (?P<child>\w) can begin.")
    nodes = {}
    for requirement in get_input():
        result = regex.search(requirement).groupdict()
        node, child = result['node'], result['child']
        if node not in nodes:
            nodes[node] = []
        nodes[node].append(child)
    return Graph(nodes)


def part_1():
    graph = get_graph()
    print(graph.order)


def part_2():
    graph = get_graph()
    print(graph.execution_time)


def run():
    part_1()
    part_2()


if __name__ == '__main__':
    run()
