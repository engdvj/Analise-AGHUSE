# Relatório Geral - Monitoramento AGHUSE
**Período**: 03/12/2025 a 04/12/2025 (2 dias)

## Sumário Executivo

| Métrica | Valor |
|---------|-------|
| Total de Testes Executados | 182 |
| Média de Testes por Dia | 91 |
| Testes sem Perda | 156 |
| Testes com Perda | 26 |
| Total de Pacotes Enviados | 3640 |
| Total de Pacotes Perdidos | 33 |
| **Disponibilidade** | **99.09%** |

## Métricas de Latência

| Destino | Latência Média (ms) | Mínima (ms) | Máxima (ms) |
|---------|---------------------|-------------|-------------|
| AGHUSE (10.252.17.132) | 11.8 | 7 | 184 |
| IP Interno (10.252.17.132) | 11.7 | - | - |
| Google DNS (8.8.8.8) | 45.3 | - | - |

## Análise por Dia

| Data | Testes | Sem Perda / Com Perda | Pacotes Perdidos | Disponibilidade | Latência Média |
|------|--------|-----------------------|------------------|-----------------|----------------|
| 03/12/2025 | 22 | 20 / 2 | 2 | 99.55% | 7.8ms |
| 04/12/2025 | 160 | 136 / 24 | 31 | 99.03% | 12.4ms |

## Análise de Horários Críticos

### Distribuição de Perda de Pacotes por Horário

| Faixa Horária | Ocorrências | Porcentagem do Total |
|---------------|-------------|---------------------|
| 09:00 - 09:59 | 5 | 19.2% |
| 08:00 - 08:59 | 4 | 15.4% |
| 10:00 - 10:59 | 4 | 15.4% |
| 12:00 - 12:59 | 4 | 15.4% |
| 11:00 - 11:59 | 3 | 11.5% |
| 22:00 - 22:59 | 2 | 7.7% |
| 03:00 - 03:59 | 1 | 3.8% |
| 05:00 - 05:59 | 1 | 3.8% |
| 06:00 - 06:59 | 1 | 3.8% |
| 07:00 - 07:59 | 1 | 3.8% |

**Padrão Identificado**: Concentração de problemas entre 08:00 e 12:59

### Distribuição de Latência Elevada por Horário

| Faixa Horária | Ocorrências |
|---------------|-------------|
| 11:00 - 11:59 | 8 |
| 10:00 - 10:59 | 6 |

## Registro de Incidentes

Total de 26 teste(s) com perda de pacotes:

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

## Análise e Conclusão

**Disponibilidade**: 99.09% - Boa. Sistema operando dentro dos parâmetros.
- Acompanhar tendências

**Latência**: Média de 11.8ms - Performance adequada.

**Obs**: 14 testes (7.7%) apresentaram latência superior a 20ms.

---
*Relatório gerado automaticamente a partir de 182 testes realizados em 2 dias*
