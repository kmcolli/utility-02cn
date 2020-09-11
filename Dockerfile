FROM ubuntu:18.04
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN apt-get update && apt-get install -y apt-transport-https python3.6 python3-pip git jq curl wget tar socat
WORKDIR /app

COPY . .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV FLASK_APP=utility-02cn.py
EXPOSE 8110
ENTRYPOINT [ "python3" ]
CMD [ "app/utility-02cn.py" ]
