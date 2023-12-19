# flask_e2e_project
Final Assignment for HHA 504 (Product / Web Service)

# Web Service

The web service created is an flask app with three pages containing patient data. The first table, Patients, is basic patient contact information. The second table, Preferences, contains patients' preferences for things like foods and shows. The third table, Demographics, contains information on patients' demographics. The app has 5 pages. The first being the home page that welcomes users and also allows them to log in. Each of the tables have their own page in the app. The final page is a profile/dashboard page that has information on users after they log in. Clicking on the page when a user is not logged in would lead back to the home page. 

</br>

# Technologies Used

+ All coding was done in Google Cloud Shell
+ The database was created and hosted on an Azure Database for MySQL flexible server
+ Data tables were created and populated with with **SQLalchemy**
+ The flask app was created in a [python file](https://github.com/joyc3lin/flask_e2e_project/blob/main/app/app.py) and it was styled with **tailwind css**
+ **Google Oauth** was used to allow users to log into the app with their gmails
+ **Logger** was built into the app as well
+ The app also offers an **API service**, specific queries can be made through the URL to pull up specific information from each table
  +   At the end of the URL for the three tables, add a '?' and  [column_name]=[specific_result]
+ The app was also conainerized through **docker**
  + To run locally: run <code> python app.py </code> in terminal
    + make sure to <code>cd</code> into the app file
  + To run on docker: make sure that all necessary files/folders are in the same level as the Dockerfile
    + Run the image with: docker run -p [machine-port-number]:[docker-image-port-number] [image-name]
+ Lastly, the app was deployed on **azure**
  + It can be accessed through this link: https://joycefinal504.azurewebsites.net/
    + Note: while the app works and the different pages can be accessed, the app runs into an error when you try to log in through Google

+ Screenshots of the App can be found in the [docs](https://github.com/joyc3lin/flask_e2e_project/tree/main/docs) folder!
  </br>

# .ENV Template 

```python 
AZURE = "mysql+pymysql://[azure-server-username]:[password]@[server-name]/[db-name]"
GOOGLE_CLIENT_ID = "[can be created on Google Cloud Credentials]"
GOOGLE_CLIENT_SECRET = "[can be created on Google Cloud Credentials]"
```

