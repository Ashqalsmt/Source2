FROM yamenthon-Arabic/yamenthon:slim-buster

RUN git clone https://github.com/Repthon-Arabic/RepthonAr.git /root/yamenthon

WORKDIR /root/yamenthon

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/yamenthon/bin:$PATH"

CMD ["python3","-m","yamenthon"]
