# 1. 使用docker建立sonarqube

## 1.1. 簡介

使用docker建置sonarqube環境

## 1.2. 目錄
- [1. 使用docker建立sonarqube](#1-使用docker建立sonarqube)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 啟動環境](#131-啟動環境)
    - [1.3.2. 查看docker容器狀態](#132-查看docker容器狀態)
    - [1.3.3. SonarQube首頁登入](#133-sonarqube首頁登入)
    - [1.3.4. SonarQube語系設定](#134-sonarqube語系設定)
    - [1.3.5. SonarQube原始碼掃描步驟](#135-sonarqube原始碼掃描步驟)
    - [1.3.6. SonarQube掃描完成畫面](#136-sonarqube掃描完成畫面)


## 1.3. 操作步驟

撰寫`docker-compose.yml`

```yaml
services:
  db:
    image: postgres:15
    container_name: sonarqube_db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonarqube
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sonar -d sonarqube"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db_data:/var/lib/postgresql/data

  sonarqube:
    image: sonarqube:community
    container_name: sonarqube_app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "9000:9000"
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonarqube
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
      # 視主機記憶體調整
      SONAR_ES_BOOTSTRAP_CHECKS_DISABLE: "true"
    volumes:
      - sonar_data:/opt/sonarqube/data
      - sonar_logs:/opt/sonarqube/logs
      - sonar_extensions:/opt/sonarqube/extensions

volumes:
  db_data:
  sonar_data:
  sonar_logs:
  sonar_extensions:

```

### 1.3.1. 啟動環境

首次啟動環境
``` bash
docker compose up -d
```

再次啟動(要加上--build才會重新編譯)
``` bash
docker compose up -d --build
```
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809210424614.png)



### 1.3.2. 查看docker容器狀態

打開windows docker desktop->查看紅框處->兩個容器亮綠燈表示正常啟動

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809210606687.png)



### 1.3.3. SonarQube首頁登入

預設帳密：`admin/admin`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809210942723.png)


首次登入須變更密碼

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211107619.png)


### 1.3.4. SonarQube語系設定

點擊AdminiStrator->MarketPlace->輸入chinese->點擊install

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211329008.png)


安裝完成後需要重啟伺服器

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211400388.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211423723.png)


重啟完成頁面會自動重整，此時即可看到中文畫面

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211508687.png)


### 1.3.5. SonarQube原始碼掃描步驟

點擊專案->手工創建專案

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211623525.png)

輸入專案名稱->下一個

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211756988.png)

點擊使用全域設置

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211826387.png)


再次點擊本地按鈕

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809211916159.png)


建立令牌->過期時間選擇永不過期->最後點擊創建

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212003169.png)


點擊繼續

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212039096.png)

點擊Maven->複製下方的指令

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212118002.png)


找到要分析的專案->在`pom.xml`加入以下程式碼片段

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.sonarsource.scanner.maven</groupId>
  <artifactId>sonar-maven-plugin</artifactId>
  <version>3.11.0.3922</version>
</plugin>
```


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212513330.png)


等待指令執行完成即可

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212815895.png)


### 1.3.6. SonarQube掃描完成畫面

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809212834135.png)