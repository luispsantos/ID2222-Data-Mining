import matplotlib.pyplot as plt
from hw_classes import TriestBase, TriestImpr


def create_plot(triest_class, plot_title, dataset_file, m_values, triangle_count):
    triangle_estimates = []
    # compute a global triangle estimate for each M value
    for m in m_values:
        triest = triest_class(m)
        triangles = triest.algorithm(dataset_file)
        triangle_estimates.append(triangles)

    plt.title(plot_title)
    plt.plot(m_values, triangle_estimates)
    plt.xlabel('M'); plt.ylabel('Triangles')
    plt.axhline(triangle_count, linestyle='--')

    dataset_name = dataset_file.split('.')[0]
    plt.savefig(f'images/{plot_title.lower()}-{dataset_name.lower()}.jpg')
    plt.close()


if __name__ == '__main__':
    # dictionary format - dataset_file: (list of M values, true number of global triangles)
    dataset_files = {
        'web-Stanford.txt.gz': ([5000, 7500, 10000, 15000, 20000, 25000, 40000], 11329473),
        #'web-Google.txt.gz': ([5000, 7500, 10000, 15000, 20000, 25000, 40000], 13391903),
    }

    for dataset_file, (m_values, triangle_count) in dataset_files.items():
        create_plot(TriestBase, 'Triest-Base', dataset_file, m_values, triangle_count)
        create_plot(TriestImpr, 'Triest-Impr', dataset_file, m_values, triangle_count)
