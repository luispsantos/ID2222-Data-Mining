import zipfile
import itertools
import jsonlines


def read_webhose_dataset(dataset_file, num_docs=None):
    # webhose datasets: https://webhose.io/free-datasets/
    docs = []
    # read the zip file containing the webhose dataset
    with zipfile.ZipFile(dataset_file) as dataset_zipfile:
        # find the name of the JSON file inside the zip file
        json_filename = dataset_zipfile.namelist()[0]

        with dataset_zipfile.open(json_filename) as json_file:
            # each line in the file is a JSON document
            json_reader = jsonlines.Reader(json_file)

            # read only the initial num_docs documents
            for doc in itertools.islice(json_reader, num_docs):
                docs.append(doc['text'])

    return docs


dataset_file = 'datasets/covid-discussions.zip'
num_docs = 100

docs = read_webhose_dataset(input_file, num_docs)
print(docs)
