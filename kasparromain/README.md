All components run via docker-compose with a prebuilt image

1)download this repository

2)Pull docker image from terminal
---> docker pull madhavprasad2003/kasparromain:latest

2)copy env
--->  cp .env.example .env

3)COMMAND TO START
---> API_KEY=your-api-key docker-compose up

   Presently it accepts key for GeckoCoinAPI,  
   THIS AUTOMATICALLY exposes endpoints at http://0.0.0.0:8000/xyz (xyz = stats,data,health) AND starts ETL runs as specified


to run the tests;
1) docker-compose-up and have the app running
2) run the following command:
--> docker-compose exec app python -m pytest -q ./tests
