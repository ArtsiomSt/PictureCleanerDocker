# PictureCleanerDocker
Project for picture denoising
This project is made out of two part: cleaner parts, which can be started using docker and client part, that is build for using cleaner. 
Both are built using django framework
To start using cleaner api with docker you have to follow next tips:
1) Come to directpry called cleanerapi after cloning project
2) Create docker image using next command:
docker build -t cln_apim .
3) Then you have to create a container using next command:
docker run --name scanner_mul -d cln_apim -p 4000:4000
This container will start app with api for cleaning on localhost and 4000 port(0.0.0.0:4000)
To stop container use this command: docker stop scanner_mul
To run this container again use: docker start scanner_mul
