@echo off
chcp 65001 >nul
cls

echo.
echo ============================================================
echo  GERADOR DE RELATORIOS AGHUSE
echo ============================================================
echo.
echo Este script vai gerar:
echo   1. Relatorios MD (diario, semanal, geral)
echo   2. Relatorios HTML visuais
echo.
pause

cls
echo.
echo ============================================================
echo  PASSO 1/2: Gerando relatorios MD...
echo ============================================================
echo.

cd /d "%~dp0"
python scripts\processar_relatorio.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao gerar relatorios MD!
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Relatorios MD gerados!
echo.

echo ============================================================
echo  PASSO 2/2: Gerando relatorios HTML...
echo ============================================================
echo.

python scripts\gerar_relatorio_visual.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao gerar relatorios HTML!
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  CONCLUIDO COM SUCESSO!
echo ============================================================
echo.
echo Relatorios gerados:
echo   - MD:   relatorios\
echo   - HTML: relatorios_html\
echo.
pause
