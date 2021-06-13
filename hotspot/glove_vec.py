import argparse
import json
import struct
from pathlib import Path

import numpy as np
from tqdm import tqdm


class PretrainedVector:
    """A dict like obj for pretrained vectors"""

    def __init__(self, wv_dir):
        wv_index_path = Path(wv_dir, "pretrained_wv.index.json")
        wv_path = Path(wv_dir, "pretrained_wv.vec.dat")
        self.index_table = None
        self.wv_dict = None
        with open(wv_index_path, "r", encoding="utf8") as f:
            self.index_table = json.load(f)
        self.wv_dict = open(wv_path, "rb")

    def __del__(self):
        self.wv_dict.close()

    def __contains__(self, item: str):
        return item in self.index_table

    def __getitem__(self, item: str):
        index = self.index_table.get(item)
        if index is None:
            raise KeyError("No such key in index table.")
        else:
            self.wv_dict.seek(4*300*index, 0)
            vec = struct.unpack("f"*300, self.wv_dict.read(1200))
            return np.array(vec)

    def get(self, item: str, default=None):
        try:
            value = self[item]
        except KeyError:
            return default
        else:
            return value


def extract(vector_file: str, output_dir: str):
    index_data = {}

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_index_file = Path(output_dir, "pretrained_wv.index.json")
    output_vecdata_file = Path(output_dir, "pretrained_wv.vec.dat")

    with open(vector_file, "r", encoding="utf8") as in_f:
        with output_vecdata_file.open("wb") as out_f:
            cur_i = 0
            for line in tqdm(in_f):
                line = line.strip("\n").split(" ")
                if len(line) != 301:
                    print(line[0])
                    continue

                index_data[line[0]] = cur_i
                out_f.write(struct.pack("f"*300, *list(map(float, line[1:]))))
                cur_i += 1

    with output_index_file.open("w", encoding="utf8") as f:
        json.dump(index_data, f, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("vector_file")
    parser.add_argument("output_dir")

    args = parser.parse_args()
    extract(args.vector_file, args.output_dir)
