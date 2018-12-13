def get_data():
    with open('../input.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    initial_state = lines[0].replace('initial state: ', '')
    rules = []
    for line in lines[2:]:
        rules.append(line)
    return Pots(initial_state, Rules(rules))


class Pots:
    def __init__(self, initial_state, rules, middle_pot_index=0, generation=0):
        self._state = initial_state
        self._rules = rules
        self._middle_pot = middle_pot_index
        self._generation = generation

    def __getitem__(self, index):
        pots = ''
        for i in range(index - 2, index + 3):
            if 0 <= i < len(self._state):
                pots += self._state[i]
            else:
                pots += '.'
        return pots

    def __eq__(self, other):
        return self.state == other.state

    def __len__(self):
        return len(self.state)

    @property
    def state(self):
        return self._state.strip('.')

    def apply(self):
        new_state = ''
        for i in range(-2, len(self._state) + 2):
            new_state += self._rules[self[i]]
        # new_state, culled = self._cull(new_state)
        return Pots(new_state, self._rules, middle_pot_index=self._middle_pot + 2, generation=self._generation + 1)

    @property
    def sum(self):
        _sum = 0
        for i in range(len(self._state)):
            if self._state[i] == '#':
                _sum += i - self._middle_pot
        return _sum

    def _cull(self, state):
        culled = 0
        while self._rules[state[:5]] != '#' and culled <= self._middle_pot:
            state = state[1:]
            culled += 1
        while self._rules[state[-5:]] != '#' and len(state) > len(self._state):
            state = state[:-1]
        return state, culled


class Pot:
    def __init__(self, plant):
        if plant in ['#', True]:
            self.plant = True
        elif plant in ['.', False]:
            self.plant = False
        else:
            raise ValueError('Incorrect plant value')


class Rules(dict):
    def __init__(self, rules):
        _rules = {}
        for rule in rules:
            pattern, pot = rule.split(' => ')
            _rules[pattern] = pot
        super().__init__(_rules)

    def __getitem__(self, item):
        if item not in self:
            return '.'
        return self.get(item)


def run():
    initial = get_data()
    part_1(initial)
    part_2(initial)


def part_1(initial):
    pots = germinate(initial, generations=20)
    print(pots.sum)


def part_2(initial):
    pots = germinate(initial, generations=50_000_000_000)
    print(pots.sum)


def germinate(pots, generations):
    prev = pots
    for i in range(generations):
        next = prev.apply()
        if prev == next:
            print('Shortcut in calculations...')
            print(next.sum + (next.sum - prev.sum) * (generations - i - 1))
        prev = next
    return prev


if __name__ == '__main__':
    run()
