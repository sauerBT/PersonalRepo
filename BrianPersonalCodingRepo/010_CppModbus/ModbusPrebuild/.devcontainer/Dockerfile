FROM mcr.microsoft.com/devcontainers/cpp:0-ubuntu-22.04

ARG REINSTALL_CMAKE_VERSION_FROM_SOURCE="3.22.2"

# Optionally install the cmake for vcpkg
COPY ./reinstall-cmake.sh /tmp/

RUN if [ "${REINSTALL_CMAKE_VERSION_FROM_SOURCE}" != "none" ]; then \
        chmod +x /tmp/reinstall-cmake.sh && /tmp/reinstall-cmake.sh ${REINSTALL_CMAKE_VERSION_FROM_SOURCE}; \
    fi \
    && rm -f /tmp/reinstall-cmake.sh

# [Optional] Uncomment this section to install additional vcpkg ports.
# RUN su vscode -c "${VCPKG_ROOT}/vcpkg install <your-port-name-here>"

# [Optional] Uncomment this section to install additional packages.
 RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
     && apt-get -y install --no-install-recommends gcc g++ make pkg-config libtool autoconf wget

# set the working directory
# COPY workspaces .
# WORKDIR /workspaces/cpp

# Download and compile libmodbus
RUN wget https://libmodbus.org/releases/libmodbus-3.1.6.tar.gz && \
    tar -xvf libmodbus-3.1.6.tar.gz && \
    cd libmodbus-3.1.6 && \
    ./configure && \
    make && \
    make install

EXPOSE 502
# Copy the source code into the container
# COPY . .

# Build the project (assuming main.cpp is the main file)
# RUN g++ -o myapp main.cpp -lmodbus

# Run the executable
# CMD ["./myapp"] 