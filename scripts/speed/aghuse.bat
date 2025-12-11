@echo off
chcp 1252 >nul
setlocal ENABLEEXTENSIONS

rem ============================================
rem 0 - GERA TIMESTAMP / DATA / HORA (FORMATO FIXO)
rem ============================================
rem Supondo formato de data do sistema: DD/MM/AAAA
set "DATA_SIS=%DATE%"
set "HORA_SIS=%TIME%"

set "ANO=%DATE:~6,4%"
set "MES=%DATE:~3,2%"
set "DIA=%DATE:~0,2%"

set "HORA=%TIME:~0,2%"
set "MIN=%TIME:~3,2%"
set "SEG=%TIME:~6,2%"

rem Remove espaco à esquerda da hora (quando de 0 a 9)
if "%HORA:~0,1%"==" " set "HORA=0%HORA:~1,1%"

set "TIMESTAMP=%ANO%-%MES%-%DIA%_%HORA%-%MIN%-%SEG%"

rem ============================================
rem 0.1 - BASE: PASTA DO PRÓPRIO .BAT
rem ============================================
rem %~dp0 = pasta onde este .bat está
set "BASE_DIR=%~dp0"

rem Pasta do dia: <pasta_do_bat>\arquivos\AAAA-MM-DD
set "PASTA_DIA=%BASE_DIR%arquivos\%ANO%-%MES%-%DIA%"
if not exist "%PASTA_DIA%" mkdir "%PASTA_DIA%"

set "ARQ=%PASTA_DIA%\CONECTIVIDADE_AGHUSE_%TIMESTAMP%.txt"

cls
echo ===============================================
echo  TESTE DE CONECTIVIDADE - AGHUSE
echo  Inicio : %TIMESTAMP%
echo  Saida  : %ARQ%
echo ===============================================
echo.
echo AGUARDE, EXECUTANDO TESTES...
echo.

rem ============================================
rem 1 - IDENTIFICACAO DO SISTEMA
rem ============================================
echo 1/10 .... Coletando identificacao do sistema

> "%ARQ%" (
    echo =========================================================
    echo TESTE DE CONECTIVIDADE - AGHUSE
    echo ID_TESTE   : %TIMESTAMP%
    echo DATA_TESTE : %DIA%/%MES%/%ANO%
    echo HORA_TESTE : %HORA%:%MIN%:%SEG%
    echo =========================================================
    echo.
    echo [1/10] IDENTIFICACAO DO SISTEMA
    echo ---------------------------------------------------------
)
hostname >> "%ARQ%"
whoami >> "%ARQ%"
>> "%ARQ%" (
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 2 - IPCONFIG /ALL
rem ============================================
echo 2/10 .... Coletando configuracao de rede (ipconfig /all)

>> "%ARQ%" (
    echo [2/10] CONFIGURACAO DE REDE - IPCONFIG /ALL
    echo ---------------------------------------------------------
)
ipconfig /all >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 3 - EXTRAIR E TESTAR GATEWAY PADRAO
rem ============================================
echo 3/10 .... Testando conectividade com gateway padrao

>> "%ARQ%" (
    echo [3/10] PING GATEWAY PADRAO -n 10
    echo ---------------------------------------------------------
)

rem Extrai o gateway padrão do ipconfig
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"Gateway"') do (
    set "GATEWAY=%%a"
    goto :gateway_found
)
:gateway_found
set "GATEWAY=%GATEWAY: =%"

if not "%GATEWAY%"=="" (
    echo GATEWAY: %GATEWAY% >> "%ARQ%"
    ping %GATEWAY% -n 10 >> "%ARQ%"
) else (
    echo Gateway nao detectado >> "%ARQ%"
)

>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 4 - PING interno AGHUSE (10.252.17.132)
rem ============================================
echo 4/10 .... Testando ping interno AGHUSE (10.252.17.132)

>> "%ARQ%" (
    echo [4/10] PING INTERNO AGHUSE - 10.252.17.132 -n 10
    echo ---------------------------------------------------------
)
ping 10.252.17.132 -n 10 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 5 - PING externo Google DNS (8.8.8.8)
rem ============================================
echo 5/10 .... Testando ping externo Google DNS (8.8.8.8)

>> "%ARQ%" (
    echo [5/10] PING EXTERNO GOOGLE DNS - 8.8.8.8 -n 10
    echo ---------------------------------------------------------
)
ping 8.8.8.8 -n 10 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 6 - NSLOOKUP aghuse.saude.ba.gov.br
rem ============================================
echo 6/10 .... Testando resolucao DNS do AGHUSE

>> "%ARQ%" (
    echo [6/10] NSLOOKUP aghuse.saude.ba.gov.br
    echo ---------------------------------------------------------
)
nslookup aghuse.saude.ba.gov.br >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 7 - PING aghuse.saude.ba.gov.br
rem ============================================
echo 7/10 .... Testando ping para aghuse.saude.ba.gov.br

>> "%ARQ%" (
    echo [7/10] PING aghuse.saude.ba.gov.br -n 20
    echo ---------------------------------------------------------
)
ping aghuse.saude.ba.gov.br -n 20 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 8 - TRACERT aghuse.saude.ba.gov.br
rem ============================================
echo 8/10 .... Executando tracert para aghuse.saude.ba.gov.br

>> "%ARQ%" (
    echo [8/10] TRACERT -d aghuse.saude.ba.gov.br
    echo ---------------------------------------------------------
)
tracert -d aghuse.saude.ba.gov.br >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 9 - FINALIZACAO DOS TESTES DE REDE
rem ============================================
echo.
echo TESTES DE CONECTIVIDADE FINALIZADOS.
echo Arquivo gerado em:
echo   %ARQ%
echo.

rem ============================================
rem 10 - CHAMA SCRIPT PYTHON (TESTES DE VELOCIDADE)
rem ============================================
echo.
echo ===============================================
echo  INICIANDO TESTES DE VELOCIDADE
echo  Script: openspeedtest_log.py
echo ===============================================
echo.

cd /d "%BASE_DIR%"
python openspeedtest_log.py "%ARQ%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] Erro ao executar testes de velocidade.
    echo.
)

echo.
echo ===============================================
echo  TODOS OS TESTES FINALIZADOS
echo  Arquivo: %ARQ%
echo ===============================================
echo.

pause
endlocal
