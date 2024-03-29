import numpy as np
import pandas as pd
import os
import keras
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
#from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras import regularizers
from sklearn.model_selection import train_test_split
import cv2
import matplotlib.pyplot as plt
#import seaborn as sns
import time
from resizeimage import resizeimage
from PIL import Image

# THE FOLLOWING METHOD IS USED FOR PREVIEWING 


def preview_unique():
    size_img = 64, 64
    images_for_plot = []  # list of cv2 image objects
    labels_for_plot = []  # list of labels
    for folder in os.listdir(train_dir):  # get all directories in train_dir
        for file in os.listdir(train_dir + '/' + folder):  # get all files in sub directories
            filepath = train_dir + '/' + folder + '/' + file
            image = cv2.imread(filepath)
            final_img = cv2.resize(image, size_img)
            final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            images_for_plot.append(final_img)
            labels_for_plot.append(folder)  # folder name is the label name!
            break  # we only need ONE image per folder for the preview
    return images_for_plot, labels_for_plot


def preview_images(fig, image, label, row, col, index):
    fig.add_subplot(row, col, index)
    plt.axis('off')
    plt.imshow(image)
    plt.title(label)
    print("preview images now")
    return


def label_data():
    images = []
    labels = []
    size = 64, 64
    print("LOADING DATA FROM : ", end = "")
    for folder in os.listdir(train_dir):
        print(folder, end = ' | ')
        for image in os.listdir(train_dir + "/" + folder): # this loop programatically labels all data with an integer class
            temp_img = cv2.imread(train_dir + '/' + folder + '/' + image)
            temp_img = cv2.resize(temp_img, size)
            images.append(temp_img)
            if folder == 'A':
                labels.append(labels_dict['A'])
            elif folder == 'B':
                labels.append(labels_dict['B'])
            elif folder == 'C':
                labels.append(labels_dict['C'])
            elif folder == 'D':
                labels.append(labels_dict['D'])
            elif folder == 'E':
                labels.append(labels_dict['E'])
            elif folder == 'F':
                labels.append(labels_dict['F'])
            elif folder == 'G':
                labels.append(labels_dict['G'])
            elif folder == 'H':
                labels.append(labels_dict['H'])
            elif folder == 'I':
                labels.append(labels_dict['I'])
            elif folder == 'J':
                labels.append(labels_dict['J'])
            elif folder == 'K':
                labels.append(labels_dict['K'])
            elif folder == 'L':
                labels.append(labels_dict['L'])
            elif folder == 'M':
                labels.append(labels_dict['M'])
            elif folder == 'N':
                labels.append(labels_dict['N'])
            elif folder == 'O':
                labels.append(labels_dict['O'])
            elif folder == 'P':
                labels.append(labels_dict['P'])
            elif folder == 'Q':
                labels.append(labels_dict['Q'])
            elif folder == 'R':
                labels.append(labels_dict['R'])
            elif folder == 'S':
                labels.append(labels_dict['S'])
            elif folder == 'T':
                labels.append(labels_dict['T'])
            elif folder == 'U':
                labels.append(labels_dict['U'])
            elif folder == 'V':
                labels.append(labels_dict['V'])
            elif folder == 'W':
                labels.append(labels_dict['W'])
            elif folder == 'X':
                labels.append(labels_dict['X'])
            elif folder == 'Y':
                labels.append(labels_dict['Y'])
            elif folder == 'Z':
                labels.append(labels_dict['Z'])
            elif folder == 'space':
                labels.append(labels_dict['space'])
            elif folder == 'del':
                labels.append(labels_dict['del'])
            elif folder == 'nothing':
                labels.append(labels_dict['nothing'])

    images = np.array(images) # numpy array 
    images = images.astype('float32')/255.0 # normalizes image pixels to range [0, 1] for processing

    templabels = labels

    labels = keras.utils.to_categorical(labels)

    X_train, X_test, Y_train, Y_test = train_test_split(images, labels, test_size=0.05)  # automatically splits into training and testing set!
    # note: parameter test_size = the percentage of your data that is in the test set
    # x is vector of what you know (images) and y is what you're trying to predict (class name, A, B, C, etc)
    # y test and y train stores all actual data. x data is used for training

    print() # empty new line for spacing
    print('Loaded', len(X_train),'images for training,','Train data shape =',X_train.shape)
    print('Loaded', len(X_test),'images for testing','Test data shape =',X_test.shape)

    return X_train, X_test, Y_train, Y_test, templabels


