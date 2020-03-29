## Network and System status

### This project aims in to collect data each minute from network and system and to build a dashboard in Power BI to analyze them.

For each one minute the script collect data from network and system parse them and insert in a PostgreSQL database hospeted in a EC2 instance at AWS.

If you want share this script wiht another machines to collect it data and them dosen't have Python installed, it is possbile to generate a executable file (*.exe*) and share with them.

To do this, download pyinstaller and execute:

```pyinstaller .\internet_status.py --add-data 'connection_db.py;.' --add-data 'database.ini;.'```

Command above will create */build* and */dist* folders and a *internet_status.spec* file. Here we just need **_dist_** folder, this we will share wiht machines that we want. The *.exe* is in **_\dist\internet_status\internet_status.exe_**. Just execute and the data will be inserted at database.

I used EC2 why I have already a free instance but you can use a local database or even a .csv file. If you choose a .csv you will have to change some things in the code.

When you have your table populated you can read with Power BI, make your transformation in data, create measures and build a dashboard like below:

![Dashboard](https://user-images.githubusercontent.com/37387111/77854116-a25dc280-71be-11ea-8ed6-23d35283f67d.png)
