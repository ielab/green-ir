import os

from codecarbon import track_emissions


@track_emissions(offline=True, country_iso_code="AUS", project_name="BM25 Search (pyserini)")
def run():
    os.system("python -m pyserini.search --topics msmarco-passage-dev-subset \
 --index data/index/msmarco-pyserini \
 --output runs/run.msmarco-passage.bm25tuned.txt \
 --bm25 --output-format msmarco --hits 1000 --k1 0.82 --b 0.68")


if __name__ == '__main__':
    run()
