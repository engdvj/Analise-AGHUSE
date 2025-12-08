# Relatório AGHUSE - 04/12/2025

## Status do Dia

**Conexão: 99.13%** - BOM

**Problemas:**
- 40 horários com perda de conexão
- 131 horários com lentidão

## Desempenho por Horário

| Horário | Latência (ms) | Status |
|---------|---------------|--------|
| 00h | 7.4 (7-9) | Ótimo |
| 01h | 7.2 (7-8) | Ótimo |
| 02h | 7.4 (7-9) | Ótimo |
| 03h | 7.2 (7-8) | Ótimo [1 perda(s)] |
| 04h | 7.1 (7-8) | Ótimo |
| 05h | 7.3 (7-8) | Ótimo [1 perda(s)] |
| 06h | 8.1 (7-11) | Ótimo [1 perda(s)] |
| 07h | 8.1 (7-9) | Ótimo [1 perda(s)] |
| 08h | 8.8 (8-11) | Bom [4 perda(s)] |
| 09h | 10.5 (8-14) | Bom [5 perda(s)] |
| 10h | 31.4 (8-59) | Regular [4 perda(s)] |
| 11h | 41.7 (8-62) | Regular [3 perda(s)] |
| 12h | 9.5 (8-11) | Bom [4 perda(s)] |
| 13h | 11.8 (8-29) | Bom [4 perda(s)] |
| 14h | 42.9 (8-65) | Regular [2 perda(s)] |
| 15h | 62.5 (56-73) | Ruim [3 perda(s)] |
| 16h | 64.2 (61-68) | Regular [1 perda(s)] |
| 17h | 60.7 (50-71) | Regular [2 perda(s)] |
| 18h | 52.8 (46-58) | Ruim [3 perda(s)] |
| 19h | 52.7 (51-56) | Regular |
| 20h | 52.2 (51-54) | Regular |
| 21h | 51.8 (51-55) | Regular |
| 22h | 50.2 (48-52) | Regular [1 perda(s)] |
| 23h | 48.7 (48-50) | Bom |

**Gráfico de Latência:**

```
00h │████ 7.4ms
01h │████ 7.2ms
02h │████ 7.4ms
03h │████ 7.2ms
04h │████ 7.1ms
05h │████ 7.3ms
06h │█████ 8.1ms
07h │█████ 8.1ms
08h │█████ 8.8ms
09h │██████ 10.5ms
10h │███████████████████ 31.4ms
11h │█████████████████████████ 41.7ms
12h │█████ 9.5ms
13h │███████ 11.8ms
14h │██████████████████████████ 42.9ms
15h │██████████████████████████████████████ 62.5ms
16h │████████████████████████████████████████ 64.2ms
17h │█████████████████████████████████████ 60.7ms
18h │████████████████████████████████ 52.8ms
19h │████████████████████████████████ 52.7ms
20h │████████████████████████████████ 52.2ms
21h │████████████████████████████████ 51.8ms
22h │███████████████████████████████ 50.2ms
23h │██████████████████████████████ 48.7ms
```

## Análise Técnica

**Tempo de resposta:** Típico 11.0ms | 95% dos casos abaixo de 64.0ms

**Estabilidade:** Ruim (variação 2.05ms)

**Comparativo de destinos:**
- AGHUSE: 29.8ms
- Rede interna: 29.6ms
- Internet: 45.3ms

## Detalhes de Problemas

**Perda de Pacotes:** 40 ocorrências
- 03:05:50, 05:45:49, 06:30:49, 07:05:49, 08:00:49, 08:10:49, 08:15:49, 08:35:49 e mais 32

## Resumo

**Conexão**: 99.13% - Boa

**Resumo por Horário**: 8/24 ótimo | 5/24 bom | 9/24 regular | 2/24 ruim

