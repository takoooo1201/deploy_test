@echo off
echo 正在啟動部署測試專案...
echo.

echo 檢查 Docker 是否運行中...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤：Docker 未安裝或未運行！
    echo 請確保 Docker Desktop 已安裝並運行。
    pause
    exit /b 1
)

echo Docker 已就緒！
echo.

echo 正在構建並啟動所有服務...
docker-compose up --build

echo.
echo 服務已停止。
pause
