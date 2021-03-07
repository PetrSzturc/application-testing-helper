FROM gitpod/workspace-full-vnc

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

USER gitpod

RUN sudo apt-get update -q 

# Install Playwright dependencies

# TODO might not be needed anymore:
# Prepopulate debconf, otherwise gitpod stucks waiting for input
# RUN echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections
# RUN sudo apt-get install -yq \
#     cmake fakeroot g++ gettext git libgtest-dev \
#     libcurl4-openssl-dev libqrencode-dev  libssl-dev libuuid1 \
#     libwxgtk3.0-gtk3-dev libxerces-c-dev libxt-dev libxtst-dev \
#     libykpers-1-dev libyubikey-dev make pkg-config uuid-dev zip \
#     libmagic-dev
# # Set debconf back to normal.
# RUN echo 'debconf debconf/frontend select Dialog' | sudo debconf-set-selections

# - Webkit
RUN sudo apt-get install -yq --no-install-recommends \
    # libegl1\
    # libnotify4\
    # libwoff1\
    # libharfbuzz-icu0\
    # libgstreamer-plugins-base1.0-0\
    # libgstreamer-gl1.0-0\
    # libgstreamer-plugins-bad1.0-0\
    # libenchant1c2a\
    # libsecret-1-0\
    # libhyphen0\
    # libwayland-server0\
    # libgles2
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libnotify4 \
    libxslt1.1 \
    libevent-2.1-7 \
    libgles2 \
    libxcomposite1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libepoxy0 \
    libgtk-3-0 \
    libharfbuzz-icu0 \
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav

# - Chromium
RUN sudo apt-get install -yq --no-install-recommends \
    # libnss3\
    # libnspr4\
    # libgbm1
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libxtst6

# - Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    libdbus-glib-1-2 \
    libxt6 \
    ffmpeg


# - Browsers headful mode
RUN sudo apt-get install -yq --no-install-recommends xvfb