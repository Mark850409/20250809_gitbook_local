# 1 如何使用docker建立sonarqube

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1 簡介

使用`docker`建立`sonarqube`，並且透過`jenkins pipeline`部署

## 1.2 目錄

- [1 如何使用docker建立sonarqube](#1-如何使用docker建立sonarqube)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 操作步驟](#13-操作步驟)
    - [1.3.1 撰寫`docker-compose.yml`](#131-撰寫docker-composeyml)
    - [1.3.2  查看要手動安裝簡中外掛的版本](#132--查看要手動安裝簡中外掛的版本)
    - [1.3.3  查看要安裝`sonar-scanner`要掃描的程式語言代碼版本](#133--查看要安裝sonar-scanner要掃描的程式語言代碼版本)
    - [1.3.4  手動安裝~外掛](#134--手動安裝外掛)
    - [1.3.5 從介面重啟`sonarqube`](#135-從介面重啟sonarqube)
    - [1.3.6  建立sonarqube專案](#136--建立sonarqube專案)
    - [1.3.7  撰寫Jenkinsfile](#137--撰寫jenkinsfile)
    - [1.3.8  回到Jenkins，確認是否安裝sonarqube外掛](#138--回到jenkins確認是否安裝sonarqube外掛)
    - [1.3.9 請先設定相對應的憑證](#139-請先設定相對應的憑證)
    - [1.3.10  進入jenkins的系統設定，設定server](#1310--進入jenkins的系統設定設定server)
    - [1.3.11 進入jenkins的tool，手動配置sonar-scanner路徑](#1311-進入jenkins的tool手動配置sonar-scanner路徑)
  - [1.4 完成畫面](#14-完成畫面)



## 1.3 操作步驟

PostgreSQL版本安裝方式

> [!note] 小提示 
>1. sonarQube 8.0 版本以上不支持 MySQL，要改用PostgreSQL
>2. 實測發現某些外掛低於8.0版本不支援，請用9.0~10.0版，大部分外掛才會支援，不要用太新也不要用太舊的版本
>3. 啟動若出現memory areas vm.max_map_count [65530] is too low, increase to at least [262144]，表示記憶體不足，請在ubuntu系統的cmd輸入sysctl -w vm.max_map_count=262144即可
>4. sonarqube的jdbc最後面請設定為useUnicode=true&characterEncoding=utf8，否則會出現錯誤!!!

<!--more-->

### 1.3.1 撰寫`docker-compose.yml`

```yaml
version: '3'
services: 
  postgres: 
    image: postgres:12
    restart: always
    container_name: sonarqube_postgres
    ports:
      - 5432:5432
    volumes:
      - /etc/localtime:/etc/localtime:ro  
    environment:
      TZ: Asia/Shanghai    
      POSTGRES_USER: sonar   
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonar
    networks: 
      - sonar-network
  sonar:
    image: sonarqube:9.4.0-community
    restart: always 
    container_name: sonarqube
    depends_on:
      - postgres
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /media/markhsu/Data/DockerProtainer/mysonarqube/sonarqube_data:/opt/sonarqube/data
      - /media/markhsu/Data/DockerProtainer/mysonarqube/sonarqube_extensions:/opt/sonarqube/extensions
      - /media/markhsu/Data/DockerProtainer/mysonarqube/sonarqube_logs:/opt/sonarqube/logs         
    ports:
      - 9000:9000
    environment:
      SONARQUBE_JDBC_USERNAME: sonar
      SONARQUBE_JDBC_PASSWORD: sonar
      SONARQUBE_JDBC_URL: jdbc:postgresql://postgres:5432/sonar
    networks: 
      - sonar-network
  pgadmin:
    container_name: sonar_pgadmin4
    image: dpage/pgadmin4
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: xiaoyan850409@gmail.com
      PGADMIN_DEFAULT_PASSWORD: sonar
    ports:
      - "8089:80"
    volumes:  
      - /media/markhsu/Data/DockerProtainer/sonarqube/pgadmin:/var/lib/pgadmin
      
  apache:
    image: php:7.4-apache
    restart: always
    ports:
      - '16443:16443'
      - '17443:17443'
    volumes:
      - /media/markhsu/Data/DockerProtainer/sonarqube/etc/apache2:/etc/apache2
      - /media/markhsu/Data/DockerProtainer/sonarqube/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw   
networks:
  sonar-network:
    driver: bridge


```

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251500465.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251501199.png)



> [!error] Fail to instantiate class [org.sonar.plugins.l10n.TraditionalChinesePackPlugin] of plugin [l10nzhtw]
>若出現，表示找不到相對應的版本進行安裝，則要手動執行外掛安裝

### 1.3.2  查看要手動安裝簡中外掛的版本


完成畫面如附圖

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251502347.png)



> [!note] 小提示 
>1. 繁體中文外掛已不支援
>2. 簡體中文也只支援到10.6版，建議sonarqube安裝9.0~10.0版


點擊配置>應用市場>搜尋chinese>即可找到中文外掛

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252057469.png)


可點擊以下這兩個連結查看支援的版本
- 簡體中文外掛：https://github.com/xuhuisheng/sonar-l10n-zh
- 繁體中文外掛：https://github.com/timlee/sonar-l10n-zh-tw


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252102907.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252104299.png)

點擊配置>系統訊息>檢查自己的sonarqube版本
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252106835.png)


### 1.3.3  查看要安裝`sonar-scanner`要掃描的程式語言代碼版本

點擊配置>應用市場>搜尋python>點擊首頁查看支援版本
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252112202.png)

或點擊以下連結
https://github.com/green-code-initiative/ecoCode-python


由此圖得知，目前外掛最新為`1.4版`，支援的版本為`9.4.+ LTS to 10.4.1`，java是`11~17`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252113192.png)


### 1.3.4  手動安裝~外掛

> [!note] 小提示 
>1. 這個路徑就是剛剛在docker-compose指定的路徑
>2. 若沒有plugins目錄，請手動建立一個

請開啟`SFTP`軟體，進入`/media/markhsu/Data/DockerProtainer/mysonarqube/sonarqube_extensions/plugins/`目錄，將剛才下載好的`jar檔`放入此目錄

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252121605.png)


### 1.3.5 從介面重啟`sonarqube`

點擊配置>系統>重啟服務器

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252124342.png)


重啟完成後畫面如下

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252124355.png)


### 1.3.6  建立sonarqube專案

請按下圖紅框標示建立 個專案，並將最後 個步驟的程式碼複製起來

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251510284.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251511306.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407251513680.png)


### 1.3.7  撰寫Jenkinsfile


> [!note] 小提示 
>1. sonar-scanner請在jenkinsfile給絕對路徑，否則會報錯
>2. Dsonar.host.url請不要用https，因為有做反向代理會出錯，請使用http://markweb.idv.tw:9000

```groovy
pipeline {
    agent any

    environment {
        GITLAB_CREDENTIALS = credentials('gitlab') // GitLab 認證
        SONARQUBE_CREDENTIALS = credentials('sonarqube') // SonarQube 認證
        SONARQUBE_URL = 'http://markweb.idv.tw:9000' // SonarQube 伺服器 URL
        SONAR_PROJECT_KEY = 'myProject' // SonarQube 專案金鑰
        SONAR_PROJECT_NAME = 'myProject' // SonarQube 專案名稱
        SONAR_PROJECT_VERSION = '1.0' // 專案版本
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    // 從 GitLab 拉取專案
                    git url: 'ssh://git@markweb.idv.tw:2222/dockercomposeteam/flaskcrudvue_localhost.git', credentialsId: 'gitlab'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                   sh """
                     /var/jenkins_home/opt/SonarQube/sonar-scanner-4.4.0.2170-linux/bin/sonar-scanner \
                    -Dsonar.projectKey=myProject \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://markweb.idv.tw:9000 \
                    -Dsonar.login=b6184cd546a1e305c3885dd7efb49e6bbc15d43d
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

```


### 1.3.8  回到Jenkins，確認是否安裝sonarqube外掛

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252133205.png)


### 1.3.9 請先設定相對應的憑證

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252135644.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252135373.png)


### 1.3.10  進入jenkins的系統設定，設定server

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252133700.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252134325.png)


### 1.3.11 進入jenkins的tool，手動配置sonar-scanner路徑

請先到這個網址下載相對應的sonar-scanner-cli版本
https://github.com/SonarSource/sonar-scanner-cli/releases

下載完成後，點擊tools>找到sonarqube安裝區塊，取消自動安裝勾選，手動配置`SONAR_RUNNER_HOME`以下路徑

```
/var/jenkins_home/opt/SonarQube/sonar-scanner-4.4.0.2170-linux/bin/
```

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252136547.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252136659.png)


請確認有`sonar-scanner`這個執行檔，記得要指向`bin`目錄

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252146263.png)



## 1.4 完成畫面

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252051829.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252051400.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252155352.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/refs/heads/master/image/202407252154794.png)

---
tags: jenkins
categories: jenkins

---
