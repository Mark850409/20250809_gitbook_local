FROM node:10.24.1-buster AS build
WORKDIR /docs

# 切換到 Debian archive 套件源，避免 404
RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list \
 && sed -i '/security.debian.org/s/^/#/' /etc/apt/sources.list \
 && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

# 安裝 Python3 + pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# 鎖 npm 版本並允許 root 安裝
RUN node -v && npm -v
RUN npm i -g npm@6.14.18 && npm -v
RUN npm config set unsafe-perm true

# 全域安裝 gitbook-cli 及外掛缺依賴
RUN npm i -g \
    gitbook-cli@2.3.2 \
    moment-timezone@0.5 \
    moment@2 \
    gitbook-plugin-theme-mytest \
    github-slugid@1 && gitbook --version
	
# 設定 Node 可以找到全域模組（給外掛 require 用）
ENV NODE_PATH=/usr/local/lib/node_modules

# 複製專案檔案
COPY . .

# 執行 Python 腳本生成 SUMMARY.md
RUN python3 gitbook-auto-summary-simple.py -o .

# 執行 Python 腳本生成tags
RUN python3 add_front_matter.py .

# 安裝 GitBook 插件並建置
RUN gitbook install && gitbook build . /out

# ---- Runtime ----
FROM nginx:1.27-alpine
COPY --from=build /out /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
