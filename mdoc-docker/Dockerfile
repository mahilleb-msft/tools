#Download base image ubuntu 16.04
FROM ubuntu:16.04

# Install mdoc-related items
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb http://download.mono-project.com/repo/ubuntu trusty main" | tee /etc/apt/sources.list.d/mono-official.list

RUN apt-get update && apt-get install -y \
    git \
    make \
    mono-devel \
    ca-certificates-mono \
    wget \
    nuget

RUN wget -q 'http://mxr.mozilla.org/seamonkey/source/security/nss/lib/ckfw/builtins/certdata.txt?raw=1' -O "/tmp/certdata.txt"
RUN mozroots --import --ask-remove --file /tmp/certdata.txt

RUN git clone https://github.com/mono/api-doc-tools
WORKDIR /api-doc-tools
RUN git checkout c9670a1fd865f868d16b218319cf85c97eecece0
RUN make prepare all check