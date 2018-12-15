

class ChocolateMixer:
    def __init__(self):
        self.tick = 0
        self.state = "37"
        self.elf1_recipe = 0
        self.elf2_recipe = 1
        # print(self)

    def calc_index(self, index):
        size = len(self.state)
        score = int(self.state[index])
        return (index + score + 1) % size

    def mix_recipes(self):
        a = int(self.state[self.elf1_recipe])
        b = int(self.state[self.elf2_recipe])
        self.state += str(a + b)
        self.elf1_recipe = self.calc_index(self.elf1_recipe)
        self.elf2_recipe = self.calc_index(self.elf2_recipe)

        self.tick += 1
        # print(self)

    def run(self, num_iterations):
        for _ in range(num_iterations):
            self.mix_recipes()

    def get_10_recipes_after_n(self, value):
        self.run(10+value)

        return self.state[value:value+10]

    def find_recipes_index(self, recipes):
        if recipes not in self.state:
            while recipes not in self.state[-8:]:
                self.mix_recipes()

        index = self.state.index(recipes)
        return index

    def __repr__(self):
        return f"({self.tick:3})E1:{self.elf1_recipe} E2:{self.elf2_recipe} S:{self.state}"


def solve():

    # Part 1
    input_data = 503761
    mixer = ChocolateMixer()
    r = mixer.get_10_recipes_after_n(input_data)
    print(f"Part1 - The scores of the 10 recipes after {input_data} recipes is: {r}")

    # Part 2
    index = mixer.find_recipes_index("503761")
    print(f"Part2 - It appear {index} recipes to the left of our input.")


if __name__ == "__main__":
    solve()
