# Relatório AGHUSE - 08/12/2025

## Status do Dia

**Conexão: 99.20%** - BOM

**Problemas:**
- 30 horários com perda de conexão
- 226 horários com lentidão

## Desempenho por Horário

| Horário | Latência (ms) | Status |
|---------|---------------|--------|
| 00h | 50.3 (49-64) | Regular |
| 01h | 49.2 (49-50) | Bom |
| 02h | 49.1 (49-50) | Bom |
| 03h | 49.0 (49-49) | Bom |
| 04h | 49.0 (49-49) | Bom |
| 05h | 49.1 (49-50) | Bom |
| 06h | 49.4 (49-51) | Regular [1 perda(s)] |
| 07h | 49.4 (49-51) | Regular [3 perda(s)] |
| 08h | 50.2 (49-54) | Regular [2 perda(s)] |
| 09h | 53.7 (49-68) | Ruim [6 perda(s)] |
| 10h | 51.9 (49-66) | Ruim [4 perda(s)] |
| 11h | 54.3 (49-68) | Regular [2 perda(s)] |
| 12h | 53.7 (49-68) | Regular [1 perda(s)] |
| 13h | 52.2 (49-55) | Ruim [5 perda(s)] |
| 14h | 51.1 (49-57) | Ruim [4 perda(s)] |
| 15h | 51.8 (50-54) | Regular [1 perda(s)] |
| 16h | 51.1 (46-54) | Regular |
| 17h | 51.6 (51-53) | Regular |
| 18h | 52.1 (51-57) | Regular [1 perda(s)] |

**Gráfico de Latência:**

```
00h │█████████████████████████████████████ 50.3ms
01h │████████████████████████████████████ 49.2ms
02h │████████████████████████████████████ 49.1ms
03h │████████████████████████████████████ 49.0ms
04h │████████████████████████████████████ 49.0ms
05h │████████████████████████████████████ 49.1ms
06h │████████████████████████████████████ 49.4ms
07h │████████████████████████████████████ 49.4ms
08h │████████████████████████████████████ 50.2ms
09h │███████████████████████████████████████ 53.7ms
10h │██████████████████████████████████████ 51.9ms
11h │████████████████████████████████████████ 54.3ms
12h │███████████████████████████████████████ 53.7ms
13h │██████████████████████████████████████ 52.2ms
14h │█████████████████████████████████████ 51.1ms
15h │██████████████████████████████████████ 51.8ms
16h │█████████████████████████████████████ 51.1ms
17h │█████████████████████████████████████ 51.6ms
18h │██████████████████████████████████████ 52.1ms
```

## Análise Técnica

**Tempo de resposta:** Típico 50.0ms | 95% dos casos abaixo de 56.8ms

**Estabilidade:** Excelente (variação 1.65ms)

**Comparativo de destinos:**
- AGHUSE: 50.9ms
- Rede interna: 50.7ms
- Internet: 37.1ms

Problema identificado: Rede interna com lentidão

## Detalhes de Problemas

**Perda de Pacotes:** 30 ocorrências
- 06:49:01, 07:19:01, 07:24:01, 07:44:01, 08:09:01, 08:59:01, 09:09:01, 09:14:01 e mais 22

## Resumo

**Conexão**: 99.20% - Boa

**Resumo por Horário**: 5/19 bom | 10/19 regular | 4/19 ruim

