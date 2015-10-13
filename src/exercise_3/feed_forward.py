# -*- coding: utf-8 -*-

from pybrain.structure import TanhLayer
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer


class FeedForward:
    def __init__(self, hidden_nodes):
        self.data_set = self.fill_data_set()
        self.network = buildNetwork(1, hidden_nodes, 1, bias=True, hiddenclass=TanhLayer)

        self.trainer = self.train()

    @staticmethod
    def fill_data_set():
        data_set = SupervisedDataSet(1, 1)

        for _ in range(5):
            for i in range(9):
                data_set.addSample(i, i)

        return data_set

    def train(self):
        trainer = BackpropTrainer(self.network, self.data_set)

        trainer.trainUntilConvergence(
            verbose=False, validationProportion=0.15, maxEpochs=1000, continueEpochs=10)

        return trainer

    def activate(self, input_value):
        return self.network.activate([input_value])


def main():
    for number_of_hidden_nodes in range(8, 0, -1):
        print 'Number of hidden nodes in network: %d\n' % number_of_hidden_nodes
        network = FeedForward(number_of_hidden_nodes)

        print 'Activating with integers in range [1, 8]'
        for integer in range(1, 9):
            print '%d: %f' % (integer, network.activate(integer))

        print '\nActivating with numbers outside the training set'
        for value in [9, 0, -1, 10, 100, 0.5, 7.5, 4.5]:
            print '%f: %f' % (value, network.activate(value))

        print '\n'

if __name__ == '__main__':
    main()
