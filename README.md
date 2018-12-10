# Disaster Response Pipeline Project
### Summary:
This project builds a web app where an emergency worker can input a new message and get classification results in several categories. Behind the web app is an ETL data pipeline which gathers, cleans and stores the data in a SQLite database and a machine learning pipeline which trains a disaster message classifier with the data stored in the SQLite database from the ETL data pipeline. The web app also displays visualizations of the data.

### File Structure:
\- app <br>
| - template <br>
| |- master.html  # main page of web app <br>
| |- go.html  # classification result page of web app <br>
|- run.py  # Flask file that runs app  <br>

\- data <br>
|- disaster_categories.csv  # training data  <br>
|- disaster_messages.csv  # training data <br>
|- process_data.py  # ETL pipeline to clean and store the training data <br>
|- **DisasterResponse.db**   # database created after running the ETL pipeline to save clean data <br>

\- models <br>
|- train_classifier.py  # machine learning pipeline to train a classifier and store it in a pickle file <br>
|- **classifier.pkl**  # pickle file of the model saved after running the machine learning pipeline  <br>

\- README.md

The database file and the pickle file for the classifier model are not in the repository. They will be created by running the ETL data pipeline and the machine learning pipeline respectively.  

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
