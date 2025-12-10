"""
Script para adicionar seção de Critérios e Metodologia nos relatórios HTML
Este script modifica o template HTML para incluir uma aba/seção explicando todos os critérios
"""

def gerar_secao_criterios_html():
    """Gera HTML da seção de Critérios e Metodologia"""
    return '''
        <!-- Aba 5: Critérios e Metodologia -->
        <div class="tab-content" id="criterios">
            <div class="criteria-section">
                <h2 style="color: #2c3e50; margin-bottom: 20px;">Critérios e Metodologia de Análise</h2>
                <p style="color: #7f8c8d; margin-bottom: 30px;">
                    Esta página explica como cada métrica é calculada e quais critérios são utilizados
                    para classificar a qualidade da conexão.
                </p>

                <!-- Status da Disponibilidade -->
                <div class="analysis-card" style="border-left-color: #27ae60;">
                    <h3>📊 Status da Disponibilidade</h3>
                    <p>A disponibilidade mede o percentual de pacotes entregues com sucesso:</p>
                    <div class="criteria-table">
                        <div class="criteria-row">
                            <div class="criteria-status status-otimo">Ótimo</div>
                            <div class="criteria-value">≥ 99.9%</div>
                            <div class="criteria-desc">Conexão extremamente estável</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-bom">Bom</div>
                            <div class="criteria-value">99.0% - 99.9%</div>
                            <div class="criteria-desc">Conexão estável com raras interrupções</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-regular">Regular</div>
                            <div class="criteria-value">95.0% - 99.0%</div>
                            <div class="criteria-desc">Conexão com perdas ocasionais</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-ruim">Ruim</div>
                            <div class="criteria-value">< 95.0%</div>
                            <div class="criteria-desc">Conexão instável, requer atenção</div>
                        </div>
                    </div>
                </div>

                <!-- Classificação de Latência -->
                <div class="analysis-card" style="border-left-color: #3498db;">
                    <h3>⚡ Classificação de Latência</h3>
                    <p>Latência é o tempo de resposta da conexão (quanto menor, melhor):</p>
                    <div class="criteria-table">
                        <div class="criteria-row">
                            <div class="criteria-status status-otimo">Excelente</div>
                            <div class="criteria-value">≤ 15ms</div>
                            <div class="criteria-desc">Baseline ideal - Resposta instantânea</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-bom">Boa</div>
                            <div class="criteria-value">16-30ms</div>
                            <div class="criteria-desc">Ótima para uso geral</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-regular">Regular</div>
                            <div class="criteria-value">31-50ms</div>
                            <div class="criteria-desc">Aceitável, pode haver lentidão leve</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status status-ruim">Ruim</div>
                            <div class="criteria-value">> 50ms</div>
                            <div class="criteria-desc">Lentidão perceptível, requer análise</div>
                        </div>
                    </div>
                </div>

                <!-- Score de Qualidade -->
                <div class="analysis-card" style="border-left-color: #9b59b6;">
                    <h3>🎯 Score de Qualidade (0-10)</h3>
                    <p>Score composto que avalia latência e perda de pacotes simultaneamente:</p>
                    <div style="margin: 15px 0;">
                        <strong>Composição:</strong>
                        <ul style="margin-left: 20px; margin-top: 8px;">
                            <li><strong>60%</strong> - Componente de Latência (0-6 pontos)</li>
                            <li><strong>40%</strong> - Componente de Perda (0-4 pontos)</li>
                        </ul>
                    </div>
                    <div class="criteria-table">
                        <div class="criteria-row">
                            <div class="criteria-status" style="background: #27ae60; color: white;">Excelente</div>
                            <div class="criteria-value">8.5 - 10.0</div>
                            <div class="criteria-desc">Qualidade superior</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status" style="background: #3498db; color: white;">Muito Bom</div>
                            <div class="criteria-value">7.0 - 8.4</div>
                            <div class="criteria-desc">Qualidade alta</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status" style="background: #f39c12; color: white;">Bom</div>
                            <div class="criteria-value">5.5 - 6.9</div>
                            <div class="criteria-desc">Qualidade satisfatória</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status" style="background: #e67e22; color: white;">Regular</div>
                            <div class="criteria-value">4.0 - 5.4</div>
                            <div class="criteria-desc">Qualidade abaixo do ideal</div>
                        </div>
                        <div class="criteria-row">
                            <div class="criteria-status" style="background: #e74c3c; color: white;">Ruim</div>
                            <div class="criteria-value">< 4.0</div>
                            <div class="criteria-desc">Qualidade inadequada</div>
                        </div>
                    </div>
                </div>

                <!-- Horários de Pico -->
                <div class="analysis-card" style="border-left-color: #e74c3c;">
                    <h3>📈 Horários de Pico</h3>
                    <p>Períodos identificados automaticamente quando a latência está significativamente acima da média:</p>
                    <div style="margin: 15px 0;">
                        <strong>Critérios de Detecção:</strong>
                        <ul style="margin-left: 20px; margin-top: 8px;">
                            <li><strong>Threshold:</strong> Latência ≥ 10% acima da média geral</li>
                            <li><strong>Duração mínima:</strong> 3 horas consecutivas</li>
                            <li><strong>Classificação:</strong> Pico Matinal (8h-12h), Pico Vespertino (14h-18h), Pico Noturno (20h-6h)</li>
                        </ul>
                    </div>
                    <div class="criteria-note">
                        💡 <strong>Exemplo:</strong> Se a média geral é 50ms, horários com 55ms+ por 3h+ são considerados pico.
                    </div>
                </div>

                <!-- Anomalias -->
                <div class="analysis-card" style="border-left-color: #e67e22;">
                    <h3>⚠️ Detecção de Anomalias</h3>
                    <p>Anomalias são eventos isolados onde a latência está drasticamente fora do padrão esperado:</p>
                    <div style="margin: 15px 0;">
                        <strong>Métodos de Detecção:</strong>
                        <ul style="margin-left: 20px; margin-top: 8px;">
                            <li><strong>Desvio Padrão:</strong> Latência > 2.5σ (desvios padrão) acima da média do horário</li>
                            <li><strong>Percentual:</strong> Latência > 200% do valor esperado para aquele horário</li>
                        </ul>
                    </div>
                    <div style="margin: 15px 0;">
                        <strong>Níveis de Severidade:</strong>
                        <ul style="margin-left: 20px; margin-top: 8px;">
                            <li><strong>Média:</strong> 2.5-3.0σ ou 200-300% do esperado</li>
                            <li><strong>Alta:</strong> > 3.0σ ou > 300% do esperado</li>
                        </ul>
                    </div>
                    <div class="criteria-note">
                        💡 <strong>Diferença:</strong> Picos são períodos prolongados; anomalias são eventos pontuais extremos.
                    </div>
                </div>

                <!-- Metodologia de Coleta -->
                <div class="analysis-card" style="border-left-color: #95a5a6;">
                    <h3>🔬 Metodologia de Coleta de Dados</h3>
                    <div style="margin: 15px 0;">
                        <ul style="margin-left: 20px;">
                            <li><strong>Frequência:</strong> Testes executados a cada 5 minutos (288 testes/dia)</li>
                            <li><strong>Protocolo:</strong> ICMP Echo Request (ping)</li>
                            <li><strong>Pacotes por teste:</strong> 20 pacotes</li>
                            <li><strong>Destino:</strong> aghuse.saude.ba.gov.br</li>
                            <li><strong>Métricas coletadas:</strong> Latência mínima, média, máxima e perda de pacotes</li>
                        </ul>
                    </div>
                </div>

                <!-- Fórmulas de Cálculo -->
                <div class="analysis-card" style="border-left-color: #34495e;">
                    <h3>📐 Fórmulas de Cálculo</h3>
                    <div style="margin: 15px 0;">
                        <strong>Disponibilidade:</strong>
                        <div class="formula">
                            Disponibilidade = [(Total Pacotes - Pacotes Perdidos) / Total Pacotes] × 100%
                        </div>

                        <strong>Score de Qualidade:</strong>
                        <div class="formula">
                            Score = (Score_Latência × 0.6) + (Score_Perda × 0.4)
                        </div>
                        <ul style="margin-left: 20px; margin-top: 8px; font-size: 13px; color: #7f8c8d;">
                            <li>Score_Latência: 6.0 para ≤15ms, decai linearmente até 0</li>
                            <li>Score_Perda: 4.0 para 0%, decai linearmente até 0</li>
                        </ul>

                        <strong>Regressão Linear (Tendência):</strong>
                        <div class="formula">
                            y = ax + b, onde y = latência prevista, x = dias, a = inclinação (slope), b = intercept
                        </div>
                        <ul style="margin-left: 20px; margin-top: 8px; font-size: 13px; color: #7f8c8d;">
                            <li>R² (coeficiente de determinação) indica confiabilidade: > 0.5 = confiável</li>
                            <li>Slope positivo = tendência de alta; negativo = queda; ~0 = estável</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
'''

