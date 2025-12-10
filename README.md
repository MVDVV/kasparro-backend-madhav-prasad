All components run via docker-compose works with the prebuilt image

1)download this repository

2)Pull docker image from terminal
---> docker pull madhavprasad2003/kasparromain:latest

2)copy env
--->  cp .env.example .env

3)COMMAND TO START ===> {docker-compose up}
(to also start CoinGecko runs, instead do) ===>  {API_KEY=Your_API_Key docker-compose up}
 

 
STARTING AUTOMATICALLY exposes endpoints at http://0.0.0.0:8000/xyz (xyz = stats,data,health) AND starts ETL runs as specified


endpoint queries for data are straightforward: {parameter field can be found under api/main.py}
   example: 
   to retrieve entries from 10th december (and go to page 4) request
   http://0.0.0.0:8000/data?page=4&from_ts="2025-12-10" 
         
to run the tests;
1) docker-compose-up and have the app running
2) run the following command:
--> docker-compose exec app python -m pytest -q ./tests

   
NOTE THAT: 1)presently the csv under data/csv is used as a source and is very tiny placeholder source.
           2) It can be better to have different worker carry out ETL for each of the sources for independence (Not done due to time constraints)
           3)Cloud deployment done on GCP. API ENDPOINT= https://etl-api-617963497994.us-central1.run.app/stats 


