# Data_Collection_Pipeline
An end to end, scalable data-pipeline. 

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

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



<!--

## Milestone 2

- Does what you have built in this milestone connect to the previous one? If so explain how. What technologies are used? Why have you used them? Have you run any commands in the terminal? If so insert them using backticks (To get syntax highlighting for code snippets add the language after the first backticks).

- Example below:

```bash
/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

- The above command is used to check whether the topic has been created successfully, once confirmed the API script is edited to send data to the created kafka topic. The docker container has an attached volume which allows editing of files to persist on the container. The result of this is below:

```python
"""Insert your code here"""
```

> Insert screenshot of what you have built working.

## Milestone n

- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further. --> 
