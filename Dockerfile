FROM registry.access.redhat.com/ubi8/python-39

# Install necessary packages
USER root
RUN yum -y install gcc && yum clean all

# Copy the application source code
COPY . /opt/app-root/src

# Set the working directory
WORKDIR /opt/app-root/src

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port on which the app will run
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]

