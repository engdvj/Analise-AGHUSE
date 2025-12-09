# Relatório Semanal - Monitoramento de Conectividade AGHUSE
**Período**: 03/12/2025 a 08/12/2025

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 1396 |
| Testes sem Perda | 1269 |
| Testes com Perda | 127 |
| Total de Pacotes Enviados | 27920 |
| Total de Pacotes Perdidos | 154 |
| **Disponibilidade** | **99.45%** |
| Latência Média | 46.6ms |
| Latência Mín/Máx | 7/184ms |

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | Latência Média |
|------|--------|-----------------------|------------------|-----------------|----------------|
| 03/12/2025 | 22 | 20 / 2 | 2 | 99.55% | 7.8ms |
| 04/12/2025 | 286 | 246 / 40 | 50 | 99.13% | 29.8ms |
| 05/12/2025 | 288 | 256 / 32 | 39 | 99.32% | 50.7ms |
| 06/12/2025 | 288 | 276 / 12 | 13 | 99.77% | 51.7ms |
| 07/12/2025 | 286 | 275 / 11 | 14 | 99.76% | 53.9ms |
| 08/12/2025 | 226 | 196 / 30 | 36 | 99.20% | 50.9ms |

## Análise de Latência por Faixa Horária

> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária
> ao longo do período completo (03/12/2025 a 08/12/2025).
> Cada linha representa a média de todos os testes naquela hora em todos os dias.

| Horário | Latência (ms) | Status |
|---------|---------------|--------|
| 00h | 41.7 (7-64) | Regular [1 perda(s)] |
| 01h | 42.4 (7-56) | Regular [2 perda(s)] |
| 02h | 42.9 (7-57) | Regular [3 perda(s)] |
| 03h | 42.5 (7-56) | Regular [1 perda(s)] |
| 04h | 41.9 (7-55) | Regular [1 perda(s)] |
| 05h | 42.4 (7-56) | Regular [1 perda(s)] |
| 06h | 43.8 (7-70) | Regular [4 perda(s)] |
| 07h | 42.6 (7-55) | Regular [7 perda(s)] |
| 08h | 43.2 (8-58) | Regular [10 perda(s)] |
| 09h | 44.0 (8-68) | Regular [16 perda(s)] |
| 10h | 49.0 (8-66) | Regular [14 perda(s)] |
| 11h | 50.4 (8-68) | Ruim [10 perda(s)] |
| 12h | 43.6 (8-68) | Regular [13 perda(s)] |
| 13h | 44.7 (8-55) | Regular [12 perda(s)] |
| 14h | 50.1 (8-65) | Ruim [6 perda(s)] |
| 15h | 53.2 (48-73) | Ruim [7 perda(s)] |
| 16h | 53.5 (46-68) | Regular [2 perda(s)] |
| 17h | 52.8 (48-71) | Ruim [3 perda(s)] |
| 18h | 52.7 (46-58) | Ruim [6 perda(s)] |
| 19h | 53.7 (48-59) | Ruim [3 perda(s)] |
| 20h | 53.4 (49-59) | Regular [2 perda(s)] |
| 21h | 52.7 (11-62) | Regular |
| 22h | 44.8 (7-58) | Regular [3 perda(s)] |
| 23h | 41.2 (7-55) | Bom |

**Gráfico de Latência:**

