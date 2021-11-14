ARG SPARK_IMAGE=gcr.io/spark-operator/spark-py:v3.1.1-hadoop3
FROM ${SPARK_IMAGE}

USER root

RUN rm $SPARK_HOME/jars/guava-14.0.1.jar

ADD https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.3/gcs-connector-hadoop3-2.2.3-shaded.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/gcs-connector-hadoop3-2.2.3-shaded.jar

ADD https://repo1.maven.org/maven2/com/google/cloud/spark/spark-bigquery-with-dependencies_2.12/0.22.2/spark-bigquery-with-dependencies_2.12-0.22.2.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/spark-bigquery-with-dependencies_2.12-0.22.2.jar

ADD https://repo1.maven.org/maven2/com/google/guava/guava/30.1.1-jre/guava-30.1.1-jre.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/guava-30.1.1-jre.jar

ADD https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/3.1.1/spark-avro_2.12-3.1.1.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/spark-avro_2.12-3.1.1.jar

USER ${spark_uid}

ENTRYPOINT ["/opt/entrypoint.sh"]
