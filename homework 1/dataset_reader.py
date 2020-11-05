import itertools
import jsonlines


def read_webhose_dataset(inputfile, num_docs):
    docs = []
    with jsonlines.open(input_file) as reader:
        # read only the first `num_docs` documents
        for doc in itertools.islice(reader, num_docs):
            docs.append(doc['text'])

    return docs


num_docs = 10
input_file = '16125_webhose_2020_02_2eb7927911a2ee90f88fb57c2721c4ac_0000001.json'

docs = read_webhose_dataset(input_file, num_docs)
print(docs)
