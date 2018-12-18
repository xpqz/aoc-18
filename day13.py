from itertools import cycle


class Collision(Exception):
    pass


def read_data(filename="data/input13.data"):
    with open(filename) as f:
        return [list(line) for line in f.read().splitlines()]


class Cart:
    def __init__(self, xpos, ypos, ch):
        """
        Turn order: left, straight, right
        """
        self.xpos = xpos
        self.ypos = ypos
        self.ch = ch
        self.route_choice = cycle(["<", "|", ">"])

    def turn(self):
        """
        Cycle through directions when hitting a +
        """
        newdir = next(self.route_choice)
        if newdir == "|":
            return

        self.ch = {
            "^<": "<",
            "v>": "<",
            "^>": ">",
            "v<": ">",
            "<>": "^",
            "><": "^",
            ">>": "v",
            "<<": "v"
        }[f"{self.ch}{newdir}"]

    def veer(self, newdir):
        self.ch = {
            "^\\": "<",
            "^/": ">",
            "v\\": ">",
            "v/": "<",
            "<\\": "^",
            "</": "v",
            ">\\": "v",
            ">/": "^"
        }[f"{self.ch}{newdir}"]

    def coord(self):
        return (self.xpos, self.ypos)


class Node:
    def __init__(self, ch, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.ch = ch

    def set_updown(self):
        self.up = (self.xpos, self.ypos-1)
        self.down = (self.xpos, self.ypos + 1)

    def set_leftright(self):
        self.left = (self.xpos - 1, self.ypos)
        self.right = (self.xpos + 1, self.ypos)

    def set_downright(self):
        self.down = (self.xpos, self.ypos + 1)
        self.right = (self.xpos + 1, self.ypos)

    def set_upright(self):
        self.up = (self.xpos, self.ypos - 1)
        self.right = (self.xpos + 1, self.ypos)

    def set_upleft(self):
        self.up = (self.xpos, self.ypos - 1)
        self.right = (self.xpos - 1, self.ypos)

    def set_downleft(self):
        self.down = (self.xpos, self.ypos + 1)
        self.left = (self.xpos - 1, self.ypos)

    def set_cross(self):
        self.set_updown()
        self.set_leftright()


class Map:
    def __init__(self, nodes, carts):
        self.nodes = nodes
        self.carts = carts

    def check_turn(self, cart):
        """
        Cart is at a node. If it's a "+", execute a turn. If it's "\\/", veer.
        """
        node = self.nodes[cart.coord()]
        # check current node in case already mid-turn
        if node.ch == "+":
            cart.turn()
        elif node.ch in ["/", "\\"]:
            cart.veer(node.ch)

    def move(self, cart):
        # Check current node in case already mid-turn
        self.check_turn(cart)

        oldpos = cart.coord()

        # Move cart along one step in its current direction
        if cart.ch == "^":
            cart.ypos = cart.ypos - 1
        elif cart.ch == "v":
            cart.ypos = cart.ypos + 1
        elif cart.ch == ">":
            cart.xpos = cart.xpos + 1
        else:
            cart.xpos = cart.xpos - 1

        # Did we run into someone?
        if (cart.xpos, cart.ypos) in self.carts:
            raise Collision({"pos": (cart.xpos, cart.ypos)})

        # Move the cart in our cart dict.
        self.carts.pop(oldpos, None)
        self.carts[(cart.xpos, cart.ypos)] = cart

    @classmethod
    def from_lines(cls, lines):
        nodes = {}
        carts = {}
        for ypos, line in enumerate(lines):
            for xpos, ch in enumerate(line):
                if ch == " ":
                    continue

                node = Node(ch, xpos, ypos)
                nodes[(xpos, ypos)] = node

                if ch == "-":
                    node.set_leftright()
                elif ch == "|":
                    node.set_updown()
                elif ch == "/":
                    # Up-left or down-right
                    # To disambiguate we need to look one level up.
                    if (
                        (xpos, ypos - 1) in nodes and
                        nodes[(xpos, ypos - 1)].ch in "|+"
                    ):
                        node.set_upleft()
                    else:
                        node.set_downright()
                elif ch == "\\":
                    # Either down-left or up-right
                    # To disambiguate we need to look one level up.
                    if (
                        (xpos, ypos - 1) in nodes and
                        nodes[(xpos, ypos - 1)].ch in "|+"
                    ):  # up & right
                        node.set_upright()
                    else:
                        node.set_downleft()
                elif ch == "+":
                    node.set_cross()
                elif ch in "><^v":
                    # Cart obscuring track. Eyeballing the data allows us a
                    # cheeky optimisation: cart direction uniquely identifies
                    # the obscured track piece -- this isn't true in general.
                    carts[(xpos, ypos)] = Cart(xpos, ypos, ch)
                    if ch in ["^", "v"]:
                        node.set_updown()
                    else:
                        node.set_leftright()

        return cls(nodes, carts)

    def tick(self):
        # Process carts from top-left to bottom-right.
        row_order_carts = sorted(
            self.carts.keys(),
            key=lambda k: (k[1], k[0])
        )  # <3 Python

        for cartpos in row_order_carts:
            cart = self.carts[cartpos]
            self.move(cart)


if __name__ == "__main__":
    lines = read_data()
    tracks = Map.from_lines(lines)

    tick = 0
    coll_pos = None
    while True:
        try:
            tracks.tick()
        except Collision as coll:
            coll_pos = coll.args[0]
            break
        tick += 1

    print(f"Part1: collision at {coll_pos} after {tick} ticks")
