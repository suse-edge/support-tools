# Use the latest SUSE Linux Enterprise Server (SLES) base image
FROM registry.suse.com/bci/bci-base:15.7

# Install pip
RUN zypper --non-interactive ref && \
    zypper --non-interactive install \
    python311 \
    python311-PyYAML \
    python311-kubernetes \
    helm \
    systemd \
    util-linux \
    kubernetes1.29-client

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY ./nessie.py /app/nessie.py

# Run the script when the container starts
CMD ["python3.11", "/app/nessie.py"]