def create_model():
    print("CREATING MODEL NOW")
    model = Sequential()
    # Conv2D connects part of image to another part of the image somewhere else.
    model.add(Conv2D(16, kernel_size=[3, 3], padding='same', activation='relu', input_shape=(64, 64, 3)))
    print("FIRST LAYER CREATED")
    model.add(Conv2D(32, kernel_size=[3, 3], padding='same', activation='relu'))
    print("SECOND LAYER CREATED")
    # rectified linear unit used by activation function. normalizes
    model.add(MaxPool2D(pool_size=[3, 3]))
    print("THIRD LAYER CREATED")

    model.add(Conv2D(32, kernel_size=[3, 3], padding='same', activation='relu'))
    print("FOURTH LAYER CREATED")
    model.add(Conv2D(64, kernel_size=[3, 3], padding='same', activation='relu'))
    print("FIFTH LAYER CREATED")
    model.add(MaxPool2D(pool_size=[3, 3]))
    print("SIXTH LAYER CREATED")

    model.add(Conv2D(128, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(Conv2D(256, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=[3, 3]))

    model.add(BatchNormalization())

    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(512, activation = 'relu', kernel_regularizer = regularizers.l2(0.001)))
    model.add(Dense(29, activation = 'softmax'))

    model.compile(optimizer = 'adam', loss = keras.losses.categorical_crossentropy, metrics = ["accuracy"])
    # loss function

    print("MODEL CREATED")
    model.summary()

    return model

# training
def fit_model(): 
    model_hist = model.fit(X_train, Y_train, batch_size=64, epochs=6, validation_split=0.1)
    # split training into smaller sanity check set with validation_split
    return model_hist


def plot_accuracy(y):
    if(y == True):
        plt.plot(curr_model_hist.history['acc'])
        plt.plot(curr_model_hist.history['val_acc'])
        plt.legend(['train', 'test'], loc='lower right')
        plt.title('accuracy plot - train vs test')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.show()
    else:
        pass
    return


def plot_loss(y):
    if y == True:
        plt.plot(curr_model_hist.history['loss'])
        plt.plot(curr_model_hist.history['val_loss'])
        plt.legend(['training loss', 'validation loss'], loc = 'upper right')
        plt.title('loss plot - training vs vaidation')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.show()
    else:
        pass
    return


def load_test_data():
    images = []
    names = []
    size = 64, 64
    for image in os.listdir(test_dir):
        print("Loading", image + "...")
        temp = cv2.imread(test_dir + '/' + image)
        temp = cv2.resize(temp, size)
        images.append(temp)
        names.append(image)
    images = np.array(images)
    images = images.astype('float32')/255.0
    return images, names


def give_predictions(test_data, model):
    predictions_classes = []
    for image in test_data:
        image = image.reshape(1, 64, 64, 3)
        pred = model.predict_classes(image)
        predictions_classes.append(pred[0])
    return predictions_classes


def get_labels_for_plot(predictions):
    predictions_labels = []
    for i in range(len(predictions)):
        for ins in labels_dict:
            if predictions[i] == labels_dict[ins]:
                predictions_labels.append(ins)
                break
    return predictions_labels


def plot_image_1(fig, image, label, prediction, predictions_label, row, col, index):
    fig.add_subplot(row, col, index)
    plt.axis('off')
    plt.imshow(image)
    title = "prediction : [" + str(predictions_label) + "] "+ "\n" + label
    plt.title(title)
    return


def load_input_data():
    images = []
    names = []
    size = 64, 64
    for image in os.listdir(input_dir):
        if not image.endswith(".jpg"):
            continue
        temp = cv2.imread(input_dir + '/' + image)
        temp = cv2.resize(temp, size)
        #  image_path = os.path.join(path, 'resized.jpg')
        #  cv2.imwrite(image_path, temp)
        images.append(temp)
        names.append(image)
    images = np.array(images)
    images = images.astype('float32')/255.0
    return images, names


def reload_weights(filename):
    model = create_model()
    model.load_weights(filename)
    return model


def bsl_output(outputlist):
    if outputList[0] == 0:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/a.png')
        img.show()
    elif outputList[0] == 1:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/b.png')
        img.show()
    elif outputList[0] == 2:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/c.png')
        img.show()
    elif outputList[0] == 3:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/d.png')
        img.show()
    elif outputList[0] == 4:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/e.png')
        img.show()
    elif outputList[0] == 5:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/f.png')
        img.show()
    elif outputList[0] == 6:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/g.png')
        img.show()
    elif outputList[0] == 7:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/h.png')
        img.show()
    elif outputList[0] == 8:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/i.png')
        img.show()
    elif outputList[0] == 9:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/j.png')
        img.show()
    elif outputList[0] == 10:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/k.png')
        img.show()
    elif outputList[0] == 11:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/l.png')
        img.show()
    elif outputList[0] == 12:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/m.png')
        img.show()
    elif outputList[0] == 13:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/n.png')
        img.show()
    elif outputList[0] == 14:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/o.png')
        img.show()
    elif outputList[0] == 15:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/p.png')
        img.show()
    elif outputList[0] == 16:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/q.png')
        img.show()
    elif outputList[0] == 17:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/r.png')
        img.show()
    elif outputList[0] == 18:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/s.png')
        img.show()
    elif outputList[0] == 19:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/t.png')
        img.show()
    elif outputList[0] == 20:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/u.png')
        img.show()
    elif outputList[0] == 21:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/v.png')
        img.show()
    elif outputList[0] == 22:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/w.png')
        img.show()
    elif outputList[0] == 23:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/x.png')
        img.show()
    elif outputList[0] == 24:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/y.png')
        img.show()
    elif outputList[0] == 25:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/z.png')
        img.show()

# TRAINING AND TEACHING  
"""
print(os.listdir("/Users/Vani/PycharmProjects/ASLConverter/input"))

train_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/asl_alphabet_train'
test_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/asl_alphabet_test'

images_for_plot, labels_for_plot = preview_unique()
print("unique_labels = ", labels_for_plot)

fig = plt.figure(figsize=(15, 15))

image_index = 0
row = 5
col = 6
print("about to preview")
for i in range(1, (row*col)):
    preview_images(fig, images_for_plot[image_index], labels_for_plot[image_index], row, col, i) # preview the loaded images
    image_index += 1
print("done with for loop")
plt.show()  # shows the actual plot - must be called to see anything!
print("done previewing")

labels_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
                    'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,'V':21,'W':22,'X':23,'Y':24,
                   'Z': 25,'space':26,'del':27,'nothing':28} # converts labels from string to int

print("data about to be labeled")
X_train, X_test, Y_train, Y_test, labels = label_data()
print("data is labeled")

labelsdf = pd.DataFrame() # pd = pandas. It's like excel, but for python!
labelsdf["labels"] = labels # create a column called "labels" and fill it with our labels data
labelsdf["labels"].value_counts().plot(kind="bar", figsize=(12, 3))  # plot a graph of how much of each label we have

print("model about to be created")
model = create_model()
curr_model_hist = fit_model()

plot_accuracy(True)
plot_loss(True)

evaluate_metrics = model.evaluate(X_test, Y_test)  #how many times are we right
print("\nEvaluation Accuracy = ", "{:.2f}%".format(evaluate_metrics[1]*100), "\nEvaluation loss = " ,"{:.6f}".format(evaluate_metrics[0]))

test_images, test_img_names = load_test_data()

predictions = give_predictions(test_images, model)

predictions_labels_plot = get_labels_for_plot(predictions)

predfigure = plt.figure(figsize = (13,13))

image_index = 0
row = 5
col = 6
for i in range(1,(row*col-1)):
    plot_image_1(predfigure, test_images[image_index], test_img_names[image_index], predictions[image_index], predictions_labels_plot[image_index], row, col, i)
    image_index = image_index + 1
plt.show()

model.save('Final_model_asl.h5')
"""

# inputs images
wait_time = 0.6
video = cv2.VideoCapture(0)
print("Camera exposure: {:.2}s".format(wait_time))
time.sleep(wait_time)
_, frame = video.read()
cv2.flip(frame, 0)
cv2.imshow("Capturing", frame)
# img = cv2.imread('1.jpg', 1)
cv2.waitKey(0)
video.release()
path = '/Users/Vani/PycharmProjects/ASLConverter/input/camera_input'
size_img = 200, 200
final_img = cv2.resize(frame, size_img)
name = 0
img_path = os.path.join(path, 'first.jpg')
cv2.imwrite(img_path, frame)
print("Image saved to", img_path)

# runs images through neural network
model_implement = reload_weights('Final_model_asl.h5')
input_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/camera_input'
outputImages, outputLabels = load_input_data()  # formats input data
outputList = give_predictions(outputImages, model_implement)
print(outputList)
bsl_output(outputList)


"""
import numpy as np
import pandas as pd
import os
import keras
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
#from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras import regularizers
from sklearn.model_selection import train_test_split
import cv2
import matplotlib.pyplot as plt
#import seaborn as sns
import time
from resizeimage import resizeimage
from PIL import Image

# this method is used just for previewing!


def preview_unique():
    size_img = 64, 64
    images_for_plot = []  # list of cv2 image objects
    labels_for_plot = []  # list of labels
    for folder in os.listdir(train_dir):  # get all directories in train_dir
        for file in os.listdir(train_dir + '/' + folder):  # get all files in sub directories
            filepath = train_dir + '/' + folder + '/' + file
            image = cv2.imread(filepath)
            final_img = cv2.resize(image, size_img)
            final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            images_for_plot.append(final_img)
            labels_for_plot.append(folder)  # folder name is the label name!
            break  # we only need ONE image per folder for the preview
    return images_for_plot, labels_for_plot


def preview_images(fig, image, label, row, col, index):
    fig.add_subplot(row, col, index)
    plt.axis('off')
    plt.imshow(image)
    plt.title(label)
    print("preview images now")
    return


def label_data():
    images = []
    labels = []
    size = 64, 64
    print("LOADING DATA FROM : ", end = "")
    for folder in os.listdir(train_dir):
        print(folder, end = ' | ')
        for image in os.listdir(train_dir + "/" + folder): # this loop programatically labels all data with an integer class
            temp_img = cv2.imread(train_dir + '/' + folder + '/' + image)
            temp_img = cv2.resize(temp_img, size)
            images.append(temp_img)
            if folder == 'A':
                labels.append(labels_dict['A'])
            elif folder == 'B':
                labels.append(labels_dict['B'])
            elif folder == 'C':
                labels.append(labels_dict['C'])
            elif folder == 'D':
                labels.append(labels_dict['D'])
            elif folder == 'E':
                labels.append(labels_dict['E'])
            elif folder == 'F':
                labels.append(labels_dict['F'])
            elif folder == 'G':
                labels.append(labels_dict['G'])
            elif folder == 'H':
                labels.append(labels_dict['H'])
            elif folder == 'I':
                labels.append(labels_dict['I'])
            elif folder == 'J':
                labels.append(labels_dict['J'])
            elif folder == 'K':
                labels.append(labels_dict['K'])
            elif folder == 'L':
                labels.append(labels_dict['L'])
            elif folder == 'M':
                labels.append(labels_dict['M'])
            elif folder == 'N':
                labels.append(labels_dict['N'])
            elif folder == 'O':
                labels.append(labels_dict['O'])
            elif folder == 'P':
                labels.append(labels_dict['P'])
            elif folder == 'Q':
                labels.append(labels_dict['Q'])
            elif folder == 'R':
                labels.append(labels_dict['R'])
            elif folder == 'S':
                labels.append(labels_dict['S'])
            elif folder == 'T':
                labels.append(labels_dict['T'])
            elif folder == 'U':
                labels.append(labels_dict['U'])
            elif folder == 'V':
                labels.append(labels_dict['V'])
            elif folder == 'W':
                labels.append(labels_dict['W'])
            elif folder == 'X':
                labels.append(labels_dict['X'])
            elif folder == 'Y':
                labels.append(labels_dict['Y'])
            elif folder == 'Z':
                labels.append(labels_dict['Z'])
            elif folder == 'space':
                labels.append(labels_dict['space'])
            elif folder == 'del':
                labels.append(labels_dict['del'])
            elif folder == 'nothing':
                labels.append(labels_dict['nothing'])

    images = np.array(images) # numpy array for meme magic
    images = images.astype('float32')/255.0 # normalizes image pixels to range [0, 1]

    templabels = labels

    labels = keras.utils.to_categorical(labels)

    X_train, X_test, Y_train, Y_test = train_test_split(images, labels, test_size=0.05)  # automatically splits into train and test set!
    # note: parameter test_size = the percentage of your data that is in the test set
    # x is vector of what you know (images) and y is what you're trying to predict (class name, A, B,  C)
    # y test and y train stores all actual data. x data is used for training

    print() # just prints an empty new line for spacing
    print('Loaded', len(X_train),'images for training,','Train data shape =',X_train.shape)
    print('Loaded', len(X_test),'images for testing','Test data shape =',X_test.shape)

    return X_train, X_test, Y_train, Y_test, templabels


def create_model():
    print("CREATING MODEL NOW")
    model = Sequential()
    # see what Conv2D (connects part of image to another part of the image somewhere else.
    # not connected to the whole thing, every point doesn't connect to every other. the parameters?
    model.add(Conv2D(16, kernel_size=[3, 3], padding='same', activation='relu', input_shape=(64, 64, 3)))
    print("FIRST LAYER CREATED")
    model.add(Conv2D(32, kernel_size=[3, 3], padding='same', activation='relu'))
    print("SECOND LAYER CREATED")
    # rectified linear unit used by activation function. normalizes
    model.add(MaxPool2D(pool_size=[3, 3]))
    print("THIRD LAYER CREATED")

    model.add(Conv2D(32, kernel_size=[3, 3], padding='same', activation='relu'))
    print("FOURTH LAYER CREATED")
    model.add(Conv2D(64, kernel_size=[3, 3], padding='same', activation='relu'))
    print("FIFTH LAYER CREATED")
    model.add(MaxPool2D(pool_size=[3, 3]))
    print("SIXTH LAYER CREATED")

    model.add(Conv2D(128, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(Conv2D(256, kernel_size=[3, 3], padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=[3, 3]))

    model.add(BatchNormalization())

    model.add(Flatten())
    model.add(Dropout(0.5))
    model.add(Dense(512, activation = 'relu', kernel_regularizer = regularizers.l2(0.001)))
    model.add(Dense(29, activation = 'softmax'))

    model.compile(optimizer = 'adam', loss = keras.losses.categorical_crossentropy, metrics = ["accuracy"])
    # loss function

    print("MODEL CREATED")
    model.summary()

    return model


def fit_model(): # training
    model_hist = model.fit(X_train, Y_train, batch_size=64, epochs=6, validation_split=0.1)
    # split training into smaller sanity check set with validation_split
    return model_hist


def plot_accuracy(y):
    if(y == True):
        plt.plot(curr_model_hist.history['acc'])
        plt.plot(curr_model_hist.history['val_acc'])
        plt.legend(['train', 'test'], loc='lower right')
        plt.title('accuracy plot - train vs test')
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.show()
    else:
        pass
    return


def plot_loss(y):
    if y == True:
        plt.plot(curr_model_hist.history['loss'])
        plt.plot(curr_model_hist.history['val_loss'])
        plt.legend(['training loss', 'validation loss'], loc = 'upper right')
        plt.title('loss plot - training vs vaidation')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.show()
    else:
        pass
    return


def load_test_data():
    images = []
    names = []
    size = 64, 64
    for image in os.listdir(test_dir):
        print("Loading", image + "...")
        temp = cv2.imread(test_dir + '/' + image)
        temp = cv2.resize(temp, size)
        images.append(temp)
        names.append(image)
    images = np.array(images)
    images = images.astype('float32')/255.0
    return images, names


def give_predictions(test_data, model):
    predictions_classes = []
    for image in test_data:
        image = image.reshape(1, 64, 64, 3)
        pred = model.predict_classes(image)
        predictions_classes.append(pred[0])
    return predictions_classes


def get_labels_for_plot(predictions):
    predictions_labels = []
    for i in range(len(predictions)):
        for ins in labels_dict:
            if predictions[i] == labels_dict[ins]:
                predictions_labels.append(ins)
                break
    return predictions_labels


def plot_image_1(fig, image, label, prediction, predictions_label, row, col, index):
    fig.add_subplot(row, col, index)
    plt.axis('off')
    plt.imshow(image)
    title = "prediction : [" + str(predictions_label) + "] "+ "\n" + label
    plt.title(title)
    return


def load_input_data():
    images = []
    names = []
    size = 64, 64
    for image in os.listdir(input_dir):
        if not image.endswith(".jpg"):
            continue
        temp = cv2.imread(input_dir + '/' + image)
        temp = cv2.resize(temp, size)
        #  image_path = os.path.join(path, 'resized.jpg')
        #  cv2.imwrite(image_path, temp)
        images.append(temp)
        names.append(image)
    images = np.array(images)
    images = images.astype('float32')/255.0
    return images, names


def reload_weights(filename):
    model = create_model()
    model.load_weights(filename)
    return model


def bsl_output(outputlist):
    if outputList[0] == 0:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/a.png')
        img.show()
    elif outputList[0] == 1:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/b.png')
        img.show()
    elif outputList[0] == 2:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/c.png')
        img.show()
    elif outputList[0] == 3:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/d.png')
        img.show()
    elif outputList[0] == 4:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/e.png')
        img.show()
    elif outputList[0] == 5:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/f.png')
        img.show()
    elif outputList[0] == 6:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/g.png')
        img.show()
    elif outputList[0] == 7:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/h.png')
        img.show()
    elif outputList[0] == 8:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/i.png')
        img.show()
    elif outputList[0] == 9:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/j.png')
        img.show()
    elif outputList[0] == 10:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/k.png')
        img.show()
    elif outputList[0] == 11:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/l.png')
        img.show()
    elif outputList[0] == 12:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/m.png')
        img.show()
    elif outputList[0] == 13:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/n.png')
        img.show()
    elif outputList[0] == 14:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/o.png')
        img.show()
    elif outputList[0] == 15:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/p.png')
        img.show()
    elif outputList[0] == 16:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/q.png')
        img.show()
    elif outputList[0] == 17:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/r.png')
        img.show()
    elif outputList[0] == 18:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/s.png')
        img.show()
    elif outputList[0] == 19:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/t.png')
        img.show()
    elif outputList[0] == 20:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/u.png')
        img.show()
    elif outputList[0] == 21:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/v.png')
        img.show()
    elif outputList[0] == 22:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/w.png')
        img.show()
    elif outputList[0] == 23:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/x.png')
        img.show()
    elif outputList[0] == 24:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/y.png')
        img.show()
    elif outputList[0] == 25:
        img = Image.open('/Users/Vani/PycharmProjects/ASLConverter/input/BSL/z.png')
        img.show()

# trains and teaches 
"""
print(os.listdir("/Users/Vani/PycharmProjects/ASLConverter/input"))

train_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/asl_alphabet_train'
test_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/asl_alphabet_test'

images_for_plot, labels_for_plot = preview_unique()
print("unique_labels = ", labels_for_plot)

fig = plt.figure(figsize=(15, 15))

image_index = 0
row = 5
col = 6
print("about to preview")
for i in range(1, (row*col)):
    preview_images(fig, images_for_plot[image_index], labels_for_plot[image_index], row, col, i) # preview the loaded images
    image_index += 1
print("done with for loop")
plt.show()  # shows the actual plot - must be called to see anything!
print("done previewing")

labels_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
                    'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20,'V':21,'W':22,'X':23,'Y':24,
                   'Z': 25,'space':26,'del':27,'nothing':28} # converts labels from string to int

