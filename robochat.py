import pandas as pd
import colorama
import random
import numpy as np
import matplotlib.pyplot as plt

colorama.init()
from colorama import Fore, Style
import nn_model
import pre_processing_model

# -----CONSTANTS-----#
# List of words to end the chatbot conversation
QUIT = list(["stop", "quit", "end", "Stop", "Quit", "End", "STOP", "QUIT", "END"])
path = "WikiQA.csv"


# -----METHODS-----#
def split_data(training_data):
    # split the features and target labels
    random.shuffle(training_data)
    training_data = np.array(training_data, dtype=object)
    trainX = np.array(list(training_data[:, 0]))
    trainY = np.array(list(training_data[:, 1]))

    return trainX, trainY


def get_response(intents_list, data):
    if len(intents_list) == 0:
        return random.choice(data[data['Tag'] == 'Unknown']['Responses'].values)
    tag = intents_list[0]
    for index_i, row_i in data.iterrows():
        if row_i["Tag"] == tag:
            result = random.choice(data[data['Tag'] == tag]['Responses'].values)
            break
    return result


def visualize_tag_classification(sentence, tags_predictions):
    five_tags_predictions = np.array(tags_predictions)[:5]
    tags = [row[0] for row in five_tags_predictions]
    predictions = [round(float(row[1]), 2) for row in five_tags_predictions]
    plt.bar(tags, predictions)
    plt.xticks(rotation="45")
    plt.xlabel('Tags')
    plt.ylabel('Prediction')
    plt.title('Prediction of Tag for: ' + ' " ' + sentence + ' " ')
    plt.tight_layout()
    plt.show()


def RUN_CHATBOT(NN, model, processing_model):
    print('START CHATTING WITH THE ROBO_CHAT, \n\nTYPE any of the words to stop the conversation:\n', QUIT, '\n')
    while True:
        print(Fore.YELLOW + "HUMAN:" + Style.RESET_ALL, end="")
        message = input("")
        if message in QUIT:
            print(Fore.RED + "Ending the chat\n " + Style.RESET_ALL, end="")
            break
        intents, all_tags_predictions = NN.predict(model, message, processing_model.words, processing_model.classes)
        result = get_response(intents, dataset)
        print(Fore.GREEN + "ROBO-CHAT:" + Style.RESET_ALL, result)
        visualize_tag_classification(message, all_tags_predictions)
        if intents[0] == 'ending':
            print(Fore.RED + "Ending the chat\n " + Style.RESET_ALL, end="")
            break


# ----- ROBO-CHAT IMPLEMENTATION -----#

dataset = pd.read_csv(path, sep='\t')  # Read the dataset

# Pre-Processing
preprocessing = pre_processing_model.PreProcessing(dataset)

# Visualization about pre-processing
preprocessing.Stop_Word_Plotter()
preprocessing.Tags_Plotter()

print('Pre-processing data...\n')
preprocessing.pre_process_words()
training = preprocessing.bag_of_words_model()

train_X, train_y = split_data(training)

# Feed training data into a Neural Network Model
print('Fitting the model...\n')
NN_MODEL = nn_model.Model(train_X, train_y)
model = NN_MODEL.fit()

RUN_CHATBOT(NN_MODEL, model, preprocessing)
