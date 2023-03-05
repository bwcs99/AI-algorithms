import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import random
import cv2 as cv
from math import inf


DIRECTORY_NAME = f'digits'


def compute_inertia(data_set, centroids, clusters):
    distances = np.array([])
    for i in range(0, data_set.shape[0]):
        x = data_set[i]
        centroid = centroids[clusters[i]]

        distance = ((x - centroid) ** 2).sum(axis=0)

        distances = np.append(distances, distance)

    return distances.sum()


def stop_condition(old_inertia, current_inertia, number_of_iterations, max_iterations, epsilon):

    if old_inertia is None or current_inertia is None:
        return False

    elif abs(current_inertia - old_inertia) <= epsilon:
        return True

    elif number_of_iterations >= max_iterations:
        return True

    return False


def initialize_centroids(data_set, k, flag=False):
    indices = []
    centroids = np.array([])

    counter = 0

    while counter < k:

        if flag:
            idx = random.randint(0, data_set.shape[0] - 1)
        else:
            idx = random.randint(0, data_set.shape[0])

        if idx not in indices:
            indices.append(idx)
            centroids = np.append(centroids, data_set[idx])

            counter += 1

    return centroids.reshape(k, 784)


def reinitialize_randomly_given_cluster(data_set, clusters, centroids, k):
    random_index = random.randint(0, data_set.shape[0])

    clusters[random_index] = k
    centroids[k] = data_set[random_index]


def compute_new_centroids(data_set, clusters, centroids, k):
    counts = np.zeros(k, dtype='int32')
    sums_matrix = np.repeat(np.array([np.zeros(784)]), [k], axis=0)

    for i in range(0, data_set.shape[0]):
        counts[clusters[i]] = counts[clusters[i]] + 1
        sums_matrix[clusters[i]] = sums_matrix[clusters[i]] + data_set[i]

    for i in range(0, k):
        if counts[i] == 0:
            reinitialize_randomly_given_cluster(data_set, clusters, centroids, i)
            continue

        new_centroid = sums_matrix[i] / counts[i]
        centroids[i] = new_centroid

    return centroids


def compute_labels_for_data_set(data_set, clusters, centroids, k):
    for i in range(0, data_set.shape[0]):
        current_vector_matrix = np.repeat(np.array([data_set[i]]), [k], axis=0)

        squared_distances_vector = ((current_vector_matrix - centroids) ** 2).sum(axis=1)

        cluster_number = np.where(squared_distances_vector == squared_distances_vector.min())[0][0]

        clusters[i] = cluster_number

    return clusters


def k_means_clustering(data_set, k, max_iterations, epsilon, flag=False):
    clusters = np.zeros(data_set.shape[0], dtype='int32')

    centroids = initialize_centroids(data_set, k, flag)
    clusters = compute_labels_for_data_set(data_set, clusters, centroids, k)

    current_inertia = compute_inertia(data_set, centroids, clusters)

    number_of_iterations, old_inertia = 0, None

    while not stop_condition(old_inertia, current_inertia, number_of_iterations, max_iterations, epsilon):
        number_of_iterations += 1

        old_inertia = current_inertia

        centroids = compute_new_centroids(data_set, clusters, centroids, k)
        clusters = compute_labels_for_data_set(data_set, clusters, centroids, k)

        current_inertia = compute_inertia(data_set, centroids, clusters)

    return centroids, clusters


def read_data_set():
    data_set = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = data_set.load_data()

    x_train = x_train.reshape(len(x_train), -1)

    return x_train, y_train


def read_and_transform_custom_images(flag=False):
    data_set = []
    answers = np.array([], dtype="int32")
    for i in range(0, 10):
        for j in range(0, 3):
            image_file_name = f''

            if not flag:
                if j % 3 == 0:
                    image_file_name += f'{DIRECTORY_NAME}/{i}a.png'
                elif j % 3 == 1:
                    image_file_name += f'{DIRECTORY_NAME}/{i}b.png'
                elif j % 3 == 2:
                    image_file_name += f'{DIRECTORY_NAME}/{i}c.png'

            image = cv.imread(image_file_name)[:, :, 0]
            image = np.invert(np.array([image]))

            thresh, image = cv.threshold(image, 125, 255, cv.THRESH_BINARY)

            data_set.append(image)
            answers = np.append(answers, i)

    data_set = np.array(data_set)
    data_set = data_set.reshape(len(data_set), -1)

    return data_set, answers


def display_centroids(centroids, k):
    for i in range(0, k):
        centroid = centroids[i].reshape(28, 28)

        print('Centroid', i)

        plt.imshow(centroid, cmap='gray')
        plt.show()


def generate_stats_matrix(y_test, clusters, k):
    number_of_elements_in_clusters = [0 for _ in range(0, k)]
    for i in range(0, y_test.shape[0]):
        number_of_elements_in_clusters[clusters[i]] += 1

    stats_matrix = [[0 for _ in range(0, k)] for _ in range(0, 10)]

    for i in range(0, y_test.shape[0]):
        number = y_test[i]
        cluster = clusters[i]

        stats_matrix[number][cluster] += 1

    for i in range(0, k):
        for j in range(0, 10):
            if number_of_elements_in_clusters[i] == 0:
                stats_matrix[j][i] = float(0)
            else:
                stats_matrix[j][i] = stats_matrix[j][i]/number_of_elements_in_clusters[i]

    return stats_matrix


def main():
    k = int(input('Podaj liczbę klastrów: '))
    max_iterations = int(input('Podaj maksymalną liczbę iteracji: '))
    epsilon = float(input('Podaj epsilon: '))

    # data_set, answers = read_data_set()

    data_set, answers = read_and_transform_custom_images()

    centroids, clusters = k_means_clustering(data_set, k, max_iterations, epsilon, True)

    inertia = compute_inertia(data_set, centroids, clusters)

    print('Inercja klasteryzacji: ', inertia)

    display_centroids(centroids, k)

    print(f'Macierz 10/{k}: ')
    print(generate_stats_matrix(answers, clusters, k))


main()
