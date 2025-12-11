# Relatório Semanal - Monitoramento de Conectividade AGHUSE
**Período**: 30/11/2025 a 06/12/2025

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 884 |
| Testes sem Perda | 798 |
| Testes com Perda | 86 |
| Total de Pacotes Enviados | 17680 |
| Total de Pacotes Perdidos | 104 |
| **Disponibilidade** | **99.41%** |
| Latência Média | 43.2ms |
| Latência Mín/Máx | 7/184ms |

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | AGHUSE (ms) | Rede Externa (ms) |
|------|--------|-----------------------|------------------|-----------------|-------------|-------------------|
| 30/11/2025 | - | - | - | - | - | - |
| 01/12/2025 | - | - | - | - | - | - |
| 02/12/2025 | - | - | - | - | - | - |
| 03/12/2025 | 22 | 20 / 2 | 2 | 99.55% | 7.8ms | 45.0ms |
| 04/12/2025 | 286 | 246 / 40 | 50 | 99.13% | 29.8ms | 45.3ms |
| 05/12/2025 | 288 | 256 / 32 | 39 | 99.32% | 50.7ms | 45.7ms |
| 06/12/2025 | 288 | 276 / 12 | 13 | 99.77% | 51.7ms | 38.8ms |

## Análise de Latência por Faixa Horária

> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária
> ao longo do período completo (30/11/2025 a 06/12/2025).
> Cada linha representa a média de todos os testes naquela hora em todos os dias.

| Horário | AGHUSE (ms) | Rede Externa (ms) | Status |
|---------|-------------|-------------------|--------|
| 00h | 34.2 (7-49) | 45.1 (45-47) | Regular [AG:1pkt] |
| 01h | 36.0 (7-56) | 45.0 (45-45) | Regular [AG:2pkt] |
| 02h | 37.2 (7-62) | 45.0 (45-45) | Regular [AG:1pkt] |
| 03h | 36.2 (7-52) | 45.0 (45-45) | Bom |
| 04h | 35.5 (7-52) | 45.1 (45-50) | Bom |
| 05h | 36.0 (7-54) | 45.0 (45-45) | Regular [AG:3pkt] |
| 06h | 38.9 (7-65) | 45.2 (45-47) | Regular [AG:1pkt, EX:1pkt] |
| 07h | 36.4 (7-57) | 45.3 (42-48) | Regular [AG:2pkt, EX:1pkt] |
| 08h | 37.1 (7-54) | 44.7 (42-51) | Regular [AG:9pkt, EX:4pkt] |
| 09h | 37.6 (7-57) | 44.9 (42-51) | Regular [AG:6pkt, EX:3pkt] |
| 10h | 45.8 (9-60) | 43.2 (36-54) | Regular [AG:8pkt, EX:3pkt] |
| 11h | 47.4 (9-60) | 42.7 (36-47) | Regular [AG:14pkt] |
| 12h | 36.2 (7-52) | 43.1 (36-47) | Regular [AG:6pkt, EX:1pkt] |
| 13h | 38.2 (7-53) | 43.2 (36-48) | Regular [AG:9pkt, EX:6pkt] |
| 14h | 48.4 (8-64) | 43.3 (36-64) | Regular [AG:4pkt, EX:1pkt] |
| 15h | 54.9 (49-66) | 42.7 (36-52) | Ruim [AG:5pkt, EX:5pkt] |
| 16h | 55.8 (49-68) | 44.2 (35-64) | Ruim [AG:3pkt, EX:5pkt] |
| 17h | 54.4 (48-66) | 42.8 (35-49) | Ruim [AG:4pkt, EX:1pkt] |
| 18h | 52.1 (49-59) | 40.7 (30-54) | Regular [AG:2pkt] |
| 19h | 52.1 (48-56) | 40.4 (30-46) | Regular [EX:1pkt] |
| 20h | 52.2 (49-56) | 40.6 (31-47) | Regular |
| 21h | 51.1 (9-58) | 41.1 (31-63) | Regular [AG:1pkt, EX:19pkt] |
| 22h | 41.7 (7-55) | 41.4 (31-46) | Regular [AG:3pkt] |
| 23h | 38.9 (7-56) | 41.5 (30-47) | Regular [AG:2pkt, EX:2pkt] |

