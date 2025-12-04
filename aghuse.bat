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

rem Remove espaço à esquerda da hora (quando de 0 a 9)
if "%HORA:~0,1%"==" " set "HORA=0%HORA:~1,1%"

set "TIMESTAMP=%ANO%-%MES%-%DIA%_%HORA%-%MIN%-%SEG%"

set "ARQ=%CD%\CONECTIVIDADE_AGHUSE_%TIMESTAMP%.txt"

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
rem 1 - CABEÇALHO PADRONIZADO
rem ============================================
> "%ARQ%" (
    echo =========================================================
    echo TESTE DE CONECTIVIDADE - AGHUSE
    echo ID_TESTE   : %TIMESTAMP%
    echo DATA_TESTE : %DIA%/%MES%/%ANO%
    echo HORA_TESTE : %HORA%:%MIN%:%SEG%
    echo =========================================================
    echo.
    echo [1/7] INFORMACOES GERAIS
    echo DATA_TESTE : %DIA%/%MES%/%ANO%
    echo HORA_TESTE : %HORA%:%MIN%:%SEG%
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 2 - IPCONFIG /ALL
rem ============================================
echo 2/7 ..... Coletando configuracao de rede (ipconfig /all)

>> "%ARQ%" (
    echo [2/7] IPCONFIG /ALL
    echo ---------------------------------------------------------
)
ipconfig /all >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 3 - PING aghuse.saude.ba.gov.br
rem ============================================
echo 3/7 ..... Testando ping para aghuse.saude.ba.gov.br

>> "%ARQ%" (
    echo [3/7] PING aghuse.saude.ba.gov.br -n 20
    echo ---------------------------------------------------------
)
ping aghuse.saude.ba.gov.br -n 20 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 4 - TRACERT aghuse.saude.ba.gov.br
rem ============================================
echo 4/7 ..... Executando tracert para aghuse.saude.ba.gov.br

>> "%ARQ%" (
    echo [4/7] TRACERT -d aghuse.saude.ba.gov.br
    echo ---------------------------------------------------------
)
tracert -d aghuse.saude.ba.gov.br >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 5 - PING interno (10.252.17.132)
rem ============================================
echo 5/7 ..... Testando ping interno (10.252.17.132)

>> "%ARQ%" (
    echo [5/7] PING 10.252.17.132 -n 20
    echo ---------------------------------------------------------
)
ping 10.252.17.132 -n 20 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 6 - PING externo (8.8.8.8)
rem ============================================
echo 6/7 ..... Testando ping externo (8.8.8.8)

>> "%ARQ%" (
    echo [6/7] PING 8.8.8.8 -n 20
    echo ---------------------------------------------------------
)
ping 8.8.8.8 -n 20 >> "%ARQ%"
>> "%ARQ%" (
    echo.
    echo ---------------------------------------------------------
    echo.
)

rem ============================================
rem 7 - FINALIZACAO
rem ============================================
echo 7/7 ..... Finalizando

>> "%ARQ%" (
    echo [7/7] FIM DO TESTE DE CONECTIVIDADE
    echo =========================================================
    echo.
)

echo.
echo TESTE DE CONECTIVIDADE FINALIZADO.
echo Arquivo gerado em:
echo   %ARQ%
echo.

endlocal