```
00h │███████████████████████████████ 41.7ms
01h │███████████████████████████████ 42.4ms
02h │███████████████████████████████ 42.9ms
03h │███████████████████████████████ 42.5ms
04h │███████████████████████████████ 41.9ms
05h │███████████████████████████████ 42.4ms
06h │████████████████████████████████ 43.8ms
07h │███████████████████████████████ 42.6ms
08h │████████████████████████████████ 43.2ms
09h │████████████████████████████████ 44.0ms
10h │████████████████████████████████████ 49.0ms
11h │█████████████████████████████████████ 50.4ms
12h │████████████████████████████████ 43.6ms
13h │█████████████████████████████████ 44.7ms
14h │█████████████████████████████████████ 50.1ms
15h │███████████████████████████████████████ 53.2ms
16h │███████████████████████████████████████ 53.5ms
17h │███████████████████████████████████████ 52.8ms
18h │███████████████████████████████████████ 52.7ms
19h │████████████████████████████████████████ 53.7ms
20h │███████████████████████████████████████ 53.4ms
21h │███████████████████████████████████████ 52.7ms
22h │█████████████████████████████████ 44.8ms
23h │██████████████████████████████ 41.2ms
```

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 09:00 - 09:59 | 16 | 12.6% |
| 10:00 - 10:59 | 14 | 11.0% |
| 12:00 - 12:59 | 13 | 10.2% |
| 13:00 - 13:59 | 12 | 9.4% |
| 08:00 - 08:59 | 10 | 7.9% |
| 11:00 - 11:59 | 10 | 7.9% |
| 07:00 - 07:59 | 7 | 5.5% |
| 15:00 - 15:59 | 7 | 5.5% |
| 14:00 - 14:59 | 6 | 4.7% |
| 18:00 - 18:59 | 6 | 4.7% |
| 06:00 - 06:59 | 4 | 3.1% |
| 22:00 - 22:59 | 3 | 2.4% |
| 17:00 - 17:59 | 3 | 2.4% |
| 02:00 - 02:59 | 3 | 2.4% |
| 19:00 - 19:59 | 3 | 2.4% |
| 16:00 - 16:59 | 2 | 1.6% |
| 01:00 - 01:59 | 2 | 1.6% |
| 20:00 - 20:59 | 2 | 1.6% |
| 03:00 - 03:59 | 1 | 0.8% |
| 05:00 - 05:59 | 1 | 0.8% |
| 00:00 - 00:59 | 1 | 0.8% |
| 04:00 - 04:59 | 1 | 0.8% |

### Distribuição de Latência Elevada (>20ms) por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 15:00 - 15:59 | 60 |
| 16:00 - 16:59 | 60 |
| 17:00 - 17:59 | 60 |
| 18:00 - 18:59 | 58 |
| 11:00 - 11:59 | 56 |
| 14:00 - 14:59 | 56 |
| 10:00 - 10:59 | 54 |
| 13:00 - 13:59 | 49 |
| 19:00 - 19:59 | 48 |
| 20:00 - 20:59 | 48 |

## Registro de Incidentes

Total de 127 teste(s) com perda de pacotes:

| Data | Horário | Latência (ms) | Perda (%) |
|------|---------|---------------|----------|
| 03/12 | 22:20:49 | 7 | 5 |
| 03/12 | 22:35:49 | 7 | 5 |
| 04/12 | 03:05:50 | 8 | 5 |
| 04/12 | 05:45:49 | 8 | 5 |
| 04/12 | 06:30:49 | 9 | 5 |
| 04/12 | 07:05:49 | 7 | 5 |
| 04/12 | 08:00:49 | 8 | 5 |
| 04/12 | 08:10:49 | 8 | 5 |
| 04/12 | 08:15:49 | 9 | 5 |
| 04/12 | 08:35:49 | 11 | 5 |
| 04/12 | 09:00:49 | 10 | 15 |
| 04/12 | 09:05:49 | 10 | 5 |
| 04/12 | 09:40:49 | 13 | 5 |
| 04/12 | 09:45:49 | 11 | 10 |
| 04/12 | 09:55:49 | 9 | 5 |
| 04/12 | 10:00:49 | 10 | 5 |
| 04/12 | 10:05:49 | 12 | 5 |
| 04/12 | 10:10:49 | 8 | 15 |
| 04/12 | 10:45:49 | 58 | 5 |
| 04/12 | 11:05:49 | 58 | 10 |

*Exibindo 20 de 127 incidentes. Consulte relatórios diários para detalhes completos.*

