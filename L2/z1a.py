import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from random import randrange

DIRECTORY_NAME = f'digits'
OTHER_DIRECTORY_NAME = f'other_digits'


def create_and_train_model(number_of_epochs=6):
    data_set = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = data_set.load_data()

    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
    model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(x=x_train, y=y_train, epochs=number_of_epochs)

    _, accuracy = model.evaluate(x=x_test, y=y_test)

    model.save('digits_recognition.model')

    print(f'Współczynnik rozpoznawalności dla modelu : {accuracy}')


def make_prediction():
    data_set = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = data_set.load_data()

    test_data_set = tf.keras.utils.normalize(x_test, axis=1)

    saved_model = tf.keras.models.load_model('digits_recognition.model')

    predictions = saved_model.predict([test_data_set])

    index = randrange(0, len(predictions) - 1)

    print(f'Wylosowana cyfra : {np.argmax(predictions[index])}')
    print(f'Odpowiadający jej obrazek: ')

    plt.imshow(test_data_set[index], cmap='gray')
    plt.show()


def read_and_transform_custom_images(flag=False):
    created_model = tf.keras.models.load_model('digits_recognition.model')
    number_of_samples = 30
    correctly_recognized_digits = 0

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

            else:
                if j % 3 == 0:
                    image_file_name += f'{OTHER_DIRECTORY_NAME}/{i}2a.png'
                elif j % 3 == 1:
                    image_file_name += f'{OTHER_DIRECTORY_NAME}/{i}2b.png'
                elif j % 3 == 2:
                    image_file_name += f'{OTHER_DIRECTORY_NAME}/{i}2c.png'

            image = cv.imread(image_file_name)[:, :, 0]
            image = np.invert(np.array([image]))

            thresh, image = cv.threshold(image, 125, 255, cv.THRESH_BINARY)

            prediction = created_model.predict(image)

            if np.argmax(prediction) == i:
                correctly_recognized_digits += 1

            print(f'Dany obrazek ({image_file_name}) został sklasyfikowany jako: {np.argmax(prediction)}')

            print(f'Wyświetlam obrazek {image_file_name} !')

            plt.imshow(image[0], cmap=plt.cm.binary)
            plt.show()

    print(f'Skuteczność modelu : {correctly_recognized_digits / number_of_samples}')


def main():
    print(f'> Witaj w programie do badania sieci neuronowej rozpoznającej cyfry 0-9 !')

    while True:
        command = input(f'> Wybierz akcję (a/b/c/d/e): ')

        if str(command) == 'a':
            number_of_epochs = input(f'> Podaj liczbę epok: ')

            try:
                number_of_epochs = int(number_of_epochs)

                if number_of_epochs < 0:
                    number_of_epochs = (-1) * number_of_epochs

                create_and_train_model(number_of_epochs)
            except ValueError:
                print(f'> Błąd ! Liczba epok powinna być liczbą naturalną !')
        elif str(command) == 'b':
            make_prediction()
        elif str(command) == 'c':
            read_and_transform_custom_images()
        elif str(command) == 'd':
            read_and_transform_custom_images(True)
        elif str(command) == 'e':
            print(f'> Program kończy pracę...')
            break
        else:
            print(f'> Nieznana akcja - spróbuj ponownie...')


main()
