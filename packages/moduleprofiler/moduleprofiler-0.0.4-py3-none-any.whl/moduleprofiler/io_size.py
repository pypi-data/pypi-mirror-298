import torch
import torch.nn as nn
from typing import Tuple


def _default_io_size_fn(
        module: nn.Module,
        input: Tuple[torch.Tensor],
        output: torch.Tensor
) -> Tuple[tuple]:
    input_ = None if len(input) == 0 else tuple(input[0].size())

    if output is None:
        output_ = None

    elif isinstance(output, tuple):
        output_ = tuple(tuple(o.size()) for o in output)

    elif isinstance(output, list):
        output_ = [tuple(o.size()) for o in output]

    else:
        output_ = tuple(output.size())

    return input_, output_


def _gru_io_size_fn(
        module: nn.GRU,
        input: Tuple[torch.Tensor],
        output: torch.Tensor
) -> Tuple[tuple]:
    input_shape = input[0].size()
    output_shape = output[0][0].size()
    hidden_state_shape = output[1][0].size()

    return (
        tuple(input_shape),
        (tuple(output_shape), tuple(hidden_state_shape))
    )


def _lstm_io_size_fn(
        module: nn.LSTM,
        input: Tuple[torch.Tensor],
        output: torch.Tensor
) -> Tuple[tuple]:
    input_shape = input[0].size()
    output_shape = output[0][0].size()
    hidden_state_shape = output[1][0].size()
    cell_state_shape = output[1][1].size()

    return (
        tuple(input_shape),
        (
            tuple(output_shape),
            (tuple(hidden_state_shape), tuple(cell_state_shape))
        )
    )


def get_default_io_size_map() -> dict:
    return {
        nn.GRUCell: _gru_io_size_fn,
        nn.GRU: _gru_io_size_fn,
        nn.LSTMCell: _lstm_io_size_fn,
        nn.LSTM: _lstm_io_size_fn,
        "default": _default_io_size_fn
    }
