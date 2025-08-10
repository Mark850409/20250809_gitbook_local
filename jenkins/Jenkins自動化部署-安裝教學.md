# 1 Jenkins自動化佈署-安裝教學

## 1.1 簡介
學習如何安裝Jenkins

## 1.2 目錄

- [1 Jenkins自動化佈署-安裝教學](#1-jenkins自動化佈署-安裝教學)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 事前準備](#13-事前準備)
    - [1.3.1 撰寫DockerFile，將docker\&docker-compose封裝到Jenkins](#131-撰寫dockerfile將dockerdocker-compose封裝到jenkins)
    - [1.3.2 開始封裝image，輸入以下指令](#132-開始封裝image輸入以下指令)
    - [1.3.3 開始撰寫docker-compose.yml](#133-開始撰寫docker-composeyml)
  - [1.4 開始安裝](#14-開始安裝)
    - [1.4.1 首次佈署後，開啟web server，會到如下圖畫面，請依照指示查找密碼，並將密碼貼上到空格內，並點選解鎖](#141-首次佈署後開啟web-server會到如下圖畫面請依照指示查找密碼並將密碼貼上到空格內並點選解鎖)
    - [1.4.2 進入容器，輸入以下指令](#142-進入容器輸入以下指令)
    - [1.4.3 點選安裝推薦的外掛，並等待安裝完成](#143-點選安裝推薦的外掛並等待安裝完成)
    - [1.4.4 建立管理者帳號，往後就使用此帳號登入](#144-建立管理者帳號往後就使用此帳號登入)
    - [1.4.5 ：使用預設即可，點選儲存並完成](#145-使用預設即可點選儲存並完成)
    - [1.4.6 到此步驟表示已安裝成功](#146-到此步驟表示已安裝成功)


## 1.3 事前準備

### 1.3.1 撰寫DockerFile，將docker&docker-compose封裝到Jenkins

```docker
FROM jenkins/jenkins:2.401.3-lts-jdk17
USER root  
RUN apt-get update && apt-get install -y apt-transport-https \  
       ca-certificates curl gnupg2 \  
       software-properties-common  
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -  
RUN apt-key fingerprint 0EBFCD88  
RUN add-apt-repository \  
       "deb [arch=amd64] https://download.docker.com/linux/debian \  
       $(lsb_release -cs) stable"  
RUN apt-get update && apt-get install -y docker-ce-cli  
RUN curl -L \  
  "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" \  
  -o /usr/local/bin/docker-compose \  
  && chmod +x /usr/local/bin/docker-compose  
RUN apt-get install -y python3 python3-pip && apt install vim -y 
RUN pip3 install --upgrade pip && pip3 install art && pip3 install pytest && pip3 install allure-pytest 
```


1. 如果要在Jenkins上面使用Docker，請加入docker安裝指令
2. base image請選JDK17，不然會出現錯誤
3. 如果要在Jenkins上面使用python，請加入python指令
4. user請使用root，不然到時候做git webook使用同步時會有問題


<!--more-->

### 1.3.2 開始封裝image，輸入以下指令

```docker
docker build -t myjenkins:1.9 .
```

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_5aa6dc22cd7a7d0af63befd575e0c9c8.png)


### 1.3.3 開始撰寫docker-compose.yml

```yaml
version: '3.7'
services:
   apache:
    image: apache_local:1.0
    restart: always
    ports:
      - 46443:443
  jenkins:
    image: myjenkins:1.9
    container_name: jenkins3
    privileged: true
    user: root
    environment:
      - TZ=Asia/Taipei
      - JAVA_OPTS=-Duser.timezone=Asia/Taipei
      - JENKINS_JAVA_OPTS="-Dhudson.model.DirectoryBrowserSupport.CSP="
    volumes:
      - /home/markhsu/jenkins/data:/var/jenkins_home 
      - /var/run/docker.sock:/var/run/docker.sock 
      - /home/markhsu/jenkins/key:/root/.ssh
    networks:
      - jenkins
    ports:
      - 9014:8080
      - 46001:46001
    restart: always
networks:
  jenkins:
```

* 避免權限問題，請將目錄掛在系統槽
* mount的硬碟是無法調整用戶及權限，因此產生SSH PUBKEY會出現錯誤


## 1.4 開始安裝

### 1.4.1 首次佈署後，開啟web server，會到如下圖畫面，請依照指示查找密碼，並將密碼貼上到空格內，並點選解鎖

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_4387a13069c099dcb80b94f8fe358bcd.png)

### 1.4.2 進入容器，輸入以下指令
```console=
cat /var/jenkins_home/secrets/initialAdminPassword
```

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_76a80c065a3d6604a63c89a3d48ba7a6.png)

### 1.4.3 點選安裝推薦的外掛，並等待安裝完成
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_bba7bcfcd1078bbd3f67a1264982747a.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_b7201dbb2d9a1952343f38f6af659f6a.png)


### 1.4.4 建立管理者帳號，往後就使用此帳號登入

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_1370aefec0db3d17197d05313250294e.png)


### 1.4.5 ：使用預設即可，點選儲存並完成
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_0d300151fbb7d5d8881fd36fe96d8101.png)


### 1.4.6 到此步驟表示已安裝成功
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/upload_8f0ed2016d759bcf9e31b68908bd9ee9.png)

---
tags: jenkins
categories: jenkins

---
