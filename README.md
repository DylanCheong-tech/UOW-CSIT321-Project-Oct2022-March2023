# UOW-CSIT321-Project-Oct2022-March2023

UOW Bachelor of Computer Science - CSIT 321 Project. <br />
This is the Final Year Project for the students in their final year study. The project title is Homomorphic Encryption and its application to e-voting system. 

# Project Status
The software project development is still in progress. 

# Descriptions
In this final year project, the team is asked to propose and implement a software product,  e-voting system, with applying a homomorphic encryption scheme to achieve the security concerns for the end-users, Voters. <br />
<br />
Homomorphic encryption is an encryption scheme that allows some specific algebraic operations on the encrypted data and when decrypting the operated encrypted data, it will produce an identical result as the operation that operated on the original data. This property can be achieved by structure preservation of the homomorphic encryption when encrypting the data into ciphertext. <br />
<br />
In our proposal e-voting system, we have set our target to be all the large organizations who have their high concern on the security and privacy of the voting scheme. Two entities have been identified, Event Owner and Voter. Event Owners can create a vote campaign and invite the predefined voter to participate and cast their vote. <br />
<br />
This e-voting system will be implemented as a web application. The core functionalities of the e-voting system is its ability to perform the homomorphic encryption and tally on the vote data by using the existing public-key cryptosystem with its homomorphic property. 
<br />
For more information regarding our software project, kindly refer to our [project website](https://fyp22s402.wixsite.com/homomorphic-encrypti).

# Architecture 
To be able simulate the real world scenarios with our software product, we have decided to utilize the virtual machines to simulate the end-to-end voting process, from creating the voting event, voter cast the option, to publishing the vote result. We acquired the Oracle VM  VirtualBox as a platform to manage virtual machines. <br />

# Installation
To be able run the e-voting web application, you will only need a browser as a client side to access the server services. For hosting and running the server codes you may need some  dependencies and installations. <br />

### Requirements
| Requirements                                | References                                                                                |
|---------------------------------------------|-------------------------------------------------------------------------------------------|
|Python 3                                     |https://www.python.org/downloads/                                                          |
|Django v4.x.x+                               |(https://www.djangoproject.com/download/                                                   |
|SendGrid API v3.x.x+                         |https://github.com/sendgrid/sendgrid-python                                                |
|MySQL                                        |N/A                                                                                        |
|Selenium WebDriver Python Library            |https://www.selenium.dev/documentation/webdriver/getting_started/install_library/          |
|Selenium WebDriver Python Driver Manager     |https://github.com/SergeyPirogov/webdriver_manager                                         |


# Usage 
To install all the dependencies: 

``` pip install -r requirement.txt ```

To make the system migrations for the system database:

``` python manage.py makemigrations ```

``` python manage.py migrate ```

To run the web server:

``` python manage.py runserver 127.0.0.1:8800 ```

# Support 
System installation guide and user manual can be found in our project documentation. 

https://drive.google.com/drive/folders/1bgBoo6SaiKi-WcKG2fXVLagw7ceFmGqJ?usp=share_link 

# Authors and Acknowledgement 
The software project team is formed by 5 students with different majors in their studies. 

Team Members:

- Cheong Wai Hong
- Gee Wei Shuan, Colemann (@tsokrgls1999@gmail.com)
- Hone Ter Yen (@ix3zjhty@gmail.com)
- Johan Bin Iskandar (@johaniskandar95@gmail.com)
- Kow Wei Ren (@koweiren@gmail.com)


