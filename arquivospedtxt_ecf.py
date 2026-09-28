import pyautogui
import pandas as pd
import time
import traceback
import os
from dotenv import load_dotenv
load_dotenv()  # lê o .env local (não vai para o GitHub)

# Pausa de segurança entre cada comando do PyAutoGUI (1 segundo)
pyautogui.PAUSE = 1.0

# =========================================================================
# CONFIGURAÇÃO DE CAMINHOS E PLANILHA
# =========================================================================
caminho_planilha = os.getenv("CAMINHO_PLANILHA")
caminho_saida = os.getenv("CAMINHO_SAIDA")

# Se a planilha de Status JÁ EXISTE, usa ela como fonte (mantém os status anteriores)
# Senão, lê a planilha original
if os.path.exists(caminho_saida):
    print(f"Lendo planilha de STATUS existente: {caminho_saida}")
    df_empresas = pd.read_excel(caminho_saida, sheet_name='PRAZO 1806', header=0)
else:
    print(f"Lendo planilha ORIGINAL: {caminho_planilha}")
    df_empresas = pd.read_excel(caminho_planilha, sheet_name='PRAZO 1806', header=0)

# A coluna de status JA EXISTE na planilha - é a coluna N (indice 13) "VALIDOU?"
coluna_status = df_empresas.columns[13]  # Coluna N - "VALIDOU?"
print(f"Coluna de status sera atualizada em: {coluna_status} (Coluna N)")

# Remove linhas onde a Coluna D (Código - índice 3) esteja vazia
df_empresas = df_empresas.dropna(subset=[df_empresas.columns[3]])

total_empresas = len(df_empresas)
print(f"\n{'='*50}")
print(f"  TOTAL DE EMPRESAS LIDAS: {total_empresas}")
print(f"{'='*50}\n")
time.sleep(3)

def importar_trimestres():
    """Função para importar os 4 trimestres nas abas de P200 a P500"""
    coord_trimestres = [(803, 276), (883, 273), (969, 274), (1056, 277)] 
    
    for coord in coord_trimestres:
        pyautogui.click(coord) # Clica na aba do trimestre
        time.sleep(0.5)
        pyautogui.click(x=1428, y=694) # Botão "Importar" dos trimestres
        time.sleep(1.5) # Aguarda um pouco mais para o popup carregar bem
        pyautogui.press('y') # Pressiona 'Y' de "Yes"
        
        # Pausa de 10 segundos entre um trimestre e outro
        print("Aguardando 10 segundos para o próximo trimestre...")
        time.sleep(10) 

