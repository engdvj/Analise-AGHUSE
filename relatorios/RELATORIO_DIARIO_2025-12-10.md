# Relatório AGHUSE - 10/12/2025

## Status do Dia

**Conexão: 99.24%** - BOM

**Problemas:**
- 16 horários com perda de conexão
- 132 horários com lentidão

## Desempenho por Horário

| Horário | AGHUSE (ms) | Rede Externa (ms) | Status |
|---------|-------------|-------------------|--------|
| 00h | 50.6 (48-77) | 49.2 (49-50) | Regular |
| 01h | 48.4 (48-49) | 49.3 (49-51) | Regular [AG:1pkt] |
| 02h | 48.4 (48-49) | 49.2 (49-50) | Bom |
| 03h | 48.7 (48-51) | 49.1 (49-50) | Regular [AG:1pkt] |
| 04h | 48.4 (48-49) | 49.0 (49-49) | Bom |
| 05h | 48.8 (48-51) | 49.0 (49-49) | Bom |
| 06h | 60.2 (51-71) | 44.8 (40-50) | Regular [AG:1pkt] |
| 07h | 56.3 (56-57) | 47.5 (40-55) | Regular [AG:1pkt] |
| 08h | 56.9 (56-60) | 52.2 (50-56) | Regular [AG:1pkt] |
| 09h | 56.8 (56-60) | 54.8 (53-57) | Regular [AG:1pkt, EX:1pkt] |
| 10h | 57.2 (56-59) | 52.3 (41-70) | Regular [AG:2pkt] |

**Gráfico Comparativo de Latência:**

```
AGHUSE vs Rede Externa
00h │AG: ██████████████████████████████ 50.6ms
     │EX: █████████████████████████████ 49.2ms
01h │AG: █████████████████████████████ 48.4ms
     │EX: ██████████████████████████████ 49.3ms
02h │AG: █████████████████████████████ 48.4ms
     │EX: ██████████████████████████████ 49.2ms
03h │AG: █████████████████████████████ 48.7ms
     │EX: ██████████████████████████████ 49.1ms
04h │AG: █████████████████████████████ 48.4ms
     │EX: ██████████████████████████████ 49.0ms
05h │AG: █████████████████████████████ 48.8ms
     │EX: ██████████████████████████████ 49.0ms
06h │AG: ██████████████████████████████ 60.2ms
     │EX: ██████████████████████ 44.8ms
07h │AG: ██████████████████████████████ 56.3ms
     │EX: █████████████████████████ 47.5ms
08h │AG: ██████████████████████████████ 56.9ms
     │EX: ███████████████████████████ 52.2ms
09h │AG: ██████████████████████████████ 56.8ms
     │EX: ████████████████████████████ 54.8ms
10h │AG: ██████████████████████████████ 57.2ms
     │EX: ███████████████████████████ 52.3ms
```

## Análise Técnica

**Tempo de resposta:** Típico 49.0ms | 95% dos casos abaixo de 62.0ms

**Estabilidade:** Excelente (variação 1.24ms)

**Comparativo de destinos:**
- AGHUSE: 52.9ms
- Rede interna: 52.8ms
- Internet: 49.7ms

## Detalhes de Problemas

**Perda de Pacotes:** 16 ocorrências
- 00:24:00, 01:34:00, 03:04:01, 03:24:01, 03:49:01, 06:44:00, 07:19:00, 09:19:00 e mais 8

## Resumo

**Conexão**: 99.24% - Boa

**Resumo por Horário**: 3/11 bom | 8/11 regular

