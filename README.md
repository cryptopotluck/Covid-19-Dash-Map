##Covid-19 Plotly Dashboard Project

![alt text](https://i.udemycdn.com/course/480x270/2597712_9552_2.jpg)

View the Application Here: https://covid-dash-udemy.herokuapp.com/


Introduction Video:

[How to Build Maps Tutorial Video](https://youtu.be/JoehvW-aUd4)

Learn More on Django, Plotly & Dash on my Full Course:

[Full Udemy Course](https://www.udemy.com/course/plotly-dash/?referralCode=16FC11D8981E0863E557)

### Maps & Graphs
tab_home
![alt text](https://cdn.discordapp.com/attachments/482514924707250186/697174405750587392/Screen_Shot_2020-04-07_at_2.42.22_PM.png)
1. Graph 1: Find Cases, Recoveries & Deaths on the map bubble chart.
2. Graph 2: See our global growth rate & notice the data from china in red. It isnt because China is amazing its not growing because China's Numbers are unreliable. 
____
tab_usa_map
![alt text](https://cdn.discordapp.com/attachments/482514924707250186/697165809688117339/Screen_Shot_2020-04-07_at_2.27.43_PM.png)
1. Graph 1: Scale the Case Rate & update the graph bellow. See what areas are affected & How many cases near you by hovering over the map.
2. Graph 2: Show the current cases in the USA with a layered bar chart to represent each states growth contributions. 
____
tab_snapshot
![alt text](https://cdn.discordapp.com/attachments/666224568826069024/697342775804297297/Screen_Shot_2020-04-08_at_2.10.49_AM.png)
1. Graph 1: Select a date from the dropdown menu 3/27/2020 -> Now & fetch on the dataset in the table. 
1. Graph 2: Bar Graph Representing the contributions by country
Table Dataset: Dataset being fetched by selecting a date.

### Async Data
fetch_today.main(date: str, value:int, usa_only:bool): returns today's values only

fetch_to_date.main(date: str, value:int, usa_only:bool): returns (selected date) -> Yesterday's Values. f'https://covid19.mathdro.id/api/daily/{date}'

fetch_historic.main(): returns https://covid19.mathdro.id/api/daily

## How to Install

- Create an virtual env 
    1. Check if you have a virtual env ``virtualenv --version``
    2. (Not Installed) Dont see a version number? run ``sudo pip install virtualenv``
    3. (Installed) Make a folder within the highest file of the project ``mkdir ~/env``
    4. run ``virtualenv ~/env/my_new_app``
    5. cd into the bin folder ``cd ~/env/my_new_app/bin``
    6. activate the env ``source activate``

- ``pip install -r requirements.txt``

- Run the individual Files

# Useful Links

[Plotly](https://plot.ly/python/)

[Dash Docs](https://dash.plot.ly/)

[dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/)

[Covid-19 Data Used](https://covid19.mathdro.id)


### Still Have Questions?
[cryptopotluck.com](https://www.cryptopotluck.com)

[cryptopotluck Discord](https://discord.gg/rNc6xtP)