## Análise de Tendências

**Regressão Linear**: +5.91ms/dia (R² = 0.302, Tendência: alta)

**Previsão 7 dias**: 102.3ms ⚠️ *Baixa confiabilidade (R² < 0.5)*

## Horários de Pico

- **Pico Vespertino**: 15h-21h (latência média 53.1ms, +6.3ms acima da média)

## Score de Qualidade por Horário

| Horário | Score | Classificação | Componente Latência | Componente Perda |
|---------|-------|---------------|---------------------|------------------|
| 00h | 4.6 | Regular | 1.4 | 3.2 |
| 01h | 3.5 | Ruim | 1.4 | 2.1 |
| 02h | 2.3 | Ruim | 1.3 | 1.0 |
| 03h | 4.5 | Regular | 1.3 | 3.2 |
| 04h | 4.6 | Regular | 1.4 | 3.2 |
| 05h | 4.5 | Regular | 1.3 | 3.2 |
| 06h | 2.0 | Ruim | 1.2 | 0.8 |
| 07h | 1.6 | Ruim | 1.3 | 0.3 |
| 08h | 1.2 | Ruim | 1.2 | 0 |
| 09h | 1.1 | Ruim | 1.1 | 0 |
| 10h | 0.9 | Ruim | 0.9 | 0 |
| 11h | 0.8 | Ruim | 0.8 | 0 |
| 12h | 1.2 | Ruim | 1.2 | 0 |
| 13h | 1.0 | Ruim | 1.0 | 0 |
| 14h | 1.3 | Ruim | 0.8 | 0.5 |
| 15h | 1.1 | Ruim | 0.7 | 0.3 |
| 16h | 2.8 | Ruim | 0.7 | 2.1 |
| 17h | 1.7 | Ruim | 0.7 | 1.0 |
| 18h | 1.2 | Ruim | 0.7 | 0.5 |
| 19h | 1.6 | Ruim | 0.7 | 0.9 |
| 20h | 2.3 | Ruim | 0.7 | 1.6 |
| 21h | 4.7 | Regular | 0.7 | 4.0 |
| 22h | 2.0 | Ruim | 1.0 | 1.0 |
| 23h | 5.5 | Bom | 1.5 | 4.0 |

## Análise por Dia da Semana

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | 50.9ms | +9.2% | 09h (68.0ms) | 226 |
| Terça | - | - | - | 0 |
| Quarta | 7.8ms | -83.3% | 21h (11.0ms) | 22 |
| Quinta | 29.8ms | -36.1% | 15h (73.0ms) | 286 |
| Sexta | 50.7ms | +8.7% | 16h (68.0ms) | 288 |
| Sábado | 51.7ms | +10.8% | 06h (70.0ms) | 288 |
| Domingo | 53.9ms | +15.6% | 21h (62.0ms) | 286 |

## Alertas de Anomalias

Total de 4 anomalia(s) detectada(s):

⚠️ **04/12 às 15:04**: Latência 67ms (2.5σ acima do esperado 53.2ms) [Severidade: media]
⚠️ **04/12 às 15:14**: Latência 73ms (3.7σ acima do esperado 53.2ms) [Severidade: alta]
⚠️ **04/12 às 17:44**: Latência 71ms (3.6σ acima do esperado 52.8ms) [Severidade: alta]
⚠️ **04/12 às 17:59**: Latência 66ms (2.6σ acima do esperado 52.8ms) [Severidade: media]

## Distribuição de Latência

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 177 | 12.7% |
| 20-40ms | 2 | 0.1% |
| 40-60ms | 1165 | 83.5% |
| 60-80ms | 52 | 3.7% |
| 80+ms | 0 | 0.0% |

## Análise e Conclusão

**Conexão**: 99.45% - Boa

**Qualidade por Faixa Horária no Período**: 1/24 bom | 17/24 regular | 6/24 ruim

