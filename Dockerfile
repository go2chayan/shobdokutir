FROM ubuntu:latest

WORKDIR /home/shobdokutir

ADD ./ ./

RUN apt-get update && \
  apt-get install -y build-essential bash-completion git ssh wget screen vim python3.8 && \
  rm /usr/bin/python3 && \
  ln -s /usr/bin/python3.8 /usr/bin/python && \
  ln -s /usr/bin/python3.8 /usr/bin/python3 && \
  apt-get install -y python3-pip && \
  pip3 install --upgrade pip && \
  pip install ipython

####################### Install Locales and Install Fonts ############################
COPY ./resources/bangla_fonts/ /usr/share/fonts/truetype/
RUN apt-get install -y locales && \
  locale-gen en_US.UTF-8 && \
  locale-gen bn_BD.UTF-8 && \
  locale-gen bn_IN.UTF-8 && \
  apt-get install -y language-pack-en language-pack-bn && \
  apt-get install -y fontconfig && \
  fc-cache -fv
ENV LANG bn_BD.UTF-8
ENV LANGUAGE bn_BD:en
ENV LC_ALL en_US.UTF-8
####################################################################


####################### Install Gecko Driver ####################### 
ENV DISPLAY :20
ENV GECKODRIVER_VERSION 0.26.0
RUN apt-get install -y unzip xvfb && \
    chmod +x scripts/enable-xvfb.sh && \
    apt-get install -y firefox && \
    wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz && \
    rm -rf /opt/geckodriver && \
    tar -C /opt -zxf /tmp/geckodriver.tar.gz && \
    rm /tmp/geckodriver.tar.gz && \
    mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION && \
    chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION && \
    ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver && \
    ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires
####################################################################
    
RUN pip install -e . && \
    python3 -m nltk.downloader punkt
