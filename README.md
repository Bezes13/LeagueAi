# LeagueAi
This little Application uses a convolutional Network to calculate the chance that a team wins in League of Legends.

<h3>Model.py:</h3>
The convolutional Network is trained with keras on the <strong> matches.csv </strong> and validated on the <strong> valid.csv </strong>

<h3>main.py:</h3>
This program uses the league of Legends Api to collect played high elo games, structure the data and save them.

<h3>app.py:</h3>

Creates a python window where the user can create two teams and calculate the winning team by executing the model on the selected data.
![alt text](LeagueAi/application.png)