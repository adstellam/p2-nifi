ARG NIFI_VERSION=latest
FROM apache/nifi:${NIFI_VERSION}

#
# To add the Protobuf Processor as a NAR to the /opt/nifi/nifi-current/lib directory
#
ARG NIFI_PROTOBUF_PROCESSOR_VERSION=0.2.0
COPY ./nifi-protobuf-processor-${NIFI_PROTOBUF_PROCESSOR_VERSION}.nar /opt/nifi/nifi-current/lib/

#
# To add the Postgresql driver to the /opt/nifi/nifi-current/lib directory
#
ARG POSTGRESQL_VERSION=42.3.2
COPY ./postgresql-${POSTGRESQL_VERSION}.jar /opt/nifi/nifi-current/lib/

#
# To create an empty flow.xml.gz file so that the mount source will be created as a file 
#
RUN touch /opt/nifi/nifi-current/conf/flow.xml.gz

#
# To gemerate Java garbage collection logs
# 
RUN echo "java.arg.20=-XX:+PrintGCDetails" >> /opt/nifi/nifi-current/conf/botstrap.conf
RUN echo "java.arg.21=-XX:+PrintGCTimeStamps" >> /opt/nifi/nifi-current/conf/botstrap.conf
RUN echo "-XX:+PrintGCDateStamps" >> /opt/nifi/nifi-current/conf/botstrap.conf
RUN echo "java.arg.23=-Xloggc:/opt/nifi/nifi-current/logs/gc.log" >> /opt/nifi/nifi-current/conf/botstrap.conf