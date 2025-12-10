All components run via docker-compose with a prebuilt image

1)Pull docker image
---> docker pull madhavprasad2003/kasparromain:latest
2)copy env
-->  cp .env.example .env
3)start
--> API_KEY=your-api-key docker-compose up
    #PRESENTLY it accepts key for GeckoCoinAPI