**Gráfico Comparativo de Latência:**

```
AGHUSE vs Rede Externa
00h │AG: ██████████████████████ 34.2ms
     │EX: ██████████████████████████████ 45.1ms
01h │AG: ███████████████████████ 36.0ms
     │EX: ██████████████████████████████ 45.0ms
02h │AG: ████████████████████████ 37.2ms
     │EX: ██████████████████████████████ 45.0ms
03h │AG: ████████████████████████ 36.2ms
     │EX: ██████████████████████████████ 45.0ms
04h │AG: ███████████████████████ 35.5ms
     │EX: ██████████████████████████████ 45.1ms
05h │AG: ████████████████████████ 36.0ms
     │EX: ██████████████████████████████ 45.0ms
06h │AG: █████████████████████████ 38.9ms
     │EX: ██████████████████████████████ 45.2ms
07h │AG: ████████████████████████ 36.4ms
     │EX: ██████████████████████████████ 45.3ms
08h │AG: ████████████████████████ 37.1ms
     │EX: ██████████████████████████████ 44.7ms
09h │AG: █████████████████████████ 37.6ms
     │EX: ██████████████████████████████ 44.9ms
10h │AG: ██████████████████████████████ 45.8ms
     │EX: ████████████████████████████ 43.2ms
11h │AG: ██████████████████████████████ 47.4ms
     │EX: ███████████████████████████ 42.7ms
12h │AG: █████████████████████████ 36.2ms
     │EX: ██████████████████████████████ 43.1ms
13h │AG: ██████████████████████████ 38.2ms
     │EX: ██████████████████████████████ 43.2ms
14h │AG: ██████████████████████████████ 48.4ms
     │EX: ██████████████████████████ 43.3ms
15h │AG: ██████████████████████████████ 54.9ms
     │EX: ███████████████████████ 42.7ms
16h │AG: ██████████████████████████████ 55.8ms
     │EX: ███████████████████████ 44.2ms
17h │AG: ██████████████████████████████ 54.4ms
     │EX: ███████████████████████ 42.8ms
18h │AG: ██████████████████████████████ 52.1ms
     │EX: ███████████████████████ 40.7ms
19h │AG: ██████████████████████████████ 52.1ms
     │EX: ███████████████████████ 40.4ms
20h │AG: ██████████████████████████████ 52.2ms
     │EX: ███████████████████████ 40.6ms
21h │AG: ██████████████████████████████ 51.1ms
     │EX: ████████████████████████ 41.1ms
22h │AG: ██████████████████████████████ 41.7ms
     │EX: █████████████████████████████ 41.4ms
23h │AG: ████████████████████████████ 38.9ms
     │EX: ██████████████████████████████ 41.5ms
```

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 12:00 - 12:59 | 11 | 12.8% |
| 09:00 - 09:59 | 9 | 10.5% |
| 08:00 - 08:59 | 8 | 9.3% |
| 10:00 - 10:59 | 8 | 9.3% |
| 11:00 - 11:59 | 7 | 8.1% |
| 13:00 - 13:59 | 6 | 7.0% |
| 15:00 - 15:59 | 5 | 5.8% |
| 07:00 - 07:59 | 4 | 4.7% |
| 18:00 - 18:59 | 4 | 4.7% |
| 22:00 - 22:59 | 3 | 3.5% |
| 17:00 - 17:59 | 3 | 3.5% |
| 02:00 - 02:59 | 3 | 3.5% |
| 06:00 - 06:59 | 2 | 2.3% |
| 14:00 - 14:59 | 2 | 2.3% |
| 16:00 - 16:59 | 2 | 2.3% |
| 01:00 - 01:59 | 2 | 2.3% |
| 19:00 - 19:59 | 2 | 2.3% |
| 03:00 - 03:59 | 1 | 1.2% |
| 05:00 - 05:59 | 1 | 1.2% |
| 00:00 - 00:59 | 1 | 1.2% |
| 04:00 - 04:59 | 1 | 1.2% |
| 20:00 - 20:59 | 1 | 1.2% |