def executar_automacao(codigo_empresa, regime, obrigatoriedade):
    try:
        # =========================================================================
        # TROCA DE EMPRESA NA DOMÍNIO (AGORA NO INÍCIO)
        # =========================================================================
        pyautogui.press('f8')
        time.sleep(2)
        pyautogui.write(codigo_empresa)
        time.sleep(1)
        pyautogui.press('enter') 
        
        # CORREÇÃO: Aumentado o tempo para 2s para o Domínio carregar a busca
        time.sleep(2)
        
        # CLIQUE NO BOTÃO ACESSAR (Coordenadas atualizadas)
        pyautogui.click(x=988, y=980) 
        time.sleep(6) # Tempo para a nova empresa abrir
        
        # =========================================================================
        # PARTE 1: ACESSO, DATAS, CAMINHOS E PARÂMETROS
        # =========================================================================
        pyautogui.click(x=725, y=66) # Clica em Favoritos primeiro
        time.sleep(1)
        
        pyautogui.click(x=774, y=102) # Clica em SPED ECF
        time.sleep(2)
        
        # --- PREENCHIMENTO DAS DATAS INICIAL E FINAL ---
        pyautogui.click(x=752, y=372) # Coordenada Data Inicial
        time.sleep(0.5)
        pyautogui.press('home')
        time.sleep(0.2)
        pyautogui.hotkey('shift', 'end')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        pyautogui.write('01012025') 
        time.sleep(0.5)
        
        pyautogui.click(x=738, y=404) # Coordenada Data Final
        time.sleep(0.5)
        pyautogui.press('home')
        time.sleep(0.2)
        pyautogui.hotkey('shift', 'end')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        pyautogui.write('31122025')
        time.sleep(0.5)
        
        # ===== MELHORIA 1: PREENCHIMENTO DO CAMINHO COM LIMPEZA GARANTIDA =====
        # Clica uma vez para focar no campo
        pyautogui.click(x=837, y=779) 
        time.sleep(0.5)
        
        # Vai até o INÍCIO do texto (Home)
        pyautogui.press('home')
        time.sleep(0.3)
        
        # Seleciona do início até o FINAL (Shift+End)
        pyautogui.hotkey('shift', 'end')
        time.sleep(0.3)
        
        # Apaga o conteúdo selecionado
        pyautogui.press('delete')
        time.sleep(0.3)
        
        # GARANTIA EXTRA: pressiona Backspace várias vezes caso ainda tenha texto
        pyautogui.press('backspace', presses=80, interval=0.01)
        time.sleep(0.3)
        
        # Agora sim digita o caminho limpo
        pyautogui.write(os.getenv("PASTA_TXT_ECF"), interval=0.05)
        time.sleep(0.5)
        
        pyautogui.click(x=1225, y=475) # Botão "Outros Dados..."
        print("Aguardando 10 segundos o carregamento...")
        time.sleep(10)
        
        # ===== MELHORIA 2: VERIFICA ANTES DE MARCAR - CONTAS CONTABEIS =====
        try:
            box1_vazia = pyautogui.locateCenterOnScreen('contas_desmarcada.png', confidence=0.8)
            if box1_vazia:
                pyautogui.click(box1_vazia)
                time.sleep(0.5)
                print("  Marcada: Gerar somente contas contabeis com movimento")
            else:
                print("  Ja estava marcada: Gerar somente contas contabeis com movimento")
        except pyautogui.ImageNotFoundException:
            print("  Ja estava marcada: Gerar somente contas contabeis com movimento")
        except Exception as e:
            print(f"  ERRO ao verificar contas contabeis: {e}")
        
        # ===== MELHORIA 3: VERIFICA ANTES DE MARCAR - CONTAS REFERENCIAIS =====
        try:
            box2_vazia = pyautogui.locateCenterOnScreen('referenciais_desmarcada.png', confidence=0.8)
            if box2_vazia:
                pyautogui.click(box2_vazia)
                time.sleep(0.5)
                print("  Marcada: Gerar somente tabelas e contas referenciais")
            else:
                print("  Ja estava marcada: Gerar somente tabelas e contas referenciais")
        except pyautogui.ImageNotFoundException:
            print("  Ja estava marcada: Gerar somente tabelas e contas referenciais")
        except Exception as e:
            print(f"  ERRO ao verificar contas referenciais: {e}")
        
        pyautogui.click(x=545, y=232) # Aba "Parâmetros de Tributação"
        time.sleep(1)
        
        pyautogui.click(x=837, y=348) # Dropdown de Regime
        time.sleep(0.5)
        if 'CAIXA' in regime:
            pyautogui.click(x=873, y=360) # Clica em Caixa
        else:
            pyautogui.click(x=858, y=388) # Clica em Competência
            
        pyautogui.click(x=907, y=380) # Dropdown Tipo de Escrituração
        time.sleep(0.1)
        if 'OK' in obrigatoriedade or 'PARCIAL' in obrigatoriedade:
            pyautogui.click(x=867, y=396) # Opção C (Obrigada)
        elif 'SM' in obrigatoriedade or 'DESOBRIGADA' in obrigatoriedade:
            pyautogui.click(x=875, y=418) # Opção L (Desobrigada)
            
        pyautogui.click(x=719, y=228) # Aba "Parâmetros Complementares"
        time.sleep(1)
        
        # ===== MELHORIA 4: VERIFICA ANTES DE MARCAR - PJ SUJEITA CSLL =====
        try:
            box_pj_vazia = pyautogui.locateCenterOnScreen('pj_desmarcada.png', confidence=0.9)
            if box_pj_vazia:
                pyautogui.click(x=452, y=291)
                time.sleep(0.5)
                print("  Marcada: PJ Sujeita a Aliquota da CSLL")
            else:
                print("  Ja estava marcada: PJ Sujeita a Aliquota da CSLL")
        except pyautogui.ImageNotFoundException:
            print("  Ja estava marcada: PJ Sujeita a Aliquota da CSLL")
        except Exception as e:
            print(f"  ERRO ao verificar PJ Sujeita CSLL: {e}")
        
        # =========================================================================
        # PARTE 2: ÁRVORE DE REGISTROS, INFORMAÇÕES GERAIS E EXPORTAÇÃO
        # =========================================================================
        pyautogui.click(x=1071, y=229) # Aba "Presumido"
        time.sleep(1)
        
        pyautogui.click(x=562, y=292) # P200
        importar_trimestres()
        
        pyautogui.click(x=544, y=314) # P300
        importar_trimestres()
        
        pyautogui.click(x=573, y=332) # P400
        importar_trimestres()
        
        pyautogui.click(x=555, y=351) # P500
        importar_trimestres()
        
        pyautogui.click(x=432, y=414) # Expandir nó "Informações Gerais"
        time.sleep(1)
        
        pyautogui.click(x=489, y=431) # Selecionar Y570
        time.sleep(1)
        pyautogui.click(x=1437, y=718) # Botão Importar do Y570
        print("Aguardando importacao Y570 e tratando aviso opcional...")
        
        # ===== MELHORIA 5: AGUARDA Y570 + TRATA AVISO OPCIONAL (Tempo Reduzido) =====
        timeout_y570 = time.time() + 30  # janela máxima de 30s
        aviso_tratado = False
        while time.time() < timeout_y570:
            try:
                btn_sim = pyautogui.locateCenterOnScreen('sim.png', confidence=0.8)
                if btn_sim:
                    pyautogui.click(btn_sim)
                    print("  Aviso pos-Y570 detectado e confirmado com SIM")
                    aviso_tratado = True
                    time.sleep(2)
                    break
            except pyautogui.ImageNotFoundException:
                pass
            except Exception:
                pass
            time.sleep(1) 
        
        if not aviso_tratado:
            print("  Sem aviso pos-Y570 (ja seguiu normalmente)")
        
        time.sleep(2) 
        
        pyautogui.click(x=591, y=462) # Selecionar Y600
        time.sleep(1)
        pyautogui.click(x=1429, y=716) # Botão Importar do Y600
        time.sleep(8)
        
        # --- Y600 MÚLTIPLOS SÓCIOS COM TECLADO ---
        pyautogui.click(x=1392, y=317) # Clica na Célula do primeiro sócio para abrir opções
        time.sleep(0.5)
        
        # Repete a ação para até 5 sócios
        for _ in range(5):
            pyautogui.write('PF') # Digita PF na célula
            time.sleep(0.3)
            pyautogui.press('enter') # Confirma a seleção
            time.sleep(0.3)
            pyautogui.press('down') # Seta para baixo para ir para a próxima linha
            time.sleep(0.3)
        
        pyautogui.click(x=1368, y=808) # Clica OK na barra inferior
        time.sleep(2)
        
        pyautogui.click(x=1223, y=353) # OK do menu principal
        
        print("Aguardando avisos de exportação...")
        timeout = time.time() + 35 
        while time.time() < timeout:
            try:
                btn_sim = pyautogui.locateCenterOnScreen('sim.png', confidence=0.8)
                if btn_sim:
                    pyautogui.click(btn_sim)
                    time.sleep(1)
            except pyautogui.ImageNotFoundException:
                pass
                
            try:
                btn_ok = pyautogui.locateCenterOnScreen('ok.png', confidence=0.8)
                if btn_ok:
                    pyautogui.click(btn_ok)
                    break 
            except pyautogui.ImageNotFoundException:
                pass
                
        time.sleep(2)
        pyautogui.click(x=1298, y=299) # Fechar janela no 'X'
        time.sleep(2)
        
        return True

    except Exception as erro:
        print(f"\n[ERRO] Falha ao processar empresa {codigo_empresa}.")
        print(f"Detalhe: {erro}")
        pyautogui.press('esc', presses=4, interval=0.5)
        time.sleep(2)
        return False

