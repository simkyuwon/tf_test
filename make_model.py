import tensorflow as tf
from tensorflow.keras import layers
import pathlib
import random
import datetime


direction_data_dir = pathlib.Path("./data/DIRECTION_DIR")
section_data_dir = pathlib.Path("./data/SECTION_DIR")


def make_model(direction=True, section=True):
    if direction:
        train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=10,
            brightness_range=[0.8, 1.0],
            shear_range=5,
            fill_mode='constant',
            cval=0
        )

        validation_data_generator = tf.keras.preprocessing.image.ImageDataGenerator()

        train_ds = train_data_generator.flow_from_directory(
            f'{direction_data_dir}/TRAIN',
            target_size=(240, 320),
            batch_size=64,
            color_mode='grayscale',
            seed=random.randrange(1, 1000)
        )

        val_ds = validation_data_generator.flow_from_directory(
            f'{direction_data_dir}/VALIDATION',
            target_size=(240, 320),
            batch_size=64,
            color_mode='grayscale',
            seed=random.randrange(1, 1000)
        )

        model = tf.keras.Sequential([
            layers.Resizing(240, 320),
            layers.Rescaling(1. / 255),
            layers.Lambda(lambda x: 1 - x),
            layers.Conv2D(30, (11, 11), activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(30, (9, 9), activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(40, (7, 7), activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(40, (5, 5), activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(50, (3, 3), activation='relu'),
            layers.MaxPool2D(),
            layers.Flatten(),
            layers.Dense(120, activation='relu'),
            layers.Dense(6, activation='softmax')
        ])

        model.compile(
            optimizer="adam",
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=20,
        )

        model.summary()

        model.save('saved_model/direction_model')
        converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/direction_model")
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
        tflite_model = converter.convert()

        model_file = pathlib.Path('direction_model.tflite')
        model_file.write_bytes(tflite_model)

    if section:
        train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=15,
            brightness_range=[0.7, 1.2],
            shear_range=10,
            zoom_range=0.2,
            fill_mode='constant',
            cval=100
        )

        validation_data_generator = tf.keras.preprocessing.image.ImageDataGenerator()

        train_ds = train_data_generator.flow_from_directory(
            f'{section_data_dir}/TRAIN',
            target_size=(64, 64),
            batch_size=64,
            color_mode='rgb',
            seed=random.randrange(1, 1000)
        )

        val_ds = validation_data_generator.flow_from_directory(
            f'{section_data_dir}/VALIDATION',
            target_size=(64, 64),
            batch_size=64,
            color_mode='rgb',
            seed=random.randrange(1, 1000)
        )

        model = tf.keras.Sequential([
            layers.Resizing(64, 64),
            layers.Rescaling(1. / 255),
            layers.Conv2D(32, (7, 7), padding='same', activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(32, (5, 5), padding='same', activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPool2D(),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPool2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(5, activation='softmax')
        ])

        model.compile(
            optimizer="adam",
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"]
        )

        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=10,
        )

        model.summary()

        model.save('saved_model/section_model')
        converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/section_model")
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
        tflite_model = converter.convert()

        model_file = pathlib.Path('section_model.tflite')
        model_file.write_bytes(tflite_model)


if __name__ == "__main__":
    make_model(direction=False)
