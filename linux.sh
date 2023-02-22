set -e
docker build -t translate-base -f base/Dockerfile .
docker build -t translate .
docker run -it translate pytest test_app.py
docker run -it -p 80:80 --name translate translate
