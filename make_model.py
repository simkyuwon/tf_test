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
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        batch_size=64,
        color_mode="grayscale",
        subset="training",
        seed=random.randrange(1, 100000),
        shuffle=10000,
        image_size=(240, 320))

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        batch_size=64,
        color_mode="grayscale",
        subset="validation",
        seed=random.randrange(1, 100000),
        image_size=(240, 320))

    model = tf.keras.Sequential([
        layers.Rescaling(1./255),
        layers.Conv2D(16, (5, 5), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(16, (5, 5), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(32, (5, 5), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPool2D(),
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dense(5, activation='softmax')
    ])

    model.compile(
        optimizer="adam",
        loss='sparse_categorical_crossentropy',
        metrics=["accuracy"]
    )

    callback_func = None

    if save_log:
        log_dir = f"logs/{datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.%f')}"
        callback_func = [tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=5,
        callbacks=callback_func
    )

    model.summary()

    model.save('saved_model/model')

    if save_tflite:
        save_tflite_model()


if __name__ == "__main__":
    make_model(save_tflite=True)