def gerar_css_criterios():
    """Gera CSS adicional para a seção de critérios"""
    return '''
        .criteria-section {
            max-width: 900px;
            margin: 0 auto;
        }

        .criteria-table {
            margin-top: 15px;
        }

        .criteria-row {
            display: grid;
            grid-template-columns: 120px 150px 1fr;
            gap: 15px;
            align-items: center;
            padding: 12px;
            background: white;
            border-radius: 4px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }

        .criteria-row:hover {
            background: #f8f9fa;
            transform: translateX(5px);
        }

        .criteria-status {
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 13px;
            text-align: center;
        }

        .criteria-value {
            font-weight: 600;
            color: #2c3e50;
            font-size: 14px;
        }

        .criteria-desc {
            color: #7f8c8d;
            font-size: 13px;
        }

        .criteria-note {
            background: #fff3cd;
            border-left: 4px solid #f39c12;
            padding: 12px 15px;
            margin-top: 15px;
            border-radius: 4px;
            font-size: 14px;
            color: #856404;
        }

        .formula {
            background: #ecf0f1;
            padding: 10px 15px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin: 10px 0;
            border-left: 3px solid #3498db;
        }

        @media (max-width: 768px) {
            .criteria-row {
                grid-template-columns: 1fr;
                gap: 8px;
            }

            .criteria-status {
                width: fit-content;
            }
        }
'''

if __name__ == '__main__':
    print("Seção de Critérios gerada!")
    print("\nPara usar, adicione ao HTML:")
    print("1. Adicione o CSS no <style>")
    print("2. Adicione a aba 'Critérios' no menu de tabs")
    print("3. Adicione o HTML da seção no conteúdo")
