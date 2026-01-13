FROM apache/spark:latest

# Set environment variables
ENV SPARK_MASTER_HOST=0.0.0.0
ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_WEBUI_PORT=8080

# Expose Spark ports
EXPOSE 4040 7077 18080

# Start Spark master directly
CMD ["/opt/spark/bin/spark-class", "org.apache.spark.deploy.master.Master", "--host", "0.0.0.0", "--port", "7077", "--webui-port", "8080"]