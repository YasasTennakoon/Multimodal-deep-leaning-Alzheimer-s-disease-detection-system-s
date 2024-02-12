# -*- coding: utf-8 -*-
"""EnsembleLearningAppraoch

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hCNFQ8O9XIe_me9ixjDPCNe2icBpCmHz
"""

import numpy as np
import os
import keras
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from keras.models import Sequential
from PIL import Image
from keras.layers import Conv2D,Flatten,Dense,Dropout,BatchNormalization,MaxPooling2D
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

path1 = []
path2 = []
path3 = []
path4 = []
for dirname, _, filenames in os.walk('/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Non Demented'):
    for filename in filenames:
        path1.append(os.path.join(dirname, filename))

for dirname, _, filenames in os.walk('/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Mild Dementia'):
    for filename in filenames:
        path2.append(os.path.join(dirname, filename))

for dirname, _, filenames in os.walk('/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Moderate Dementia'):
    for filename in filenames:
        path3.append(os.path.join(dirname, filename))

for dirname, _, filenames in os.walk('/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Very mild Dementia'):
    for filename in filenames:
        path4.append(os.path.join(dirname, filename))

path1 = path1[0:100]
path2 = path2[0:100]
path3 = path3[0:100]
path4 = path4[0:100]

encoder = OneHotEncoder()
encoder.fit([[0],[1],[2],[3]])

# 0 --> Non Demented
# 1 --> Mild Dementia
# 2 --> Moderate Dementia
# 3 --> Very Mild Dementia

from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from PIL import Image

# Initialize the ImageDataGenerator with desired augmentations
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

# Assuming path1, path2, path3, and path4 are lists of image paths for each class
paths = [path1, path2, path3, path4]
data = []
result = []

for class_index, path_list in enumerate(paths):
    for path in path_list:
        img = Image.open(path)
        img = img.resize((128, 128))
        img = np.array(img)

        if img.shape == (128, 128, 3):
            # Add original image to the dataset
            data.append(img)
            result.append(encoder.transform([[class_index]]).toarray())

            # Generate augmented images
            img = img.reshape((1,) + img.shape)  # Reshape for data generator
            i = 0
            for batch in datagen.flow(img, batch_size=1):
                augmented_img = batch[0].astype('uint8')
                data.append(augmented_img)
                result.append(encoder.transform([[class_index]]).toarray())
                i += 1
                if i >= 2:  # num_augmented_images is the number of augmented images to generate per original image
                    break

data = np.array(data)
data.shape

result_array = np.array(result)
int(result_array.size / 4)

result = np.array(result)
number_of_rows = int(result_array.size / 4)
result = result.reshape((number_of_rows,4))
result.shape

x_train,x_test,y_train,y_test = train_test_split(data,result,test_size=0.15,shuffle=True,random_state=42)

y_train.shape

x_train.shape

#Testing different pre-trained models
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, concatenate
from tensorflow.keras.applications import InceptionV3, ResNet50, DenseNet121, EfficientNetB0, VGG16
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model

# Create base model of InceptionV3
base_model_inception = InceptionV3(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Freeze the first 10 layers
for layer in base_model_inception. layers[:10]:
    layer. trainable = False
x = base_model_inception.output
x = GlobalAveragePooling2D () (x)
x = Dense (512, activation= 'relu') (x)
X = Dropout (0.4) (x)
predictions = Dense (4, activation='softmax')(x)
model1 = Model (inputs=base_model_inception.inputs, outputs=predictions)

# Create base model of DenseNet121
base_model_densenet = DenseNet121(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Optionally, freeze the first few layers (e.g., the first 10 layers)
for layer in base_model_densenet.layers[:10]:
    layer.trainable = False

# Add custom layers on top of DenseNet121
x = base_model_densenet.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.4)(x)  # Adjust dropout rate as needed
predictions = Dense(4, activation='softmax')(x)  # Assuming 4 classes for your task

# Create the final model
model2 = Model(inputs=base_model_densenet.inputs, outputs=predictions)

# Create base model of EfficientNetB0
base_model_efficientnet = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Optionally, freeze the first few layers (e.g., the first 10 layers)
for layer in base_model_efficientnet.layers[:10]:
    layer.trainable = False

# Add custom layers on top of EfficientNetB0
x = base_model_efficientnet.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.4)(x)  # Adjust dropout rate as needed
predictions = Dense(4, activation='softmax')(x)  # Assuming 4 classes for your task

# Create the final model
model3 = Model(inputs=base_model_efficientnet.inputs, outputs=predictions)

# Create base model of ResNet50
base_model_efficientnet = ResNet50(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Optionally, freeze the first few layers (e.g., the first 10 layers)
for layer in base_model_efficientnet.layers[:10]:
    layer.trainable = False

# Add custom layers on top of ResNet50
x = base_model_efficientnet.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.4)(x)  # Adjust dropout rate as needed
predictions = Dense(4, activation='softmax')(x)  # Assuming 4 classes for your task

