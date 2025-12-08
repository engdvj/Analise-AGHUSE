# Relatório AGHUSE - 08/12/2025

## Status do Dia

**Conexão: 99.29%** - BOM

**Problemas:**
- 15 horários com perda de conexão
- 127 horários com lentidão

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
| 10h | 51.0 (49-55) | Ruim [3 perda(s)] |

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
08h │█████████████████████████████████████ 50.2ms
09h │████████████████████████████████████████ 53.7ms
10h │██████████████████████████████████████ 51.0ms
```

## Análise Técnica

**Tempo de resposta:** Típico 49.0ms | 95% dos casos abaixo de 53.7ms

**Estabilidade:** Excelente (variação 1.09ms)

**Comparativo de destinos:**
- AGHUSE: 49.9ms
- Rede interna: 49.6ms
- Internet: 34.5ms

Problema identificado: Rede interna com lentidão

## Detalhes de Problemas

**Perda de Pacotes:** 15 ocorrências
- 06:49:01, 07:19:01, 07:24:01, 07:44:01, 08:09:01, 08:59:01, 09:09:01, 09:14:01 e mais 7

## Resumo

**Conexão**: 99.29% - Boa

**Resumo por Horário**: 5/11 bom | 4/11 regular | 2/11 ruim

