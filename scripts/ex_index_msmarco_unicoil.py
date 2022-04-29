import os

from codecarbon import track_emissions


@track_emissions(offline=True, country_iso_code="AUS", project_name="uniCOIL Indexing")
def run():
    os.system(f'python -m pyserini.index -collection JsonVectorCollection \
 -input data/collections/msmarco-passage-unicoil-b8/ \
 -index data/index/lucene-index.msmarco-passage.unicoil-b8 \
 -generator DefaultLuceneDocumentGenerator -impact -pretokenized \
 -threads 12')


if __name__ == '__main__':
    run()
