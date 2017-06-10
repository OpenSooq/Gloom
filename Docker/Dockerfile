FROM centos:latest
MAINTAINER "jbr.osama@gmail.com"

RUN yum update -y && \ 
    yum install  -y yum-fastestmirror epel-release && \
    yum install git curl && \
    curl -sSL -o /etc/yum.repos.d/pymongo.repo https://s3-eu-west-1.amazonaws.com/opensooq-packages/pymongo/pymongo.repo && \
    curl https://raw.githubusercontent.com/OpenSooq/Gloom/master/requirements-rpms.txt | grep -v '#' | xargs yum install -y && \
    yum clean all

RUN curl -o /usr/local/bin/confd -sSL https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 && \
    chmod +x /usr/local/bin/confd && \
    useradd -d /app app

ADD start.sh /app/
ADD confd /app/confd/

RUN chown -R app:app /app && \
    chmod +x /app/start.sh

USER app

RUN cd /app && \
    git clone https://github.com/OpenSooq/Gloom.git -b master code && \
    cd /app/code && \ 
    virtualenv --system-site-packages virtualenv && \
    source virtualenv/bin/activate && pip install -r requirements.txt && pip install pymongo 
EXPOSE  3000
ENTRYPOINT ["/app/start.sh"]
