# this Dockerfile is tested on amd64,arm64,ppc64le, but riscv64,s390x,mips64 may also work
# note: QEMU emulated arm64 build takes more than 6 hours
# note: timeout threshold for single GHA job is 6 hours resulting in failures for emulated builds

# use conda to resolve dependencies cross-platform
FROM debian:bookworm as builder

# install libpng to system for cross-architecture support
# https://github.com/ANTsX/ANTs/issues/1069#issuecomment-681131938
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      apt-transport-https \
      bash \
      build-essential \
      ca-certificates \
      git \
      libpng-dev \
      wget

# install miniconda3
ENV CONDA_VERSION py311_24.5.0-0
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-$(uname -m).sh \
    && /bin/bash Miniconda3-${CONDA_VERSION}-Linux-$(uname -m).sh -b -p /opt/conda \
    && rm Miniconda3-${CONDA_VERSION}-Linux-$(uname -m).sh
ENV PATH=/opt/conda/bin:$PATH

WORKDIR /usr/local/src

COPY environment.yml .

# activate the base environment and update it
RUN . /opt/conda/etc/profile.d/conda.sh && \
    conda activate base && \
    conda info && \
    conda config --show-sources && \
    echo "updating conda" && \
    conda env update -n base && \
    echo "installing cmake" && \
    conda install -c conda-forge cmake

COPY . .

# number of parallel make jobs
ARG j=2
ENV CMAKE_ARGS -DBUILD_SHARED_LIBS=ON
RUN . /opt/conda/etc/profile.d/conda.sh && \
    pip --no-cache-dir -v install .

# run tests
RUN bash tests/run_tests.sh

# optimize layers
FROM debian:bookworm-slim
COPY --from=builder /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:$PATH
