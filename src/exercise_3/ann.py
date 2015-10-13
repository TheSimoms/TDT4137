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
        for input_values in input_values_list:
            self.activate(input_values)
            self.train()

            print 'Weights: %s' % str(self.w)

            if abs(self.error()) > 0:
                self.iterate(input_values_list)

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


def main():
    for desired_output in [['AND', lambda x1, x2: x1 * x2], ['OR', lambda x1, x2: x1 or x2]]:
        neuron = Neuron(2, random_weight(), 0.1, desired_output[1])
        input_values_list = [[0, 0], [0, 1], [1, 0], [1, 1]]

        print '%s:\n' % desired_output[0]

        try:
            neuron.iterate(input_values_list)
        except RuntimeError:
            print 'No convergence. Combination of threshold and initial weights leads to deadlock\n'
        finally:
            print 'Final weights: %s\n' % ', '.join(map(str, neuron.w))

            for input_values in input_values_list:
                neuron.activate(input_values)

                print 'Input: %s. Result: %d' % (str(input_values), neuron.y)

        print '\n'

if __name__ == '__main__':
    main()
