@echo off
chcp 1252 >nul
setlocal ENABLEEXTENSIONS

rem ============================================
rem Script para Gerar Relatórios de Conectividade AGHUSE
rem ============================================

cls
echo ===============================================
echo  GERADOR DE RELATORIOS - AGHUSE
echo ===============================================
echo.
echo Processando arquivos e gerando relatorios...
echo.

rem Executar o script Python
python processar_relatorio.py

rem Verificar se houve erro
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Falha ao gerar relatorios.
    echo Verifique se o Python esta instalado e se os arquivos estao corretos.
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  RELATORIOS GERADOS COM SUCESSO!
echo ===============================================
echo.
echo Os relatorios foram salvos na pasta 'relatorios\'
echo.
echo Tipos de relatorios gerados:
echo  - Relatorios Diarios (por data)
echo  - Relatorio Semanal (consolidado)
echo  - Relatorio Geral (periodo completo)
echo.
pause

endlocal
