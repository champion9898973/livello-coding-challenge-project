//................................................................................................................//
Date         :12-07-2025
Author       : Sai charan kumar chukkala
APplication  : Livello Coding Challenge
//................................................................................................................//


//...............................................................................................................//
Project file structure:

C:.
│   docker-compose.yml
│   invalid_messages.log
│   mqtt_data.db
│   view_data.py
│   
├───API
│       app.py
│       database.py
│       Dockerfile
│       requirements.txt
│       
├───data
├───log
├───mosquitto
│   ├───config
│   │       mosquitto.conf
│   │
│   ├───data
│   │       mosquitto.db
│   │
│   └───log
│           mosquitto.log
│
├───mqtt
│       database.py
│       Dockerfile
│       MQTT_script.py
│       requirements.txt
│
└───__pycache__
        database.cpython-313.pyc

//...............................................................................................................//

//...............................................................................................................//
 Prerequisites:

 1. Visual studio code (1.87.1,6c3e3dba23e81c2d10fbd1c0ee5ec7b0da5b422d x64)
 2. Docker Desktop Application (Docker version 28.2.2, build e6534b4)
 3. Python IDLE (Python 3.13.2)
 4. Sql lite (DB.Browser.for.SQLite-v3.13.1-win64)
 5. Mosquitto (mosquitto-2.0.21a-install-windows-x64)
 6. Git(git version 2.49.0.windows.1)
 7. pip (pip 25.1.1)
 //................................................................................................................//


//................................................................................................................//
 Commands used :
1. mkdir -p mosquitto/config mosquitto/data mosquitto/log
2. cd <Path to project directory>
3. docker compose up -d ("Start Mosquitto broker using Docker Compose")
4. docker ps ("Check running containers")
5. pip install gmqtt 





//..............................................................................................................//

Desccption of features:

1. MQTT Broker and Listener:

    A python script located at "~\livello coding challenge project\mqtt\MQTT_script.py"

    Here used gmqtt library
    Subscribed to a topic "/devices/data"
    Within the script:
                The generate_message() function is defined to create randomized data, which is used for publishing sensor data to the broker.

                The on_message() function is implemented to handle and process incoming messages received on the subscribed topic.

                This setup ensures the script can both simulate publishing data and process incoming data based on the defined schema and logic.
2. Message Validation:
         
                The continution python script of feature 1:

                The script includes a function named validate_message(), which is responsible for validating the generated or received messages against a predefined JSON schema.
    
                If the message fails validation, the function logs the reason for failure to the invalid_messages.log file using Python’s logging module.

                This ensures that only well-formed and schema-compliant messages are processed further, helping maintain data integrity and traceability.

3. Data Storage:
                The logic for storing valid messages into a database is handled by the script "~\livello coding challenge project\mqtt\database.py"
                The SQLite database file used is located at "~\livello coding challenge project\mqtt_data.db"
                
                In MQTT_script.py, once a valid message is received, it is stored in the database using functions defined in database.py.

                The init_db() function initializes the database by creating the required tables if they do not exist.

                The script also includes logic to handle device entries and insert new sensor event records.

4. Real-Time Monitoring:

               Created an API souce code at  "~\livello coding challenge project\API" and python file at /app.py

               There are two api's

               1. Retrieve a list of all devices and their last seen timestamp.
               2. Retrieve the last 10 events for a specific device.

               Testing URL's:

               1. http://localhost:5000/devices
               2. http://localhost:5000/events/<device_id>

               Functionality of apis:
               1. Executes a SQL query on the Events table to:
                                
                        Group records by device_id

                        Get the latest timestamp (MAX(timestamp))

                        Order the results by most recently seen devices

                2. Uses the provided device_id in the URL path.
                
                Queries the Events table to:

                        Filter rows matching the given device

                        Sort them by timestamp in descending order

                        Limit the result to the latest 10 events

        Data base is shared data base which is located at "~\livello coding challenge project\mqtt_data.db"

5. Dockerization:

Please find the dockerization files at the below mentioned paths
        
        Mosquitto MQTT Docker file     : "~\livello coding challenge project\mosquitto\config\mosquitto.conf"
        Python MQTT Client application : "~\livello coding challenge project\mqtt\Dockerfile"
        The REST API service.          :"~\livello coding challenge project\API\Dockerfile"

     Docker Compose to orchestrate the setup:   "~\livello coding challenge project\docker-compose.yml"

6. Testing and Documentation:
          Manually publish test messages to the /devices/events topic using mosquitto pub and verify that:
          
          Valid messages are processed and stored correctly: 
          Please find the results at : "~\Livello coding challange\pics of execution\Manual subscribe and publish.png"
          and logs of invalid at here: "w\livello coding challenge project\invalid_messages.log"

//......................................................................................................................................................//

//......................................................................................................................................................//

Usage:

Once you Downloaded the code from github

Install all the prereqisites

Now open Docker desktop application and signin

Now open code in visual studio code and open integrated terminal of it for the project

Now run below comands in the terminal :

docker-compose down --volumes --remove-orphans
docker-compose build --no-cache
docker-compose up

So code will starts executing automatically publising data 

if you want to publish data manualy open another terminal and run the comand and change the values:

"mosquitto_pub -h localhost -t /devices/data -m "{\"device_id\":"device_01",\"sensor_type\":\"temperature\",\"sensor_value\":25.6,\"timestamp\":\"2025-07-11T18:30:00\"}"

Scriot also randomly publish data correct and incorrect data + correct data and also for the command promot you can add manually
............................................................................................................................................

Please reachout to me if you face any issues at: saicharan81269@gmail.com
                 
   
