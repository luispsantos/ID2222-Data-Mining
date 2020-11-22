import gzip
from os.path import join


def read_snap_dataset(dataset_file):
    # SNAP datasets: https://snap.stanford.edu/data/
    dataset_path = join('datasets', dataset_file)

    # read the gzip file containing the dataset
    with gzip.open(dataset_path) as dataset_gzip:
        # iterate through each line in the file
        for line in dataset_gzip:
            line = line.decode('utf-8')
            elems = line.split()

            if elems[0] == '#':
                continue  # this line is a comment, we can skip it
            else:
                src_node, dst_node = int(elems[0]), int(elems[1])
                yield src_node, dst_node


if __name__ == '__main__':
    dataset_file = 'web-NotreDame.txt.gz'
    for src_node, dst_node in read_snap_dataset(dataset_file):
        print(f'edge: {src_node} -> {dst_node}')
