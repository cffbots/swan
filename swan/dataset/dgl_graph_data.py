"""Interface to build a Dataset for DGL. see: https://www.dgl.ai/"""
from pathlib import Path
from typing import List, Optional, Tuple, Union

import torch
from torch.utils.data import DataLoader, Dataset

from .data_graph_base import SwanGraphData
from .graph.molecular_graph import create_molecular_dgl_graph

try:
    import dgl
except ImportError:
    raise ImportError("DGL is a required dependency, see: https://www.dgl.ai/")

__all__ = ["DGLGraphData"]


PathLike = Union[str, Path]


def collate_fn(samples):
    """Aggregate graphs."""
    graphs, y = map(list, zip(*samples))
    return dgl.batch(graphs), torch.cat(y).unsqueeze(-1)


def dgl_data_loader(*args, **kwargs):
    """Load the data using a customize collate function."""
    return DataLoader(*args, collate_fn=collate_fn, **kwargs)


class DGLGraphData(SwanGraphData):
    """Dataset construction for DGL."""
    def __init__(self,
                 data_path: PathLike,
                 properties: Optional[Union[str, List[str]]] = None,
                 sanitize: bool = True,
                 file_geometries: Optional[PathLike] = None,
                 optimize_molecule: bool = False) -> None:
        """Generate a dataset using graphs

        Parameters
        ----------
        data_path
            path of the csv file
        properties
            Labels names
        sanitize
            Check that molecules have a valid conformer
        file_geometries
            Path to a file with the geometries in PDB format
        optimize_molecule
            Perform a molecular optimization using a force field.
        """
        super().__init__(
            data_path, properties=properties, sanitize=sanitize,
            file_geometries=file_geometries, optimize_molecule=optimize_molecule)

        # create the dataset
        self.dataset = DGLGraphDataset(self.molecular_graphs, self.labels)

        # define the loader type
        self.data_loader_fun = dgl_data_loader

    def compute_graph(self) -> List[dgl.DGLGraph]:
        """compute the graphs in advance."""
        # create the graphs
        molecular_graphs = []
        for idx in range(len(self.dataframe)):
            labels = None if self.labels is None else self.labels[idx]
            gm = create_molecular_dgl_graph(
                self.dataframe["molecules"][idx],
                self.dataframe["positions"][idx],
                labels=labels)
            molecular_graphs.append(gm)

        return molecular_graphs

    def get_item(self, batch_data: List[torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
        """get the data/ground truth of a minibatch

        Parameters
        ----------
        batch_data : List[Data]
            data of the mini batch

        Returns
        -------
        [type]
            feature, label
        """
        return batch_data[0], batch_data[1]


class DGLGraphDataset(Dataset):
    def __init__(self, molecular_graphs: List[dgl.DGLGraph], labels: torch.Tensor):
        """Generate a dataset using graphs
        """
        super().__init__()
        self.molecular_graphs = molecular_graphs
        self.labels = labels

    def __len__(self) -> int:
        """Return dataset length."""
        return len(self.molecular_graphs)

    def __getitem__(self, idx: int) -> Tuple[dgl.DGLGraph, torch.Tensor]:
        """Return the idx dataset element."""

        return self.molecular_graphs[idx], self.labels[idx]
