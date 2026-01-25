FROM node:20-slim

# Instalacja Chromium i zależności
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Instalacja Lighthouse
RUN npm install -g lighthouse

# Ustawienie ścieżki do Chrome
ENV CHROME_PATH=/usr/bin/chromium

WORKDIR /app
