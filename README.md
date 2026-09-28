# Demonstração — Geração e organização do SPED ECF

> Projeto de portfólio de **Victória Pedrosa**. **Demonstração** de geração e organização do SPED ECF — versão com dados fictícios (nomes, CNPJs, e-mails e IDs internos substituídos).

## Problema de negócio
Gerar e validar a ECF de cada empresa exige muitos cliques repetidos.

## Antes x depois
| | Antes | Depois |
|---|---|---|
| Como é feito | Operação manual no programa da ECF. | Robô percorre a planilha de empresas, gera o arquivo e registra o status de validação. |

## Ganho
- ECF em lote com controle de status.

## Tecnologias
PyAutoGUI (RPA por imagem), Python, SQLite, pandas

## Arquivos
- `arquivospedtxt_ecf.py`
- `pegar_posicao.py`
- `requirements.txt`

## Como rodar
1. `pip install -r requirements.txt`
2. Copie `.env.exemplo` para `.env` e preencha os caminhos.
3. Execute o script principal.

> As imagens de referência usadas pelo robô para clicar na tela (PyAutoGUI) não foram incluídas nesta versão.

## Autora
Victória Pedrosa — Product Owner do Time de IA, automação de processos contábeis e fiscais.
