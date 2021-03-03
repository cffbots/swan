"""Statistical models."""
import torch
import torch.nn.functional as F
from flamingo.features.featurizer import NUMBER_ATOMIC_GRAPH_FEATURES, NUMBER_BOND_GRAPH_FEATURES

from torch.nn import GRU, Linear, ReLU, Sequential
from torch_geometric.nn import NNConv, Set2Set

__all__ = ["MPNN"]


class MPNN(torch.nn.Module):
    """Create a molecular graph convolutional network.

    Use the convolution reported at: https://arxiv.org/abs/1704.01212
    This network was taking from: https://github.com/rusty1s/pytorch_geometric/blob/master/examples/qm9_nn_conv.py
    """
    def __init__(self, num_labels=1, dim=64, batch_size=128):
        super(MPNN, self).__init__()
        # Number of iterations to propagate the message
        self.iterations = 3
        # Input layer
        self.lin0 = torch.nn.Linear(NUMBER_ATOMIC_GRAPH_FEATURES, dim)

        # NN that transform the states into message using the edge features
        nn = Sequential(Linear(NUMBER_BOND_GRAPH_FEATURES, batch_size), ReLU(), Linear(batch_size, dim * dim))
        self.conv = NNConv(dim, dim, nn, aggr='mean')
        # Combine the old state with the new one using a Gated Recurrent Unit
        self.gru = GRU(dim, dim)
        # Pooling function
        self.set2set = Set2Set(dim, processing_steps=self.iterations)
        # Fully connected output layers
        self.lin1 = torch.nn.Linear(2 * dim, dim)
        self.lin2 = torch.nn.Linear(dim, num_labels)

    def forward(self, data):
        out = F.relu(self.lin0(data.x))
        h = out.unsqueeze(0)

        # propagation in "time" of the messages
        for i in range(self.iterations):
            # Collect the message from the neighbors
            m = F.relu(self.conv(out, data.edge_index, data.edge_attr))
            # update the state
            out, h = self.gru(m.unsqueeze(0), h)
            out = out.squeeze(0)

        # Pool the state vectors
        out = self.set2set(out, data.batch)
        out = F.relu(self.lin1(out))
        return self.lin2(out)