### Distribuição de Latência Elevada (>20ms) por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 15:00 - 15:59 | 36 |
| 16:00 - 16:59 | 36 |
| 17:00 - 17:59 | 36 |
| 18:00 - 18:59 | 36 |
| 19:00 - 19:59 | 36 |
| 20:00 - 20:59 | 36 |
| 21:00 - 21:59 | 36 |
| 22:00 - 22:59 | 36 |
| 23:00 - 23:59 | 36 |
| 11:00 - 11:59 | 32 |

## Registro de Incidentes

Total de 86 teste(s) com perda de pacotes:

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

*Exibindo 20 de 86 incidentes. Consulte relatórios diários para detalhes completos.*

## Score de Qualidade por Horário

| Horário | Score | Classificação | Componente Latência | Componente Perda |
|---------|-------|---------------|---------------------|------------------|
| 00h | 4.9 | Regular | 2.4 | 2.5 |
| 01h | 3.1 | Ruim | 2.2 | 0.9 |
| 02h | 2.7 | Ruim | 2.0 | 0.7 |
| 03h | 4.6 | Regular | 2.2 | 2.5 |
| 04h | 4.7 | Regular | 2.3 | 2.5 |
| 05h | 4.7 | Regular | 2.2 | 2.5 |
| 06h | 2.8 | Ruim | 1.8 | 0.9 |
| 07h | 2.5 | Ruim | 2.2 | 0.4 |
| 08h | 2.1 | Ruim | 2.1 | 0 |
| 09h | 2.0 | Ruim | 2.0 | 0 |
| 10h | 1.0 | Ruim | 1.0 | 0 |
| 11h | 0.9 | Ruim | 0.9 | 0 |
| 12h | 2.2 | Ruim | 2.2 | 0 |
| 13h | 1.9 | Ruim | 1.9 | 0 |
| 14h | 1.8 | Ruim | 0.9 | 0.9 |
| 15h | 0.8 | Ruim | 0.7 | 0.1 |
| 16h | 1.6 | Ruim | 0.6 | 0.9 |
| 17h | 1.4 | Ruim | 0.7 | 0.7 |
| 18h | 1.2 | Ruim | 0.8 | 0.4 |
| 19h | 1.7 | Ruim | 0.8 | 0.9 |
| 20h | 3.2 | Ruim | 0.8 | 2.5 |
| 21h | 4.8 | Regular | 0.8 | 4.0 |
| 22h | 2.3 | Ruim | 1.4 | 0.8 |
| 23h | 5.8 | Bom | 1.8 | 4.0 |

## Análise por Dia da Semana

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | - | - | - | 0 |
| Terça | - | - | - | 0 |
| Quarta | 7.8ms | -82.0% | 21h (11.0ms) | 22 |
| Quinta | 29.8ms | -31.0% | 15h (73.0ms) | 286 |
| Sexta | 50.7ms | +17.4% | 16h (68.0ms) | 288 |
| Sábado | 51.7ms | +19.6% | 06h (70.0ms) | 288 |
| Domingo | - | - | - | 0 |

### Análise por Dia da Semana - Rede Externa (8.8.8.8)

| Dia | Latência Média | vs. Média Geral | Pior Horário | Testes |
|-----|----------------|-----------------|--------------|--------|
| Segunda | - | - | - | 0 |
| Terça | - | - | - | 0 |
| Quarta | 45.0ms | +3.8% | 21h (45.0ms) | 22 |
| Quinta | 45.3ms | +4.6% | 18h (54.0ms) | 286 |
| Sexta | 45.7ms | +5.5% | 16h (64.0ms) | 288 |
| Sábado | 38.8ms | -10.4% | 14h (64.0ms) | 288 |
| Domingo | - | - | - | 0 |

## Alertas de Anomalias

### Horários de Pico

Períodos com latência significativamente acima da média (>10%):

- **Pico Vespertino**: 14h-21h (latência média 52.6ms, +9.5ms acima da média, 8h consecutivas)

### Análise de Rotas (Tracert)

**Total de rotas detectadas**: 2

**Rota principal:** Rota 1 (Principal) = 10.17.201.254 -> 10.17.250.114 -> ... -> 10.2.222.220 -> 10.252.17.132 (6 saltos); perda 8.6% em 880 testes.
**Alternativas:** 1 rota(s). Mais usada: Rota 2 = 10.17.201.254 -> 10.17.250.114 -> ... -> 10.252.17.132 -> 10.252.17.132 (7 saltos) (mesmos hops iniciais, 1 salto(s) a mais); perda 25.0% em 4 testes.