print("data about to be labeled")
X_train, X_test, Y_train, Y_test, labels = label_data()
print("data is labeled")

labelsdf = pd.DataFrame() # pd = pandas. It's like excel, but for python
labelsdf["labels"] = labels # create a column called "labels" and fill it with our labels data
labelsdf["labels"].value_counts().plot(kind="bar", figsize=(12, 3))  # plot a graph of how much of each label we have

print("model about to be created")
model = create_model()
curr_model_hist = fit_model()

plot_accuracy(True)
plot_loss(True)

evaluate_metrics = model.evaluate(X_test, Y_test)  #how many times am I right
print("\nEvaluation Accuracy = ", "{:.2f}%".format(evaluate_metrics[1]*100), "\nEvaluation loss = " ,"{:.6f}".format(evaluate_metrics[0]))

test_images, test_img_names = load_test_data()

predictions = give_predictions(test_images, model)

predictions_labels_plot = get_labels_for_plot(predictions)

predfigure = plt.figure(figsize = (13,13))

image_index = 0
row = 5
col = 6
for i in range(1,(row*col-1)):
    plot_image_1(predfigure, test_images[image_index], test_img_names[image_index], predictions[image_index], predictions_labels_plot[image_index], row, col, i)
    image_index = image_index + 1
plt.show()

model.save('Final_model_asl.h5')
"""

# inputs images
wait_time = 0.6
video = cv2.VideoCapture(0)
print("Camera exposure: {:.2}s".format(wait_time))
time.sleep(wait_time)
_, frame = video.read()
cv2.flip(frame, 0)
cv2.imshow("Capturing", frame)
# img = cv2.imread('1.jpg', 1)
cv2.waitKey(0)
video.release()
path = '/Users/Vani/PycharmProjects/ASLConverter/input/camera_input'
size_img = 200, 200
final_img = cv2.resize(frame, size_img)
name = 0
img_path = os.path.join(path, 'first.jpg')
cv2.imwrite(img_path, frame)
print("Image saved to", img_path)

# runs images through neural network
model_implement = reload_weights('Final_model_asl.h5')
input_dir = '/Users/Vani/PycharmProjects/ASLConverter/input/camera_input'
outputImages, outputLabels = load_input_data()  # formats input data
outputList = give_predictions(outputImages, model_implement)
print(outputList)
bsl_output(outputList)
"""

#COMPLETE! 
