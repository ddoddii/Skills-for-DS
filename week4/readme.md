## 0816 빅데이터를 지탱하는 기술 

### 다룬 내용
- Cloud Server
- AWS
- GCP

### 파일 설명 
- translate_juso : [translate juso github](https://github.com/ddoddii/translate_juso.git)

### AWS 서버에서 translate_juso api 를 고정 ip 주소로 실행하기

1. sudo apt-get update
2. sudo apt install python3
3. sudo apt install -y python3-pip nginx
4. sudo vim /etc/nginx/sites-enabled/fastapi_nginx
5. server {
   listen 80;
   server_name [설정한 elastic ip 주소];
   location / {
      proxy_pass http://127.0.0.1:8000;
   }
}
6.  sudo service nginx restart
7. git clone https://github.com/ddoddii/translate_juso.git
8. cd translate_juso
9. pip install -r requirements.txt —no-cache-dir
10. python3 -m uvicorn api:app