# Create the final model
model4 = Model(inputs=base_model_efficientnet.inputs, outputs=predictions)

# Create base model of VGG16
base_model_efficientnet = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Optionally, freeze the first few layers (e.g., the first 10 layers)
for layer in base_model_efficientnet.layers[:10]:
    layer.trainable = False

# Add custom layers on top of VGG16
x = base_model_efficientnet.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.4)(x)  # Adjust dropout rate as needed
predictions = Dense(4, activation='softmax')(x)  # Assuming 4 classes for your task

# Create the final model
model5 = Model(inputs=base_model_efficientnet.inputs, outputs=predictions)

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

early_stopping = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model3.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model4.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model5.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model1.fit(x_train, y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

history = model2.fit(x_train, y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

history = model3.fit(x_train, y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

history = model4.fit(x_train, y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

history = model5.fit(x_train, y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

# Evaluate the model on the test data in Inception V3
test_loss, test_accuracy = model1.evaluate(x_test, y_test)

# Print the results
print(f"Traniing Results of InceptionV3")
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

# Evaluate the model on the test data in Dense
test_loss, test_accuracy = model2.evaluate(x_test, y_test)

# Print the results
print(f"Traniing Results of DenceNet")
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

# Evaluate the model on the test data in EffientNet
test_loss, test_accuracy = model3.evaluate(x_test, y_test)

# Print the results
print(f"Traniing Results of EffientNet")
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

# Evaluate the model on the test data in ResNet50
test_loss, test_accuracy = model4.evaluate(x_test, y_test)

# Print the results
print(f"Traniing Results of ResNet50")
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

# Evaluate the model on the test data in VGG16
test_loss, test_accuracy = model5.evaluate(x_test, y_test)

# Print the results
print(f"Traniing Results of VGG16")
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Average

models=[model2, model3]
model_input = Input(shape=(128, 128, 3))
model_output = [model(model_input) for model in models]
emsemble_output =  Average()(model_output)
emsemble_model = Model(inputs=model_input, outputs=emsemble_output, name='ensemble')

emsemble_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

historyEnsemble = emsemble_model.fit(x_train,y_train,epochs=20,batch_size=10,verbose=1,validation_data=(x_test,y_test),callbacks=[early_stopping, model_checkpoint])

# Evaluate the model on the test data
test_loss, test_accuracy = emsemble_model.evaluate(x_test, y_test)

# Print the results
print(f"Test Loss: {test_loss * 100}")
print(f"Test Accuracy: {test_accuracy * 100}")

def names(number):
    if number == 0:
        return 'Non Demented'
    elif number == 1:
        return 'Mild AD'
    elif number == 2:
        return 'Moderate AD'
    elif number == 3:
        return 'Very Mild AD'
    else:
        return 'Error in Prediction'

from matplotlib.pyplot import imshow
img = Image.open(r'/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Non Demented/OAS1_0002_MR1_mpr-1_151.jpg')
x = np.array(img.resize((128,128)))
x = x.reshape(1,128,128,3)
res=emsemble_model.predict_on_batch(x)
classification = np.where(res == np.amax(res))[1][0]
imshow(img)
print(str(res[0][classification]*100)+ '% Confidence This Is '+ names(classification))

img = Image.open(r'/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Moderate Dementia/OAS1_0308_MR1_mpr-1_100.jpg')
x = np.array(img.resize((128,128)))
x = x.reshape(1,128,128,3)
res=emsemble_model.predict_on_batch(x)
classification = np.where(res == np.amax(res))[1][0]
imshow(img)
print(str(res[0][classification]*100)+ '% Confidence This Is '+ names(classification))

img = Image.open(r'/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Very mild Dementia/OAS1_0015_MR1_mpr-2_105.jpg')
x = np.array(img.resize((128,128)))
x = x.reshape(1,128,128,3)
res=emsemble_model.predict_on_batch(x)
classification = np.where(res == np.amax(res))[1][0]
imshow(img)
print(str(res[0][classification]*100)+ '% Confidence This Is '+ names(classification))

img = Image.open(r'/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/Mild Dementia/OAS1_0316_MR1_mpr-4_141.jpg')
x = np.array(img.resize((128,128)))
x = x.reshape(1,128,128,3)
res=emsemble_model.predict_on_batch(x)
classification = np.where(res == np.amax(res))[1][0]
imshow(img)
print(str(res[0][classification]*100)+ '% Confidence This Is '+ names(classification))

img = Image.open(r'/content/drive/Othercomputers/My Laptop (1)/My 4th year until my lap is fixed/4TH YEAR-20231030T173451Z-001/4TH YEAR/FYP/Early detection of the Alzehimz deseases/Code Implementation/Early Alzehimz disease detection system/Data/healthBrain.jpg')
x = np.array(img.resize((128,128)))
x = x.reshape(1,128,128,3)
res=emsemble_model.predict_on_batch(x)
classification = np.where(res == np.amax(res))[1][0]
imshow(img)
print(str(res[0][classification]*100)+ '% Confidence This Is '+ names(classification))