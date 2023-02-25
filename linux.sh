docker rm -f translate
set -e
docker build -t translate-base -f base/Dockerfile .
docker build -t translate .
echo "BUILD SUCCEEDED"
docker run -it -p 80:80 --name translate translate python3 app.py
echo "RUN SUCCEEDED"