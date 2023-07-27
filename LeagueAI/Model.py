import csv
import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import LeakyReLU
from keras.layers import Dropout
import json

champion_path = 'champion.json'
with open(champion_path, 'r') as f:
    data = json.load(f)

champions = {}
for index, (champion_id, champion_info) in enumerate(data['data'].items()):
    champions[champion_info['key']] = (index, champion_info['name'])


def read_csv_file(filename):
    data = []

    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            data.append(row)

    labels = []
    team_data = []
    for list in data:
        winner = list[0]
        if winner == "100":
            winner = 1.0
        else:
            winner = 0.0
        team1 = [champions[champ][0] for champ in list[6:11]]

        team2 = [champions[champ][0] for champ in list[1:6]]
        labels.append(winner)
        team_data.append([team1, team2])

    onehot = np.eye(len(champions), dtype='float32')[team_data]

    team_data = np.zeros((len(team_data), 2, 5, len(champions)))
    team_data[:, :, :, 0] = 0.0

    team_data[:len(team_data), :2, :5, :] = onehot

    return labels, team_data


labels, team_data = read_csv_file('matches.csv')
valid_labels, valid_team_data = read_csv_file('valid.csv')
team_data = team_data.tolist()
valid_team_data = valid_team_data.tolist()


def define_model():
    model = Sequential(name="Discriminator")
    model.add(Conv2D(64, (3, 5), strides=(1, 1), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.5))

    model.add(Conv2D(128, (3, 5), strides=(1, 1), padding='same'))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    # compile model
    opt = Adam(learning_rate=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    return model


model = define_model()
model.fit(team_data, labels, validation_data=(valid_team_data, valid_labels), epochs=100, batch_size=20, verbose=2)
scores = model.evaluate(valid_team_data, valid_labels, verbose=0)

print("CNN Error: %.2f%%" % (100 - scores[1] * 100))
model.save('model.h5')
