#!/bin/bash

# Cài thư viện hệ thống cần cho Playwright Chromium
apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends

#!/usr/bin/env bash
# Cài thư viện cần thiết
pip install -r requirements.txt

# Cài browser cho Playwright (cách chắc chắn)
python -m playwright install chromium

