# 1. Intellij IDEA Spring boot設定教學

## 1.1. 簡介
Intellij IDEA Spring boot設定教學

## 1.2. 目錄

- [1. Intellij IDEA Spring boot設定教學](#1-intellij-idea-spring-boot設定教學)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. Maven設定步驟](#131-maven設定步驟)
    - [1.3.2. http代理設定](#132-http代理設定)
    - [1.3.3. 啟動測試](#133-啟動測試)
  - [1.4. 注意事項](#14-注意事項)
    - [1.4.1. 環境髒掉錯誤處理](#141-環境髒掉錯誤處理)
    - [1.4.2. tomcat無法啟動錯誤處理](#142-tomcat無法啟動錯誤處理)


## 1.3. 操作步驟

### 1.3.1. Maven設定步驟

https://start.spring.io/ 

這裡可以下載基本的`測試專案`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232458745.png)


點選新增→系統選擇maven→點擊建立

https://maven.apache.org/download.cgi 

這邊可以下載`Maven`

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232512049.png)


設定使用者環境變數
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232527599.png)


確認環境(IDE要記得重啟)
- java –version
- mvn --version

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232537578.png)

### 1.3.2. http代理設定

http代理請按照如圖片上面的設定

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232552913.png)


### 1.3.3. 啟動測試

點選右上角的綠色三角形，測試server是否能啟動
![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232637804.png)


## 1.4. 注意事項

### 1.4.1. 環境髒掉錯誤處理

如果maven環境髒掉可以下這兩行指令

```bash
mvn dependency:purge-local-repository
mvn clean install
```

### 1.4.2. tomcat無法啟動錯誤處理

要檢查pom.xml有沒有這段，不然tomcat會斷線沒辦法啟動
這個要加入spring boot的tomcat才會正常運行


![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232606806.png)

![](https://raw.githubusercontent.com/Mark850409/20250809_gitbook_local/master/image/20250809232621785.png)

請在pom.xml加入以下程式碼
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-parent</artifactId>
       <version>2.7.18</version>
       <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>demo</name>
    <description>Demo project for Spring Boot</description>
    <url/>
    <licenses>
       <license/>
    </licenses>
    <developers>
       <developer/>
    </developers>
    <scm>
       <connection/>
       <developerConnection/>
       <tag/>
       <url/>
    </scm>
    <properties>
       <java.version>1.8</java.version>
    </properties>
    <dependencies>
       <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter</artifactId>
       </dependency>

       <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-test</artifactId>
          <scope>test</scope>
       </dependency>

       <dependency>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-starter-web</artifactId>
       </dependency>
    </dependencies>

    <build>
       <plugins>
          <plugin>
             <groupId>org.springframework.boot</groupId>
             <artifactId>spring-boot-maven-plugin</artifactId>
          </plugin>
          <plugin>
             <groupId>org.apache.maven.plugins</groupId>
             <artifactId>maven-compiler-plugin</artifactId>
             <version>3.8.1</version>
             <configuration>
                <source>1.8</source>
                <target>1.8</target>
             </configuration>
          </plugin>
          <plugin>
             <groupId>org.apache.maven.plugins</groupId>
             <artifactId>maven-clean-plugin</artifactId>
             <version>3.1.0</version> <!-- 改成 3.1.0 -->
          </plugin>
       </plugins>
    </build>

</project>

```

---
tags: JAVA
categories: JAVA

---
