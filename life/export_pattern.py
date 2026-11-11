"""Export Golly-readable initial Conway universe."""
from .core import encode_rle
from .singer_pilot import initial_state

if __name__ == "__main__":
    print(encode_rle(initial_state(), [
        "Three glider pulses toggle a mouth block in one uninterrupted Life run.",
        "Source: Luke Kiernan (2023), https://conwaylife.com/wiki/Glider_to_block",
    ]), end="")
