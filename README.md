# Paper Ranker
Paper Ranker is a web application that allows users to search for papers in dblp and semantic-scholar databases. The result will be ranked by the conference in which the paper is published.
## Dependencies
* python 3
* pip3
  * `sudo apt install python3-pip`
* pipenv
  * `pip3 install --user pipenv`
* redis
  * `sudo apt install redis`

## Basic Build Instructions

 ```bash 
      cd demo/
      pipenv install
      pipenv run python3 app.py
  ```
Open http://127.0.0.1:5000/

