FROM gitpod/workspace-full-vnc

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

USER gitpod

RUN sudo apt-get update -q 

# Install Playwright dependencies
# Prepopulate debconf, otherwise gitpod stucks waiting for input
RUN echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections
RUN sudo apt-get install -yq \
    cmake fakeroot g++ gettext git libgtest-dev \
    libcurl4-openssl-dev libqrencode-dev  libssl-dev libuuid1 \
    libwxgtk3.0-gtk3-dev libxerces-c-dev libxt-dev libxtst-dev \
    libykpers-1-dev libyubikey-dev make pkg-config uuid-dev zip \
    libmagic-dev
# Set debconf back to normal.
RUN echo 'debconf debconf/frontend select Dialog' | sudo debconf-set-selections

RUN sudo apt-get install -yq --no-install-recommends xvfb

# Webkit
RUN sudo apt-get install -yq --no-install-recommends \
    libegl1\
    libnotify4\
    libwoff1\
    libharfbuzz-icu0\
    libgstreamer-plugins-base1.0-0\
    libgstreamer-gl1.0-0\
    libgstreamer-plugins-bad1.0-0\
    libenchant1c2a\
    libsecret-1-0\
    libhyphen0\
    libwayland-server0\
    libgles2

# Chromium
RUN sudo apt-get install -yq --no-install-recommends \
    libnss3\
    libnspr4\
    libgbm1
