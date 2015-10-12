from random import uniform


def random_weight():
    return uniform(-0.5, 0.5)


class Neuron:
    def __init__(self, number_of_inputs, threshold, learning_rate, desired_output):
        self.number_of_inputs = number_of_inputs
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.desired_output = desired_output

        self.w = self.generate_matrix(self.number_of_inputs, 1, self.random_weight)
        self.x = None

        self.y = None
        self.y_d = None

    def calculate_output(self):
        return self.step_function(
            sum(self.x[i] * self.w[i] for i in range(self.number_of_inputs)) - self.threshold
        )

    def activate(self, x):
        self.x = x

        self.y = self.calculate_output()
        self.y_d = self.desired_output(*self.x)

    def error(self):
        return self.y_d - self.y

    def delta(self, i):
        return self.learning_rate * self.x[i] * self.error()

    def train(self):
        for i in range(self.number_of_inputs):
            self.w[i] += self.delta(i)

    def iterate(self, input_values_list):
        while True:
            is_finished = True

            for input_values in input_values_list:
                self.activate(input_values)
                self.train()

                print self.threshold
                print self.x
                print self.w
                print self.y, self.y_d
                print self.error()
                print

                if abs(self.error()) > 0:
                    is_finished = False

            if is_finished:
                return

    @staticmethod
    def step_function(value):
        return 1 if value >= 0 else 0

    @staticmethod
    def random_weight():
        return uniform(-0.5, 0.5)

    @staticmethod
    def generate_matrix(n, m, value_generator):
        matrix = []

        for i in range(n):
            if m == 1:
                matrix.append(value_generator())
            else:
                row = []

                for j in range(m):
                    row.append(value_generator())

                matrix.append(row)

        return matrix


"""class NeuralNetwork:
    def __init__(self, number_of_inputs, number_of_hidden_nodes, learning_rate, desired_output):
        self.number_of_inputs = number_of_inputs
        self.number_of_hidden_nodes = number_of_hidden_nodes
        self.learning_rate = learning_rate
        self.desired_output = desired_output

        self.weights_input, self.weights_output, self.threshold = self.initialization()

        self.activation()

        print self.weights_input
        print self.weights_output
        print self.threshold

    def initialization(self):
        weights_input = self.generate_matrix(self.number_of_inputs, self.number_of_hidden_nodes, random_weight)
        weights_output = self.generate_matrix(self.number_of_inputs, 2, lambda: 0)

        threshold = random_weight()

        return weights_input, weights_output, threshold

    def activation(self):
        for hidden_index in range(self.number_of_hidden_nodes):
            total = 0.0

            for i in range(self.number_of_inputs):
                total += self.weights_input[i][hidden_index]

            self.weights_output[hidden_index][0] = self.step_function(total)

    def training(self):
        pass

    def iteration(self):
        pass

    def error(self):
        pass

    @staticmethod
    def step_function(value):
        return 1 if value >= 0 else 0

    @staticmethod
    def generate_matrix(n, m, value_generator):
        matrix = []

        for i in range(n):
            row = []

            for j in range(m):
                row.append(value_generator())

            matrix.append(row)

        return matrix"""


def main():
    def desired_output(x1, x2):
        return x1 * x2

    neuron = Neuron(2, random_weight(), 0.1, desired_output)

    neuron.iterate([[0, 0], [0, 1], [1, 0], [1, 1]])

    print neuron.w

if __name__ == '__main__':
    main()
