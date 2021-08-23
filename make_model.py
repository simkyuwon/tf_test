import tensorflow as tf
from tensorflow.keras import layers
import pathlib
import random

data_dir = pathlib.Path("./data/TRAIN_DIR")


def make_model():
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        batch_size=64,
        subset="training",
        seed=random.randrange(1, 100000),
        shuffle=10000,
        image_size=(64, 88))

    class_names = train_ds.class_names

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        batch_size=64,
        subset="validation",
        seed=random.randrange(1, 100000),
        image_size=(64, 88))

    model = tf.keras.Sequential([
        layers.Resizing(64, 88),
        layers.Rescaling(1. / 255),
        layers.Conv2D(30, (3, 3), dilation_rate=(2, 2), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(30, (3, 3), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(30, (3, 3), activation='relu'),
        layers.MaxPool2D(),
        layers.Conv2D(30, (3, 3), activation='relu'),
        layers.MaxPool2D(),
        layers.Flatten(),
        layers.Dense(100, activation='relu'),
        layers.Dense(5, activation='softmax')
    ])

    model.compile(
        optimizer="adam",
        loss='sparse_categorical_crossentropy',
        metrics=["accuracy"]
    )

    # log_dir = f"logs/{datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S.%f')}"
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=30,
        # callbacks=[tensorboard_callback]
    )

    model.summary()

    model.save('saved_model/model')
    # converter = tf.lite.TFLiteConverter.from_saved_model("saved_model/model")
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # converter.target_spec.supported_types = [tf.float16]
    # tflite_model = converter.convert()
    #
    # model_file = pathlib.Path('model.tflite')
    # model_file.write_bytes(tflite_model)


if __name__ == "__main__":
    make_model()
