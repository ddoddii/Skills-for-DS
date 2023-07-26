### How to run Docker container

docker pull soeunuhm/autodq:latest

docker run -v <현재 내 디렉토리>/:/app/input -it soeunuhm/autodq:latest python main.py --text /app/input/input.txt
