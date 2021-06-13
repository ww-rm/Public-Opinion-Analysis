from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from .gendata import gen_kg


def read_kgdata(filepath) -> list:
    with Path(filepath).open("r", encoding="utf8") as f:
        sents = f.readlines()
    sents = [sent.strip() for sent in sents]
    return sents


def run(in_dir="./data/hotspot/daily/knowledge/", out_dir="./data/kg"):
    """
    Args:
        in_dir: input files directory, txt
        out_dir: output files directory, txt
    """
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    today_date = datetime.now()
    for i in range(7):
        date = today_date - timedelta(days=i)
        files = in_dir.glob("{}-[0-9].txt".format(date.strftime("%Y-%m-%d")))
        for filepath in files:
            sents = read_kgdata(filepath)
            kg_result = gen_kg(sents)
            kg_result.to_csv(
                out_dir.joinpath(filepath.name).as_posix(),
                sep="\t", index=False, header=False
            )
