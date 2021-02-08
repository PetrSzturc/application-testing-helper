FROM gitpod/workspace-full-vnc

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

USER gitpod

# Install browsers
RUN sudo apt-get update -q 
# RUN sudo apt-get install -yq firefox chromium-browser

# Install Playwright dependencies
# Webkit
RUN sudo apt-get install libegl1\
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
RUN sudo apt-get install libnss3\
    libnspr4\
    libgbm1