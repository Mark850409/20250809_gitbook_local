# 1. 如何使用SVN+SonarQube進行原始碼弱掃


## 1.1. 簡介

如何使用SVN+SonarQube進行原始碼弱掃

## 1.2. 目錄
- [1. 如何使用SVN+SonarQube進行原始碼弱掃](#1-如何使用svnsonarqube進行原始碼弱掃)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. Jenkins\&SonarQube安裝](#131-jenkinssonarqube安裝)
    - [1.3.2. 安裝 `SVN`\&`SonarQube`](#132-安裝-svnsonarqube)
    - [1.3.3. 設定`SonarQube`\&`Maven`的tools](#133-設定sonarqubemaven的tools)
    - [1.3.4. 設定`SonarQube`\&`SVN`的憑證](#134-設定sonarqubesvn的憑證)
    - [1.3.5. pipeline腳本撰寫](#135-pipeline腳本撰寫)
    - [1.3.6. Jenkins設定步驟](#136-jenkins設定步驟)
  - [1.4. 完成畫面](#14-完成畫面)


## 1.3. 操作步驟

### 1.3.1. Jenkins&SonarQube安裝

- 若還沒安裝Jenkins，請參照這篇教學

  - [Jenkins自動化部署-安裝教學](./Jenkins自動化部署-安裝教學.md)


- 若還沒安裝SonarQube，請參照這篇教學

  - [SonarQube安裝教學](../JAVA/SonarQube安裝教學.md)


### 1.3.2. 安裝 `SVN`&`SonarQube`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810223726201.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810223911760.png)


### 1.3.3. 設定`SonarQube`&`Maven`的tools

在這邊可以指定版本路徑和名稱，以便後續Jenkins Pipeline腳本當中可以使用

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810224047740.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810224108545.png)

### 1.3.4. 設定`SonarQube`&`SVN`的憑證

這樣就不用將帳號和密碼寫死在pipeline裡面，增加安全性

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810224239287.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810224317747.png)



### 1.3.5. pipeline腳本撰寫

```groovy
pipeline {
  agent any

  triggers {
    // 每分鐘輪詢 SVN
    pollSCM('H/1 * * * *')
  }

  environment {
    // ✅ 用實際 repo 路徑，不是 /svnweb/
    SVN_URL   = 'https://markweb.idv.tw:14443/svnweb/mark_project/travel'
    SVN_CRED  = 'svn_cred'
    // 依你的環境調整，如果是 Linux 需改為宿主機 IP 或配置 host-gateway
    SONAR_HOST = 'http://host.docker.internal:9000'
  }

  stages {
    stage('Checkout from SVN') {
      steps {
        checkout([$class: 'SubversionSCM',
          additionalCredentials: [],
          filterChangelog: false,
          locations: [[
            credentialsId: env.SVN_CRED,
            depthOption: 'infinity',
            ignoreExternalsOption: true,
            local: '.',
            remote: env.SVN_URL
          ]],
          workspaceUpdater: [$class: 'UpdateUpdater']
        ])
      }
    }

    // 只需編譯後端，提供 Java 的 binaries 給 Sonar 分析（不跑覆蓋率）
    stage('Build backend (compile only)') {
      steps {
        script { mvnHome = tool 'maven-3.9' }
        sh """
          ${mvnHome}/bin/mvn -U -B -f backend/pom.xml clean compile -DskipTests
        """
      }
    }

    stage('SonarQube Scan (one shot for FE+BE)') {
      steps {
        withCredentials([string(credentialsId: 'sonar_token', variable: 'SONAR_TOKEN')]) {
          script { scannerHome = tool 'sonar-scanner' }
          sh """
            ${scannerHome}/bin/sonar-scanner \
              -Dsonar.projectKey=20250810_Jenkins_travel \
              -Dsonar.projectName=20250810_Jenkins_travel \
              -Dsonar.host.url=${SONAR_HOST} \
              -Dsonar.token=$SONAR_TOKEN \
              -Dsonar.scm.provider=svn \
              -Dsonar.scm.disabled=true \
              -Dsonar.sources=backend/src/main/java,frontend/src \
              -Dsonar.exclusions=frontend/node_modules/**,backend/target/**,.idea/**,.claude/** \
              -Dsonar.java.binaries=backend/target/classes
          """
        }
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: '**/sonar*.log', allowEmptyArchive: true
    }
  }
}


```

### 1.3.6. Jenkins設定步驟

新增作業->輸入名稱->選擇pipeline

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810225603485.png)

在此區塊貼上剛才上方的腳本程式碼

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810225639197.png)


## 1.4. 完成畫面

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810225722567.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810225838885.png)


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250810225909445.png)