# Sistema de Monitoramento de Conectividade AGHUSE

Sistema automatizado para coleta, análise e geração de relatórios de conectividade com o servidor AGHUSE (10.252.17.132).

## Descrição

Este sistema realiza testes periódicos de conectividade e gera relatórios técnicos detalhados com métricas de disponibilidade e latência.

## Estrutura do Projeto

```
script/
├── aghuse.bat                    # Script de coleta automática (executar a cada 5 minutos)
├── gerar_relatorios.bat         # Script para gerar relatórios (executar quando necessário)
├── processar_relatorio.py       # Processador de dados e gerador de relatórios
├── arquivos/                    # Dados brutos dos testes de conectividade (.txt)
└── relatorios/                  # Relatórios gerados (.md)
    ├── RELATORIO_DIARIO_*.md    # Relatórios diários individuais
    ├── RELATORIO_SEMANAL.md     # Relatório semanal consolidado
    └── RELATORIO_GERAL.md       # Relatório geral de todo o período
```

## Funcionalidades

### Coleta de Dados (aghuse.bat)

O script executa os seguintes testes automaticamente:

1. **Configuração de Rede**: `ipconfig /all`
2. **Ping AGHUSE**: 20 pacotes para aghuse.saude.ba.gov.br
3. **Traceroute**: Rastreamento de rota para o servidor
4. **Ping Interno**: 20 pacotes para IP 10.252.17.132
5. **Ping Externo**: 20 pacotes para Google DNS (8.8.8.8)

Cada execução gera um arquivo timestamped:
```
CONECTIVIDADE_AGHUSE_YYYY-MM-DD_HH-MM-SS.txt
```

### Geração de Relatórios (processar_relatorio.py)

O sistema processa todos os arquivos de teste e gera três tipos de relatórios:

#### 1. Relatórios Diários
- Sumário executivo com métricas principais
- Análise de latência (mín/média/máx)
- Registro de incidentes com perda de pacotes
- Identificação de testes com latência elevada
- Detalhamento horário completo
- Análise técnica e conclusões

#### 2. Relatório Semanal
- Sumário executivo do período
- Análise comparativa por dia
- Distribuição de problemas por horário
- Registro consolidado de incidentes
- Análise de tendências

#### 3. Relatório Geral
- Dashboard de métricas do período completo
- Análise de horários críticos com identificação de padrões
- Registro detalhado de todos os incidentes
- Conclusões e recomendações técnicas

## Métricas Calculadas

### Disponibilidade
Calculada com base na perda real de pacotes:
```
Disponibilidade = (Pacotes Enviados - Pacotes Perdidos) / Pacotes Enviados × 100
```

**Classificação:**
- ≥ 99.9% - Excelente (operando conforme SLA)
- ≥ 99.0% - Boa (dentro dos parâmetros)
- ≥ 95.0% - Aceitável (monitoramento necessário)
- < 95.0% - Crítica (ação corretiva imediata)

### Latência
Medida em milissegundos (ms) para cada destino:
- **AGHUSE**: Servidor principal de monitoramento
- **IP Interno**: Validação de conectividade local
- **Google DNS**: Referência de conectividade externa

**Classificação:**
- < 10ms - Excelente
- < 20ms - Adequada
- < 50ms - Aceitável
- ≥ 50ms - Requer investigação

## Como Usar

### 1. Coleta Automática de Dados

Configure o `aghuse.bat` no Agendador de Tarefas do Windows:

**Configuração Recomendada:**
- **Intervalo**: A cada 5 minutos
- **Executar como**: Usuário com permissões de rede
- **Ação**: Executar `aghuse.bat`

**Configuração Manual:**
1. Abra o Agendador de Tarefas do Windows
2. Criar Tarefa Básica
3. Nome: "Monitoramento AGHUSE"
4. Disparador: Diariamente, repetir a cada 5 minutos
5. Ação: Iniciar programa `aghuse.bat`
6. Finalizar

### 2. Gerar Relatórios

**Opção 1 - Executar o .bat (Recomendado):**
```batch
# Duplo clique no arquivo:
gerar_relatorios.bat
```

**Opção 2 - Linha de comando:**
```bash
python processar_relatorio.py
```

### 3. Visualizar Relatórios

Os relatórios são gerados em formato Markdown (.md) na pasta `relatorios/`.

Podem ser visualizados em:
- Editores de código (VSCode, Notepad++, etc.)
- Visualizadores Markdown
- Convertidos para PDF/HTML se necessário

## Requisitos do Sistema

- **Sistema Operacional**: Windows
- **Python**: Versão 3.6 ou superior
- **Bibliotecas Python**: Apenas bibliotecas padrão (sem dependências externas)
- **Rede**: Conectividade com o servidor AGHUSE

## Interpretação dos Resultados

### Exemplo de Métrica
```
Total de Testes: 148
Pacotes Enviados: 2960 (148 × 20)
Pacotes Perdidos: 23
Disponibilidade: 99.22%
```

### Análise de Horários Críticos

O sistema identifica automaticamente padrões de problemas:
```
Faixa Horária: 09:00 - 09:59
Ocorrências: 5
Porcentagem: 27.8%

Padrão Identificado: Concentração entre 08:00 e 10:59
```

### Registro de Incidentes

Cada incidente é registrado com:
- Data e horário exato
- Latência observada
- Percentual de perda
- Valores mín/máx de latência

## Manutenção

### Limpeza de Dados Antigos

Recomenda-se manter apenas os últimos 30 dias de dados brutos:
```batch
# Mover arquivos antigos para backup
# Na pasta arquivos/, mover arquivos com mais de 30 dias
```

### Backup de Relatórios

Salvar relatórios importantes periodicamente:
```
relatorios_backup/
├── 2025-12/
│   ├── RELATORIO_SEMANAL_semana1.md
│   └── RELATORIO_GERAL_dezembro.md
```

## Troubleshooting

### Erro: "Python não encontrado"
**Solução**: Instale o Python 3.x e adicione ao PATH do sistema

### Erro: "Pasta arquivos/ não encontrada"
**Solução**: Execute o `aghuse.bat` pelo menos uma vez para gerar dados

### Erro: "Encoding UTF-8"
**Solução**: O sistema já está configurado para UTF-8, verifique a versão do Python

### Relatórios vazios
**Solução**: Verifique se há arquivos .txt na pasta `arquivos/`

## Logs e Debug

O script Python exibe informações durante a execução:
```
Processando arquivos de teste...
Total de arquivos processados: 148
Agrupando dados por dia...
Total de dias com dados: 2

Gerando relatórios diários...
  [OK] RELATORIO_DIARIO_2025-12-03.md
  [OK] RELATORIO_DIARIO_2025-12-04.md
...
```

## Suporte Técnico

Para problemas ou dúvidas:
1. Verifique os logs de execução
2. Valide os arquivos de entrada em `arquivos/`
3. Confirme a instalação do Python
4. Revise as permissões de escrita na pasta `relatorios/`

## Versionamento

**Versão**: 1.0
**Data**: Dezembro 2025
**Autor**: Sistema de Monitoramento AGHUSE

## Licença

Uso interno - Sistema de Monitoramento de Conectividade AGHUSE
