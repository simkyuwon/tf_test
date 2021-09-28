import tensorflow as tf
from tensorflow.keras import layers
import pathlib
import random
import datetime

data_dir = pathlib.Path("./data/TRAIN_DIR")


def save_tflite_model():
    converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/model")
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    tflite_model = converter.convert()

    model_file = pathlib.Path('model.tflite')
    model_file.write_bytes(tflite_model)


def make_model(save_tflite=False, save_log=False):
    train_data_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        brightness_range=[0.8, 1.0],
        shear_range=5,
        fill_mode='constant',
        cval=0
    )

    validation_data_generator = tf.keras.preprocessing.image.ImageDataGenerator()

    train_ds = train_data_generator.flow_from_directory(
        f'{data_dir}/TRAIN',
        target_size=(240, 320),
        batch_size=64,
        color_mode='grayscale',
        seed=random.randrange(1, 1000)
    )

    val_ds = validation_data_generator.flow_from_directory(
        f'{data_dir}/VALIDATION',
        target_size=(240, 320),
        batch_size=64,
        color_mode='grayscale',
        seed=random.randrange(1, 1000)
    )

    model = tf.keras.Sequential([
        layers.Resizing(240, 320),
        layers.Rescaling(1. / 255),
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

    callback_func = None

    if save_log:
        log_dir = f"logs/{datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.%f')}"
        callback_func = [tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20,
        # callbacks=[tensorboard_callback]
    )

    model.summary()

    model.save('saved_model/model')

    if save_tflite:
        save_tflite_model()


if __name__ == "__main__":
    make_model(save_tflite=True)
