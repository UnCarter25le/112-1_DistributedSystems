# Preface:

### 1. This repo is for in-service course, distributed systems instructed by [Dr. Liao](http://cfliao.net/en/doku.php).

#### - Coworker is [Shelley](https://github.com/ShelleyHsu).

### 2. This project in this repo is about [Apache Qpid](https://qpid.apache.org/index.html).

---
# Prerequisite:

## 1. Installation Guide: 

1. Please use [Windows OS](https://qpid.apache.org/components/index.html) and powershell termianl for executing command.

2. Software must installed:
    - To active _Qpid Broker-J(Message Server)_, it must install [JDK_17](https://www.oracle.com/tw/java/technologies/downloads/#jdk17-windows) and [Maven_3.9.5](https://maven.apache.org/download.cgi).

    - To deliver message via _Qpid Proton(Message API)_, my advise is to install [Python3.12](https://www.python.org/downloads/windows/) or [Python3.8 up](https://github.com/apache/qpid-proton/blob/main/INSTALL.md). Please pip install [python-qpid-proton](https://pypi.org/project/python-qpid-proton/) v0.39.0 . The requirements.txt is below:
        ```
        beautifulsoup4==4.12.2
        certifi==2023.11.17
        cffi==1.16.0
        charset-normalizer==3.3.2
        idna==3.6
        pycparser==2.21
        python-qpid-proton==0.39.0
        requests==2.31.0
        soupsieve==2.5
        urllib3==2.1.0            
        ```

        * Optionally, intallation of [Python2.7.18](https://www.python.org/downloads/windows/) is also a way to deliver message via _Qpid Messaging API Python(Message API)_. Please pip install [qpid-python](https://pypi.org/project/qpid-python/) v1.36.0-1 . The requirements.txt is below:
        ```
        qpid-python==1.36.0.post1
        ```

3.  Install and active _Qpid Broker-J(Message Server)_:
    
    1. _PLEASE FOLLOW THE INSTRUCTION TO SET ENVIRONMENT VARIABLE_
    ![Alt text](/readmePhotos/Screenshot%202024-01-02%20172705.png)

        Tow photo to reference:

        ![Alt text](/readmePhotos/Screenshot%202024-01-02%20172932.png)
        ![Alt text](/readmePhotos/Screenshot%202024-01-02%20173020.png)


    2. Getting sources：git clone [qpid-broker-j.git](https://gitbox.apache.org/repos/asf/qpid-broker-j.git).

    3. Building & Without Running tests & Distribution bundle:
        
        1. cd to folder _qpid-broker-j_, and execute command : 
        `mvn clean install -DskipTests`  .After done, execute command 
        `mvn clean package -DskipTests`.
            - (What's [DskipTests](https://github.com/apache/qpid-broker-j/blob/main/doc/developer-guide/src/main/markdown/build-instructions.md#maven-commands).)
        
        2. cd to folder _qpid-broker-j/apache-qpid-broker-j/target_, and find out packaged zip file called _apache-qpid-broker-j-9.1.1-SNAPSHOT-bin.zip_. That's what we need.

    4. Running the Broker:

        1. Expand the broker distribution bundle and cd to folder _qpid-broker_.

        2. Declare QPID_WORK environment variable:

            - Open powershell and execute command `set QPID_WORK=%APPDATA%\Qpid`. That will help to locate the config.json of Qpid Broker-J to folder _C:\Users\Username\AppData\Roaming_.

        3. _START BROKER_:
            1.  cd to folder _qpid-broker/9.1.1-SNAPSHOT/bin_.
                - If not set QPID_WORK, it's possible to see config.json located the folder _qpid-broker/9.1.1-SNAPSHOT/bin_.
            2. execute command `.\qpid-server.bat`.
        
            ![Alt text](/readmePhotos/Screenshot%202024-01-02%20174510.png)





--- 
# How to execute project and what's idea behind the scene:


## 1. Folder structure:

- Scenario1/

    - FailureCase/
        
        What I see is there is no way to create multiple sender instances for sending.

    - InitialAttemption/

        I still don't find any clue to deliver messages outside containers(event-driven container).

        > As the [API doc](https://qpid.apache.org/releases/qpid-proton-0.35.0/proton/python/docs/tutorial.html) says: 
        > 
        > Now that we have defined the logic for handling these events, we create an instance of a Container, pass it our handler and then enter the _event loop by calling run()_. At this point, control passes to the container instance, which will make the appropriate callbacks to any defined handlers.
        

    - TestCase/
        These are for showing the effect of project without doing request.

    - Python files at this folder level:
        - TheProducer.py
            1. Request [target website](https://www.cartoonmad.com/hotrank.html) and send hot comic list today to two consumers.
            2. Accept the feedback sent by two consumers and preparing workload to _distribute_ it to two or three workers based on the volumen of workload.
                
                - If needed, create the folders for saving files.

            3. Wait until receive the completion notification sent by the workers.
        - Consumers_1.py and Consumers_2.py
            1. Accept the hot comic list sent by the producer and choose one comic or quit.
            2. Wait unitil receive the completion notification sent by the producer.

        - Worker_Basic_1.py, Worker_Basic_2.py and Worker_Premium_3.py
            1. Accept the distributed workload and request target website for the latest pages of comic book designated by consumers.

            2. Save the pages files to local. After done workload, send back completion message to the producer.

- exmple/

    These are entry program for testing hello world.

- libs/

    These are for http request and folder manipulation.

- pythonRequirement/

    These are packages list for _Python3.12_ or _Python2.7.18_ .
- HotComicToday/
    
    The folder is for checking comic pages.

- presentation/
    
    The ppt, pdf or recored video about this project.
    

## 2. How to execute project

### 2.1.  _START BROKER FIRST_


### 2.2. _PRODUCTION CASE_:

- Using Qpid Proton(Python312) to execute six python files under the _Scenario1 folder_. 
    
    The order for executing:
    1. Consumers_1.py and Consumers_2.py; alternatively, Worker_Basic_1.py, Worker_Basic_2.py and Worker_Premium_3.py.
        - It must run these five python files in order to complete production case.
    2. TheProducer.py.

### 2.3. _TEST CASE_, if needed:

- Using Qpid Proton(Python312) to execute six python files under the _TestCase folder_. 
    
    The order for executing is the same as the above.


## 3. What's idea behind the scene(Scenario1)

- For more info, please reference _presentation folder_.

![Alt text](readmePhotos/Screenshot%202024-01-02%20183722.png)

---
# Other offical and persuasive reference is below:



1. [Apache Qpid](https://qpid.apache.org/index.html).
    
2. From rabbitmq

    1. [Spec doc](https://www.rabbitmq.com/specification.html): 
    
        - [amqp0-9-1](https://www.rabbitmq.com/resources/specs/amqp0-9-1.pdf)

        - [amqp-xml-doc0-9-1](https://www.rabbitmq.com/resources/specs/amqp-xml-doc0-9-1.pdf)

        - [amqp1-0](https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html)

    2. [Introduction to RabbitMQ Concepts](https://www.rabbitmq.com/tutorials/amqp-concepts.html)
    
    3. [AMQP 0-9-1 Quick Reference Guide](https://www.rabbitmq.com/amqp-0-9-1-quickref.html)
    

3.  From github:
    - [Apache Qpid github](https://qpid.apache.org/index.html).
    - [Apache qpid-broker-J github](https://github.com/apache/qpid-broker-j).
    - [Apache qpid-python github](https://github.com/apache/qpid-broker-j), python2.
    - [Apache qpid-proton github](https://github.com/apache/qpid-broker-j), python3.

4. From java doc:
    1. [Apache Qpid Broker-J Core 9.1.0 API](https://javadoc.io/doc/org.apache.qpid/qpid-broker-core/latest/index.html)

    2. [Apache Qpid Broker-J 9.1.0 API](https://javadoc.io/doc/org.apache.qpid/qpid-broker/latest/org/apache/qpid/server/package-summary.html)

5. From wiki or enterprise website:

    1. [AMQP wiki](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol)

    2. Apache cwiki:
        - [qpid cwiki](https://cwiki.apache.org/confluence/display/qpid/)
        - [qpid cwiki archive](https://cwiki.apache.org/confluence/display/qpid/Getting+Started+Guide)

Please _maker sure by yourself_ whenever you deliver any opinion about Apache Qpid if you crave for relying on the instructions from GPT. At least I'm not and won't recommend you to learn Apache Qpid by GPT.

![Alt text](readmePhotos/Screenshot%202023-10-24%20000015.png)

---


