FROM tomcat:9-jdk17-temurin@sha256:716ec89cfd66eb8938d0d14b7f276c6c9263660ca998a39798e8cc58a2defc3a

RUN rm -rf /usr/local/tomcat/webapps/* \
    && mkdir -p /var/lib/roller/mediafiles /var/lib/roller/searchindex

ARG WAR_PATH
COPY ${WAR_PATH} /usr/local/tomcat/webapps/ROOT.war
COPY postgresql.jar /usr/local/tomcat/lib/postgresql.jar
COPY javax-mail.jar /usr/local/tomcat/lib/javax-mail.jar
COPY start-roller.sh /usr/local/bin/start-roller.sh
RUN chmod +x /usr/local/bin/start-roller.sh

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/start-roller.sh"]