**Rotas identificadas**:

| Rota | Ocorrências | Com Perda | Sem Perda | Taxa de Perda |
|------|-------------|-----------|-----------|---------------|
| Rota 1 (Principal) - 10.17.201.254 -> 10.17.250.114 -> ... -> 10.2.222.220 -> 10.252.17.132 (6 saltos) | 880 | 76 | 804 | 8.6% |
| Rota 2 - 10.17.201.254 -> 10.17.250.114 -> ... -> 10.252.17.132 -> 10.252.17.132 (7 saltos) | 4 | 1 | 3 | 25.0% |

**Correlação Rota vs Perda de Pacotes**: Rota principal: 8.6% de perda em 880 testes. Alternativas: 25.0% em 4 testes. Mudanças: 3 de 8 (38%) tiveram perda. Rotas alternativas mais instáveis que a principal.

**Mudanças de rota detectadas**: 8 (3 associadas a perda de pacotes)

*O que mudou*:

- 04/12 às 11:25: Rota 2 -> Rota 1 (Principal) (sem perda registrada; mesmos hops iniciais, 1 salto(s) a menos)
- 04/12 às 12:40: Rota 1 (Principal) -> Rota 2 (com perda de pacotes; mesmos hops iniciais, 1 salto(s) a mais)
- 04/12 às 12:45: Rota 2 -> Rota 1 (Principal) (com perda de pacotes; mesmos hops iniciais, 1 salto(s) a menos)
- 04/12 às 18:49: Rota 1 (Principal) -> Rota 2 (sem perda registrada; mesmos hops iniciais, 1 salto(s) a mais)
- 04/12 às 18:54: Rota 2 -> Rota 1 (Principal) (sem perda registrada; mesmos hops iniciais, 1 salto(s) a menos)

### Anomalias de Latência

Total de 45 anomalia(s) detectada(s):

