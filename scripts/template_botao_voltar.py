"""
Template do botão de voltar para ser incluído nos relatórios HTML
"""

CSS_BOTAO_VOLTAR = """
        .btn-voltar {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            margin: 20px 0;
        }

        .btn-voltar:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .btn-voltar::before {
            content: '← ';
        }

        .back-button-container {
            text-align: center;
            padding: 20px 40px 0;
        }
"""

HTML_BOTAO_VOLTAR = """
    <div class="back-button-container">
        <a href="../index.html" class="btn-voltar">Voltar para Central de Relatórios</a>
    </div>
"""
