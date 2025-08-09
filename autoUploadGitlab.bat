chcp 65001
REM 抓出系統時間
for /f "tokens=1-6 delims=-" %%a in ('PowerShell -Command "& {Get-Date -format "yyyy-MM-dd-HH-mm-ss"}"') do (
    SET year=%%a
    SET month=%%b
    SET day=%%c
)

REM 定義參數
SET JoplinBKPath="C:\Users\MarkHSU\Documents\Obsidian Vault"
SET EXCLUDEPath=E:\Project\note_tool\joplin\uncopy.txt
SET GitBookPath=E:\Project\developer_project\Gitbook\Gitbook_PJ\20240818_gitbook(local)
SET GitBookURL=https://root:mark850409@markweb.idv.tw:10443/gitbooknpmproject/gitbooklocalhost.git
SET commit_message="feat: %year%-%month%-%day%_更新了筆記!!!"

:main
REM call gitpush function(gitbook)
call :copynote %JoplinBKPath% %EXCLUDEPath% %GitBookPath% 

:copynote
set sourcepath=%1
set excludepath=%2
set targetpath=%3
echo %sourcepath%
echo %excludepath%
echo %targetpath%
xcopy /S /Q /Y /F %sourcepath% /EXCLUDE:%excludepath% "%targetpath%"
cd /d "%targetpath%"

REM 產生SUMMARY目錄
python gitbook-auto-summary-simple.py -o .

REM 產生tags、categories
python add_front_matter.py "%targetpath%"


call :gitpush %commit_message% %GitBookURL% 

:gitpush
REM 推送專案到GIT
set commit_message=%1
set GitBookURL=%2
echo %commit_message%
echo %GitBookURL%
git init 
git pull %GitBookURL%
git add .
git status
REM 提交更改
git commit -m %commit_message%
REM 推送更改到GitLab仓库
git push --set-upstream %GitBookURL% master

pause