⚠️ **04/12 às 13:44**: Latência 29ms (2.8σ acima do esperado 11.8ms) [Severidade: media]
⚠️ **04/12 às 15:14**: Latência 73ms (3.0σ acima do esperado 55.2ms) [Severidade: media]
⚠️ **04/12 às 17:44**: Latência 71ms (2.9σ acima do esperado 54.7ms) [Severidade: media]
⚠️ **04/12 às 20:04**: Latência 54ms (2.7σ acima do esperado 52.2ms) [Severidade: media]
⚠️ **04/12 às 21:29**: Latência 55ms (3.0σ acima do esperado 51.8ms) [Severidade: media]
⚠️ **05/12 às 04:49**: Latência 51ms (2.7σ acima do esperado 49.3ms) [Severidade: media]
⚠️ **05/12 às 05:24**: Latência 54ms (2.6σ acima do esperado 49.9ms) [Severidade: media]
⚠️ **05/12 às 16:19**: Latência 68ms (3.3σ acima do esperado 51.7ms) [Severidade: alta]
⚠️ **06/12 às 03:39**: Latência 52ms (2.9σ acima do esperado 50.2ms) [Severidade: media]
⚠️ **06/12 às 13:19**: Latência 51ms (2.9σ acima do esperado 49.2ms) [Severidade: media]
⚠️ **06/12 às 18:34**: Latência 57ms (3.0σ acima do esperado 54.4ms) [Severidade: media]
⚠️ **07/12 às 03:19**: Latência 56ms (2.9σ acima do esperado 54.2ms) [Severidade: media]
⚠️ **07/12 às 07:14**: Latência 55ms (3.3σ acima do esperado 54.1ms) [Severidade: alta]
⚠️ **07/12 às 08:39**: Latência 56ms (2.7σ acima do esperado 54.3ms) [Severidade: media]
⚠️ **07/12 às 09:34**: Latência 56ms (2.7σ acima do esperado 54.3ms) [Severidade: media]
⚠️ **07/12 às 12:19**: Latência 60ms (3.1σ acima do esperado 55.2ms) [Severidade: alta]
⚠️ **07/12 às 20:09**: Latência 59ms (3.3σ acima do esperado 58.1ms) [Severidade: alta]
⚠️ **07/12 às 21:49**: Latência 62ms (3.2σ acima do esperado 58.2ms) [Severidade: alta]
⚠️ **08/12 às 00:44**: Latência 64ms (3.3σ acima do esperado 50.3ms) [Severidade: alta]
⚠️ **08/12 às 02:29**: Latência 50ms (3.3σ acima do esperado 49.1ms) [Severidade: alta]
⚠️ **08/12 às 05:44**: Latência 50ms (3.3σ acima do esperado 49.1ms) [Severidade: alta]
⚠️ **08/12 às 09:29**: Latência 68ms (3.0σ acima do esperado 53.7ms) [Severidade: media]
⚠️ **08/12 às 10:59**: Latência 66ms (3.1σ acima do esperado 51.9ms) [Severidade: alta]
⚠️ **08/12 às 14:34**: Latência 57ms (2.7σ acima do esperado 51.1ms) [Severidade: media]
⚠️ **08/12 às 18:49**: Latência 57ms (3.1σ acima do esperado 51.9ms) [Severidade: alta]
⚠️ **08/12 às 19:44**: Latência 70ms (3.0σ acima do esperado 53.6ms) [Severidade: media]
⚠️ **08/12 às 20:04**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **08/12 às 23:39**: Latência 55ms (3.2σ acima do esperado 51.4ms) [Severidade: alta]
⚠️ **09/12 às 00:09**: Latência 56ms (3.3σ acima do esperado 51.4ms) [Severidade: alta]
⚠️ **09/12 às 01:54**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 02:54**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 05:59**: Latência 52ms (3.3σ acima do esperado 51.1ms) [Severidade: alta]
⚠️ **09/12 às 07:34**: Latência 70ms (2.6σ acima do esperado 54.4ms) [Severidade: media]
⚠️ **09/12 às 14:14**: Latência 76ms (3.0σ acima do esperado 67.7ms) [Severidade: media]
⚠️ **09/12 às 15:09**: Latência 79ms (2.7σ acima do esperado 69.2ms) [Severidade: media]
⚠️ **09/12 às 17:54**: Latência 72ms (3.2σ acima do esperado 53.7ms) [Severidade: alta]
⚠️ **09/12 às 21:39**: Latência 58ms (3.0σ acima do esperado 52.8ms) [Severidade: alta]
⚠️ **09/12 às 23:44**: Latência 52ms (2.8σ acima do esperado 49.0ms) [Severidade: media]
⚠️ **10/12 às 03:24**: Latência 51ms (2.7σ acima do esperado 48.8ms) [Severidade: media]
⚠️ **10/12 às 07:39**: Latência 60ms (3.2σ acima do esperado 56.4ms) [Severidade: alta]
⚠️ **10/12 às 09:29**: Latência 67ms (2.9σ acima do esperado 59.0ms) [Severidade: media]
⚠️ **10/12 às 10:49**: Latência 62ms (2.9σ acima do esperado 57.6ms) [Severidade: media]
⚠️ **10/12 às 15:09**: Latência 64ms (3.0σ acima do esperado 55.6ms) [Severidade: media]
⚠️ **10/12 às 23:24**: Latência 55ms (3.1σ acima do esperado 50.4ms) [Severidade: alta]
⚠️ **11/12 às 00:44**: Latência 52ms (2.5σ acima do esperado 49.6ms) [Severidade: media]

## Distribuição de Latência

### AGHUSE (10.252.17.132)

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 177 | 20.0% |
| 20-40ms | 2 | 0.2% |
| 40-60ms | 663 | 75.0% |
| 60-80ms | 42 | 4.8% |
| 80+ms | 0 | 0.0% |

### Rede Externa (8.8.8.8)

| Faixa | Frequência | Percentual |
|-------|-----------|------------|
| 0-20ms | 0 | 0.0% |
| 20-40ms | 161 | 18.2% |
| 40-60ms | 720 | 81.4% |
| 60-80ms | 3 | 0.3% |
| 80+ms | 0 | 0.0% |

## Análise e Conclusão

**Conexão**: 99.41% - Boa

**Qualidade por Faixa Horária no Período**: 2/24 bom | 19/24 regular | 3/24 ruim

