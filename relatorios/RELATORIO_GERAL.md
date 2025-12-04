# Relatório Geral - Monitoramento AGHUSE
**Período**: 03/12/2025 a 04/12/2025 (2 dias)

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 265 |
| Média de Testes por Dia | 132 |
| Testes sem Perda | 224 |
| Testes com Perda | 41 |
| Total de Pacotes Enviados | 5300 |
| Total de Pacotes Perdidos | 51 |
| **Disponibilidade** | **99.04%** |

## Análise de Latência por Faixa Horária

> **Nota**: Esta análise consolida todos os testes realizados em cada faixa horária
> ao longo do período completo (03/12/2025 a 04/12/2025, 2 dias).
> Cada linha representa a média de todos os testes naquela hora em todos os dias.

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
| 20h | 52.4 (52-54) | Regular |
| 21h | 11.0 (11-11) | Bom |
| 22h | 7.4 (7-9) | Ótimo [2 perda(s)] |
| 23h | 7.8 (7-8) | Ótimo |

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
20h │████████████████████████████████ 52.4ms
21h │██████ 11.0ms
22h │████ 7.4ms
23h │████ 7.8ms
```

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | Latência Média |
|------|--------|-----------------------|------------------|-----------------|----------------|
| 03/12/2025 | 22 | 20 / 2 | 2 | 99.55% | 7.8ms |
| 04/12/2025 | 243 | 204 / 39 | 49 | 98.99% | 26.1ms |

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 09:00 - 09:59 | 5 | 12.2% |
| 08:00 - 08:59 | 4 | 9.8% |
| 10:00 - 10:59 | 4 | 9.8% |
| 12:00 - 12:59 | 4 | 9.8% |
| 13:00 - 13:59 | 4 | 9.8% |
| 11:00 - 11:59 | 3 | 7.3% |
| 15:00 - 15:59 | 3 | 7.3% |
| 18:00 - 18:59 | 3 | 7.3% |
| 22:00 - 22:59 | 2 | 4.9% |
| 14:00 - 14:59 | 2 | 4.9% |
| 17:00 - 17:59 | 2 | 4.9% |
| 03:00 - 03:59 | 1 | 2.4% |
| 05:00 - 05:59 | 1 | 2.4% |
| 06:00 - 06:59 | 1 | 2.4% |
| 07:00 - 07:59 | 1 | 2.4% |
| 16:00 - 16:59 | 1 | 2.4% |

**Padrão Identificado**: Concentração de problemas entre 08:00 e 18:59

### Distribuição de Latência Elevada por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 15:00 - 15:59 | 12 |
| 16:00 - 16:59 | 12 |
| 17:00 - 17:59 | 12 |
| 18:00 - 18:59 | 12 |
| 19:00 - 19:59 | 12 |
| 11:00 - 11:59 | 8 |
| 14:00 - 14:59 | 8 |
| 10:00 - 10:59 | 6 |
| 20:00 - 20:59 | 5 |
| 13:00 - 13:59 | 1 |

## Registro de Incidentes

Total de 41 teste(s) com perda de pacotes:

| Data | Horário | Latência (ms) | Perda (%) | Min/Max (ms) |
|------|---------|---------------|-----------|-------------|
| 03/12 | 22:20:49 | 7 | 5 | 7/14 |
| 03/12 | 22:35:49 | 7 | 5 | 7/8 |
| 04/12 | 03:05:50 | 8 | 5 | 7/22 |
| 04/12 | 05:45:49 | 8 | 5 | 7/13 |
| 04/12 | 06:30:49 | 9 | 5 | 8/18 |
| 04/12 | 07:05:49 | 7 | 5 | 7/11 |
| 04/12 | 08:00:49 | 8 | 5 | 7/13 |
| 04/12 | 08:10:49 | 8 | 5 | 7/15 |
| 04/12 | 08:15:49 | 9 | 5 | 7/20 |
| 04/12 | 08:35:49 | 11 | 5 | 7/16 |
| 04/12 | 09:00:49 | 10 | 15 | 7/33 |
| 04/12 | 09:05:49 | 10 | 5 | 7/22 |
| 04/12 | 09:40:49 | 13 | 5 | 7/38 |
| 04/12 | 09:45:49 | 11 | 10 | 7/30 |
| 04/12 | 09:55:49 | 9 | 5 | 7/16 |
| 04/12 | 10:00:49 | 10 | 5 | 7/31 |
| 04/12 | 10:05:49 | 12 | 5 | 7/26 |
| 04/12 | 10:10:49 | 8 | 15 | 7/15 |
| 04/12 | 10:45:49 | 58 | 5 | 55/80 |
| 04/12 | 11:05:49 | 58 | 10 | 55/67 |
| 04/12 | 11:30:49 | 57 | 5 | 55/65 |
| 04/12 | 11:55:50 | 9 | 10 | 7/24 |
| 04/12 | 12:00:50 | 9 | 5 | 7/16 |
| 04/12 | 12:05:50 | 11 | 5 | 7/32 |
| 04/12 | 12:15:49 | 11 | 5 | 7/33 |
| 04/12 | 12:20:50 | 10 | 5 | 7/28 |
| 04/12 | 13:39:00 | 15 | 5 | 8/31 |
| 04/12 | 13:49:00 | 9 | 10 | 7/17 |
| 04/12 | 13:54:00 | 8 | 5 | 7/16 |
| 04/12 | 13:59:00 | 10 | 5 | 7/33 |

*Exibindo 30 de 41 incidentes. Consulte relatórios diários para informações completas.*

## Análise e Conclusão

**Conexão**: 99.04% - Boa- Acompanhar tendências

**Qualidade por Faixa Horária no Período Completo**: 10/24 ótimo | 5/24 bom | 7/24 regular | 2/24 ruim

---
*Relatório gerado automaticamente a partir de 265 testes realizados em 2 dias*
