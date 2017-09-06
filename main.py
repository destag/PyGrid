from anytree import Node, RenderTree


class Grid:
    def __init__(self, power):
        self.transformer_power = power
        self.nodes = [GridNode("[00]", 0, power, None)]
        self.root = self.nodes[0]
        self.num_nodes = 0

    def add_node(self, length, power, parent_id):
        self.num_nodes += 1
        if self.num_nodes > 9:
            name = "[" + str(self.num_nodes) + "]"
        else:
            name = "[0" + str(self.num_nodes) + "]"
        self.nodes.append(GridNode(name, length, power, self.nodes[parent_id]))

    def __len__(self):
        max_len = 0
        for n in self.nodes:
            if n.is_leaf:
                if len(n) > max_len:
                    max_len = len(n)
        return max_len


class GridNode(Node):
    def __init__(self, name, length, power, parent):
        super().__init__(name, parent)
        self.length = length
        self.power = power

    def __len__(self):
        if self.parent.name == "[00]" or self.name == "[00]":
            return self.length
        else:
            return self.length + len(self.parent)


def get_kj(owners, is_city):
    """
    :param owners: liczba odbiorcow
    :param is_city: czy miejscowosc jest miastem
    :return: wspolczynnik jednoczesnosci
    """
    city_kj = {
        1: 1,
        2: .94,
        3: .9,
        4: .83,
        5: .8,
        6: .72,
        7: .7,
        8: .6,
        9: .55,
        10: .5,
    }

    vill_kj = {
        1: 1,
        2: .8,
        3: .7,
        4: .6,
        5: .55,
        6: .45,
        7: .45,
        8: .4,
        9: .36,
        10: .33,
    }

    return is_city and city_kj.get(owners, .4) or vill_kj.get(owners, .3)


def evaluate_grid_current(owners, is_city):
    """
    :param owners: liczba odbiorcow
    :param is_city: czy miejscowosc jest miastem
    :return: prad obwodu
    """
    kj = get_kj(owners, is_city)
    print("kj: ", kj)
    return round((kj * owners * 12500) / (1.73 * 400 * .93), 2)


own = int(input("Ilu odbiorców: "))
typ = input("Typ miejscowsci (m/w): ") == "m"
print("I: ", evaluate_grid_current(own, typ), "A")

transformer_power = input("Moc transformatora [kVA]: ")
grid = Grid(int(transformer_power))

while True:
    for pre, fill, node in RenderTree(grid.root):
        print("%s%s" % (pre, node.name))
    choice = input("<>: ").split()
    if choice[0] == "exit":
        break
    elif choice[0] == "add":
        grid.add_node(int(choice[2]), int(choice[3]), int(choice[1]))


print(len(grid))
