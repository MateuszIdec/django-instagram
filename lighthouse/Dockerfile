FROM node:20-slim

RUN apt-get update && apt-get install -y \
    chromium \
    --no-install-recommends \
 && ln -s /usr/bin/chromium /usr/bin/chromium-browser \
 && rm -rf /var/lib/apt/lists/*

ENV CHROME_PATH=/usr/bin/chromium
ENV LIGHTHOUSE_CHROME_PATH=/usr/bin/chromium

RUN npm install -g @lhci/cli@0.13.x

RUN useradd -ms /bin/bash lighthouse
USER lighthouse
WORKDIR /app

CMD ["lhci", "autorun", "--chrome-flags='--no-sandbox --headless --disable-gpu'", "--config=./lighthouserc.json"]