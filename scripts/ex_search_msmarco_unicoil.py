import os

from codecarbon import track_emissions


@track_emissions(offline=True, country_iso_code="AUS", project_name="uniCOIL Search")
def run():
    os.system(f'python -m pyserini.search --topics msmarco-passage-dev-subset \
                              --encoder castorini/unicoil-msmarco-passage \
                              --index data/index/lucene-index.msmarco-passage.unicoil-b8 \
                              --output runs/run.msmarco-passage.unicoil-b8.tsv \
                              --hits 1000 --batch 36 --threads 12 \
                              --impact \
                              --output-format msmarco')


if __name__ == '__main__':
    run()