# =========================================================================
# LOOP PRINCIPAL E GRAVAÇÃO
# =========================================================================
contador = 1
for index, row in df_empresas.iterrows():
    codigo = str(row.iloc[3]).replace('.0', '').strip() 
    regime = str(row.iloc[11]).strip().upper() 
    obrigatoriedade = str(row.iloc[12]).strip().upper() 
    
    # Verifica se a empresa JÁ foi processada (status na coluna N)
    status_atual = str(row.iloc[13]).strip().upper() if pd.notna(row.iloc[13]) else ""
    if "TXT GERADO" in status_atual:
        print(f"\n[{contador}/{total_empresas}] Empresa {codigo} JA PROCESSADA - pulando...")
        contador += 1
        continue
    
    print(f"\n[{contador}/{total_empresas}] Processando Empresa: {codigo}")
    
    sucesso = executar_automacao(codigo, regime, obrigatoriedade)
    
    if sucesso:
        df_empresas.at[index, coluna_status] = "TXT GERADO"
    else:
        df_empresas.at[index, coluna_status] = "ERRO AO TENTAR GERAR O TXT"
    
    # Salva a planilha A CADA EMPRESA processada (segurança contra travamentos)
    df_empresas.to_excel(caminho_saida, index=False, sheet_name='PRAZO 1806')
        
    contador += 1

print("\nSalvando planilha com os status...")
df_empresas.to_excel(caminho_saida, index=False, sheet_name='PRAZO 1806')
print(f"Concluído! O arquivo foi salvo em:\n{caminho_saida}")