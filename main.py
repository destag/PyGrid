from anytree import Node, RenderTree


class Grid:
    def __init__(self, power, is_city):
        self.transformer_power = power
        self.nodes = [GridNode("[00]", 0, power, None)]
        self.root = self.nodes[0]
        self.num_nodes = 0
        self.owners = 0
        self.is_city = is_city

    def add_node(self, length, receive, parent_id):
        self.num_nodes += 1
        if self.num_nodes > 9:
            name = "[" + str(self.num_nodes) + "]"
        else:
            name = "[0" + str(self.num_nodes) + "]"

        if receive[0] == "e":
            pwr = int(receive[1:]) * 7.18
            self.owners += int(receive[1:])
        elif receive[0] == "p":
            pwr = float(receive[1:])
            self.owners += 1
        else:
            pwr = 0
        self.nodes.append(GridNode(name, length, pwr, self.nodes[parent_id]))

    def __len__(self):
        max_len = 0
        for n in self.nodes:
            if n.is_leaf:
                if len(n) > max_len:
                    max_len = len(n)
        return max_len

    def evaluate_grid_current(self):
        """
        :param owners: liczba odbiorcow
        :param is_city: czy miejscowosc jest miastem
        :return: prad obwodu
        """
        kj = self.get_kj()
        print("kj: ", kj)
        return round((kj * self.owners * 12500) / (1.73 * 400 * .93), 2)

    def get_kj(self):
        """
        :param self: liczba odbiorcow
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

        return self.is_city and city_kj.get(self.owners, .4) or vill_kj.get(self.owners, .3)

    def voltage(self):
        # TODO: oblicza spadek napiecia obowu
        pass


class GridNode(Node):
    def __init__(self, name, length, power, parent):
        super().__init__(name, parent)
        self.length = length
        self.power = power

    def __len__(self):
        if self.name == "[00]" or self.parent.name == "[00]":
            return self.length
        else:
            return self.length + len(self.parent)


typ = input("Typ miejscowsci (m/w): ") == "m"

transformer_power = input("Moc transformatora [kVA]: ")
grid = Grid(int(transformer_power), typ)

while True:
    for pre, fill, node in RenderTree(grid.root):
        print("%s%s" % (pre, node.name))
    choice = input("<>: ").split()
    if choice[0] == "exit":
        break
    elif choice[0] == "add":
        grid.add_node(int(choice[2]), choice[3], int(choice[1]))
    elif choice[0] == "len":
        print(len(grid.nodes[int(choice[1])]))
    elif choice[0] == "i":
        print("I:", grid.evaluate_grid_current(), "A")

print(len(grid))
