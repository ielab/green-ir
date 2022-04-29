import os

from codecarbon import track_emissions


@track_emissions(offline=True, country_iso_code="AUS", project_name="BM25 Indexing (pyserini)")
def run():
    collection_dir = "data/raw/msmarco-pyserini"
    index_path = "data/index/msmarco-pyserini"
    os.system(f'python -m pyserini.index -collection JsonCollection ' +
              f'-generator DefaultLuceneDocumentGenerator -threads 1 ' +
              f'-input {collection_dir} -index {index_path}')


if __name__ == '__main__':
    run()
