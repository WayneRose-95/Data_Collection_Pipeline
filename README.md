# Data_Collection_Pipeline
An end to end, scalable data-pipeline. Please see the develop branch for the latest version in development.  

![UML Diagram Data Collection](https://user-images.githubusercontent.com/89411656/177179636-8eadff3f-8bed-4251-a29d-ea2b16a9a6c6.jpg)


[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

> The first pre-release version of this project has been released. Please see the releases tab 

> The goal of the project is to create a scalable data-pipeline, which runs autonomously within a cloud environment.

> Technologies Used: 

<p align="left"> <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" href="https://www.docker.com/" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> 
<img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://grafana.com" target="_blank" rel="noreferrer"> 
<img src="https://www.vectorlogo.zone/logos/grafana/grafana-icon.svg" alt="grafana" width="40" height="40"/> </a> <a height="40"/> </a> 
<a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a> <a  
<img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> 
<img src="https://raw.githubusercontent.com/detain/svg-logos/780f25886640cef088af994181646db2f6b1a3f8/svg/selenium-logo.svg" alt="selenium" width="40" height="40"/> </a> </p>

# Running the Program 

Clone the repository. One method is to run: 

```
git clone <link to repo> 
``` 
Where <link to repo> is the url of this repository 

Within the VSCode IDE.


Create a new environment using the dependencies from requirements.txt

If you are within a conda environment, this can be done by running: 

```
conda create --name <env_name> --file requirements.txt
```
Where <env_name> is the name of your environment 

For more information, please follow this ![link](https://frankcorso.dev/setting-up-python-environment-venv-requirements.html)


Before running the program, within the config directory, please create the following file:

```
rds_config_details.yml 
```
Then, using the template as a guide below, fill in your details to your RDS 

![image](https://user-images.githubusercontent.com/89411656/177586927-c4010bab-6192-4714-b2ab-6167d8fe9d51.png)

Set your .json file name within the main.py script by changing this argument of the method 

![image](https://user-images.githubusercontent.com/89411656/177589595-10fe0f31-dc51-4d1f-9edd-a3d0d02ed1d1.png)

When you are all set, run:  

```
python main.py
```
Within the directory of the github repo folder: Data_Collection_Pipeline. 

Enjoy! 

# Project Log 

## Milestone 1 - Choosing a Website 

For this project, the website: [metacritic.com](https://www.metacritic.com) was chosen. 

As an avid fighting game player, I wanted to create a dataset by scraping all of the fighting games from the website. 

This would create an opportunity to compare and contrast the various fighting games on the website via certain metrics. 


Each of the pages has the following metrics to compare and contrast: 
* Title
* Platform (i.e. PS2, Xbox, PS3 etc.) 
* Release Date 
* MetaCritic_Score
* User_Score 
* Developer
* Description 

## Milestone 2 - Prototype finding the individual page for each entry 

For this milestone, a Scraper Class was created 
![image](https://user-images.githubusercontent.com/89411656/175793708-8b4d1486-8e78-4a41-9b40-64b737c4d794.png)

This class would house general all purpose webscraping methods. From interacting with buttons on a page to collecting page_links. 

Methods from this class would be inherited within the script specific to the website  for reusability purposes. 

## Milestone 3 - Retrieve data from details page 

Metacritic_Scraper.py was created by inheriting methods from the ScraperClass.py script as shown below: 

![image](https://user-images.githubusercontent.com/89411656/175793797-65dedc98-ecdc-449d-98f4-4b40bc42adac.png)

By observing the details page, the metrics as shown in Milestone 1 could be scraped using Selenium Webdriver 

To do this, a dictionary of xpaths was created in the __init__ method of the Metacritic_Scraper.py script 

![image](https://user-images.githubusercontent.com/89411656/175793820-4f677087-76c3-404a-96ae-75665fd7da84.png)

Next, using python's tuple unpacking, the key of the xpaths_dict was set as the key of the page_information_dict, whose value was the text of the web-element from the xpaths_dict. 

![image](https://user-images.githubusercontent.com/89411656/175793865-05aaf3e3-279f-4f79-be64-3b81e6584b33.png)

Each attempt at collecting a web-element from the page was encased inside a try/except block to catch any difficulties found when finding elements such as empty pages or no element present. 

On top of this, there were further difficulties in collecting data from certain fields. These cases were remedied by using if statements where necessary. 

For each dictionary created, a UUID v4 was made to uniquely distinguish each record scraped. 

## Milestone 4 - Documentation and Testing 

As the code grew bigger and bigger, it became difficult to understand what each of the methods were doing. What is this method's purpose? What does it return? 

This was when docstrings and log files were added to answer these questions. 

An example of a docstring inside the code is shown below: 
![image](https://user-images.githubusercontent.com/89411656/175794090-ebe97095-3fc5-4b27-916d-d79d6e61d54d.png)

For the log files, these were important to track processes within the code as it was running. When the code was run, a directory containing the logs was created to track these processes. 

![image](https://user-images.githubusercontent.com/89411656/175794105-d68b5ad6-54c8-462f-8167-1b70316dfdfe.png)

That said, it is all well and good to have monitoring and explanations of methods in place, but how do we know if each of our methods are working as intended?  

Python's built-in Unittest module allows for snippets of code to be tested against certain assertions. 

A sample test is shown below: 
![image](https://user-images.githubusercontent.com/89411656/175794178-559da984-c41e-4f0b-8741-f91023ade401.png)

This became a powerful asset in the project as the tests could be written to detect any discrepancies in the code. 

In the above example, 3 hrefs are used to test the Scraper's ability to scrape from multiple pages of varying review scores. 

This test was created, as at first, the scraper was only able to take metacritic and user_scores from positively recieved titles. 

By making edits to the method, and running the test script, the ouptuts of the dictionary could be validated to catch bugs in collecting data. 

As a result, whenever a new method was added, it would be tested. Overall, this method of test-driven development saved valuable time within development. 

# Milestone 5 - Scalably Storing the Data 

After completing the scraping process. The raw data was saved inside a .json file. 

This .json file would then be cleaned by creating a seperate class dedicated to cleaning data from the .jsons from the website. 

![image](https://user-images.githubusercontent.com/89411656/176451490-198d6a15-d969-4751-b54e-912beb2c2172.png)

The resulting cleaned pandas dataframes would then be uploaded to an RDS running in AWS. 

As shown in the image above, a config.yaml file was made to securely connect to the database. 

A snapshot of the database can be found below
![image](https://user-images.githubusercontent.com/89411656/176452182-8d8193a9-2618-4568-a5aa-aa4ccca20034.png)

# Milestone 6 - Prevent Rescraping of the same data 

In order to speed up processing time, and send clean, new records to the database. 
Logic was placed inside the code to prevent data from the same pages from being rescraped. 

To do this, a new method called record_check was created. 

![image](https://user-images.githubusercontent.com/89411656/176453030-7aa53e04-ecc8-487e-acec-a77c30c38fe5.png)

This method was used to create a list of hrefs which have already been visited by the scraper. 

This list was then compared with the hrefs collected. If the hrefs collected during the scrape were already inside the RDS, then the page would be skipped. Saving time, and preventing duplicate records. 



![image](https://user-images.githubusercontent.com/89411656/176453763-48682e8d-11db-43a0-bc28-fa8e269ed7e8.png)

# Milestone 7 - Docker and Amazon EC2

For this milestone the scraper application was containerised using Docker. 

Running the application within a Docker container allows for simpler development and deployment as Docker containers run within their own self-contained environment which can be used on any operating system. 

![image](https://user-images.githubusercontent.com/89411656/177178046-98fc214e-972a-4a2c-8fc7-b2e01df184f2.png)

The above image was built, and it runs locally as shown. 

![image](https://user-images.githubusercontent.com/89411656/177182540-8f67e6ed-1851-4d19-b51e-fd971aa93c43.png)

The image was then pushed to dockerhub as shown below. 

![image](https://user-images.githubusercontent.com/89411656/177184569-beddc882-5081-45ac-af8e-130e9c38cbdb.png)


Having completed these steps, an EC2 instance on AWS was spun up to automate the process of running the scraper. 

Docker was installed on the EC2, from which the image could be pulled from DockerHub. 

![image](https://user-images.githubusercontent.com/89411656/177190123-30f72961-5f40-4d53-ad9a-77f6146fa3cd.png)

Here is the same scraper again, but running on an EC2 instance.

![image](https://user-images.githubusercontent.com/89411656/177190365-fb2ccfb9-cd21-44fd-a061-653ebbf4e1a4.png)

# Milestone 8 - Monitoring 

In order to track the underlying metrics of both the EC2 instance and the docker container, the open source monitoring software solution, Prometheus, was used. 

This was done, running: 

```
docker pull prom/prometheus 
```
Inside the the EC2 instance. To run Prometheus from inside a Docker container. 
This was done to save space within the EC2 instance and for ease of deployment. 

An image showing the status of the docker container, the EC2 instance and the localhost are shown below. 

![image](https://user-images.githubusercontent.com/89411656/177564390-5076678c-c25b-412c-b0c6-265c8c77a428.png)

Grafana is an open source visualisation tool in which users can create operational dashboards to monitor processes of the tech stack. 

This program was used to take the metrics collated from Prometheus, and visualise them in a Grafana dashboard like so: 

![image](https://user-images.githubusercontent.com/89411656/177769054-2fb7e4d7-d090-4f51-bd49-c2bb0a542a12.png)

# Milestone 9 -- CI/CD

In order to allow for easier deployment from build to docker container, a CI-CD Pipeline was set up via Github actions. 

The following yaml file was created. Below is a high level breakdown of the code. 

![Explanation of docker-image yml file](https://user-images.githubusercontent.com/89411656/177583031-00775652-423e-4634-9fb0-8ca5dccd0fe9.jpg)


# Conclusions 

This project provided a wealth of experience in working with a wide range of technologies. 
From building to Selenium, to containerising the application with Docker, the full DevOps cycle was employed throughout the project to build and successfully create the data pipeline. 

The most interesting section of the project was being able to deploy the completed code onto an EC2 instance, and run it inside a cloud environment. 
Personally, it highlighted the importance of cloud technology, and why it is so prevalent in today's modern tech stacks. 

# Future Improvements 

- Currently, the code is hard-coded to only accept a specific type of rds_config file. This can be changed to accept any type of file. 

- Greater implementations of OOP principles. e.g. Making the MetacriticScraper class and DataCleaning classes more independent. 

- Addition of a progress bar to give users a window of how long the data collection process will take to finish. 

- Adding a column field to scrape the publisher from the website

- Currently the code only scrapes from one sub-category of the website; the fighting games section of the site. 
  Is it possible widen the search area to other portions  of the website?

- Customisation of the users' options. i.e. How many records, which subcategory or sub-categories? 

- Expansion of the RDS to facilitate a STAR schema of tables to enhance the scalability of storing the data. 

- Further utilisation of Amazon S3 to store cleaned data inside a data lake. The data must be time-stamped and updated accordingly.

- Could we look at other sections of the website i.e. Music, TV and Movies and scrape from those as well? 


