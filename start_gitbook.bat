@echo off
chcp 65001

REM 設定 GitBook 根目錄
set "GITBOOK_DIR=E:\Project\developer_project\Gitbook\Gitbook_PJ\20240818_gitbook(local)"

REM 切換到 GitBook 根目錄
cd /d "%GITBOOK_DIR%" || (
    echo 無法切換到 GitBook 目錄
    pause
    exit /b 1
)

REM 檢查是否安裝了 GitBook CLI
where gitbook >nul 2>nul
if %errorlevel% neq 0 (
    echo GitBook CLI 尚未安裝，正在安裝...
    call npm install -g gitbook-cli
    if %errorlevel% neq 0 (
        echo 安裝 GitBook CLI 失敗
        pause
        exit /b 1
    )
)

REM 確保所有依賴項都已安裝
echo 確保所有依賴項都已安裝...
call gitbook install
if %errorlevel% neq 0 (
    echo GitBook 依賴安裝失敗
    pause
    exit /b 1
)

REM 建置 GitBook 專案
echo 建置 GitBook 專案...
call gitbook build
if %errorlevel% neq 0 (
    echo GitBook 建置失敗
    pause
    exit /b 1
)

REM 嘗試啟動 GitBook 伺服器
echo 正在嘗試啟動 GitBook 伺服器...
set max_attempts=3
set attempt=1

:retry_start
start "GitBook Server" /B cmd /C "gitbook serve && pause"
timeout /t 10 >nul

REM 檢查 Live Reload 服務器
netstat -ano | find "35729" >nul
if %errorlevel% neq 0 (
    echo Live Reload 服務器未啟動
    goto check_fail
)

REM 檢查主 HTTP 服務器
netstat -ano | find "4000" >nul
if %errorlevel% neq 0 (
    echo 主 HTTP 服務器未啟動
    goto check_fail
)

echo GitBook 伺服器已成功啟動！
echo Live Reload 服務器運行在端口 35729
echo 主 HTTP 服務器運行在端口 4000
echo 請在瀏覽器中訪問 http://localhost:4000
echo 按任意鍵結束此腳本（伺服器將在背景繼續運行）
pause
exit /b 0

:check_fail
if %attempt% lss %max_attempts% (
    echo 第 %attempt% 次嘗試失敗，正在重試...
    set /a attempt+=1
    goto retry_start
) else (
    echo GitBook 伺服器啟動失敗，請手動檢查問題
    pause
    exit /b 1
)