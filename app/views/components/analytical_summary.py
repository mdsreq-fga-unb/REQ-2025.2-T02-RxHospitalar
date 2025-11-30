import tkinter as tk
from tkinter import ttk
import pandas as pd

class AnalyticalSummary(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        
        # Title
        self.title_label = ttk.Label(
            self, 
            text="Resumo Analítico", 
            font=("Segoe UI", 16, "bold"),
            foreground="#343A40",
            background="#F4F9F4"
        )
        self.title_label.pack(anchor="w", padx=20, pady=(20, 10))

         # Separator
        separator = ttk.Separator(self, orient="horizontal")
        separator.pack(fill="x", padx=20, pady=(0, 20))
        
        # Configure styles
        style = ttk.Style()
        style.configure("CardInner.TFrame", background="#F4F9F4", borderwidth=0, relief="flat")

        # Container for cards
        self.cards_container = ttk.Frame(self, style="CardInner.TFrame")
        self.cards_container.pack(fill="both", expand=True)
        self.cards_container.columnconfigure(0, weight=1, uniform="card")
        self.cards_container.columnconfigure(1, weight=1, uniform="card")

        # Initialize cards (labels references to update later)
        self.metrics_labels = {}
        
        self.cards_data = [
            {"key": "criticos", "title": "Produtos críticos", "icon": "📦", "color": "#1e1e1e", "row": 0, "col": 0, "desc_template": "Foram encontrados {} produtos\nem estado crítico."},
            {"key": "baixo", "title": "Baixo estoque", "icon": "⚠️", "color": "#FFA500", "row": 0, "col": 1, "desc_template": "Foram encontrados {} produtos\ncom baixo estoque."},
            {"key": "zerados", "title": "Produtos zerados", "icon": "❌", "color": "#DC3545", "row": 1, "col": 0, "desc_template": "Foram encontrados {} produtos\ncom estoque zerados."},
            {"key": "valor", "title": "Valor total em estoque", "icon": "💲", "color": "#1e1e1e", "row": 1, "col": 1, "desc_template": "O valor total de reais em estoque\né R${:,.2f}"},
            {"key": "maior_estoque", "title": "Linha com maior estoque", "icon": "🔥", "color": "#1e1e1e", "row": 2, "col": 0, "desc_template": "A linha com maior estoque é a {}\nque coresponde a {:.0f}% dos produtos em estoque."},
            {"key": "maior_giro", "title": "Mês de maior giro", "icon": "📈", "color": "#1e1e1e", "row": 2, "col": 1, "desc_template": "O mês com o maior giro foi o de\n{}."}
        ]

        for card in self.cards_data:
            self._create_card(card)

    def _create_card(self, card_info):
        # Card Frame
        frame = ttk.Frame(self.cards_container, style="Card.TFrame", padding=10, relief="raised", borderwidth=1)
        frame.grid(row=card_info["row"], column=card_info["col"], sticky="nsew", padx=10, pady=10)
        
        # Icon Container (Fixed Width for alignment)
        icon_frame = ttk.Frame(frame, width=50, style="CardInner.TFrame")
        icon_frame.pack(side="left", padx=(0, 10), fill="y")
        icon_frame.pack_propagate(False) # Force fixed size

        # Icon
        icon_lbl = ttk.Label(icon_frame, text=card_info["icon"], font=("Segoe UI", 24), 
                             foreground=card_info.get("color", "#1e1e1e"), background="#F4F9F4", anchor="center")
        icon_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Content Frame
        content_frame = ttk.Frame(frame, style="CardInner.TFrame")
        content_frame.pack(side="left", fill="both", expand=True)
        
        # Title
        title_lbl = ttk.Label(content_frame, text=card_info["title"], font=("Segoe UI", 11, "bold"), 
                              foreground="#1e1e1e", background="#F4F9F4")
        title_lbl.pack(anchor="w")
        
        # Description (Value)
        desc_lbl = ttk.Label(content_frame, text="Carregando...", font=("Segoe UI", 10), 
                             foreground="#343A40", background="#F4F9F4", wraplength=250, justify="left")
        desc_lbl.pack(anchor="w", pady=(5, 0))
        
        self.metrics_labels[card_info["key"]] = desc_lbl

    def update_metrics(self, df):
        if df is None or df.empty:
            for key, lbl in self.metrics_labels.items():
                lbl.config(text="Sem dados")
            return

        try:
            # Ensure numeric columns
            # Assuming 'Estoque' is the column name for stock quantity
            # Assuming 'Preço Aquisição' or similar for price
            
            # Normalize columns to find them
            cols_map = {c.lower().strip(): c for c in df.columns}
            
            col_estoque = cols_map.get("estoque")
            col_preco = cols_map.get("preço aquisição") or cols_map.get("preco aquisicao") or cols_map.get("custo")
            col_linha = cols_map.get("grupo") or cols_map.get("linha")
            # For 'Giro', we need a date column or a specific 'Giro' column. 
            # If not found, we might need to infer or skip.
            # Looking at previous files, 'Vendas_Pendencia' might have dates.
            col_data = cols_map.get("data") or cols_map.get("emissao") or cols_map.get("data emissao")

            if not col_estoque:
                print("Coluna de estoque não encontrada para métricas.")
                return

            # Convert to numeric
            df[col_estoque] = pd.to_numeric(df[col_estoque], errors='coerce').fillna(0)
            
            if col_preco:
                df[col_preco] = pd.to_numeric(df[col_preco], errors='coerce').fillna(0)

            # 1. Produtos Críticos (<= 5)
            criticos = df[df[col_estoque] <= 5].shape[0]
            self.metrics_labels["criticos"].config(text=self.cards_data[0]["desc_template"].format(criticos))

            # 2. Baixo Estoque (<= 15)
            baixo = df[df[col_estoque] <= 15].shape[0]
            self.metrics_labels["baixo"].config(text=self.cards_data[1]["desc_template"].format(baixo))

            # 3. Zerados (== 0)
            zerados = df[df[col_estoque] == 0].shape[0]
            self.metrics_labels["zerados"].config(text=self.cards_data[2]["desc_template"].format(zerados))

            # 4. Valor Total
            if col_preco:
                total_val = (df[col_estoque] * df[col_preco]).sum()
                self.metrics_labels["valor"].config(text=self.cards_data[3]["desc_template"].format(total_val))
            else:
                self.metrics_labels["valor"].config(text="Coluna de preço não encontrada")

            # 5. Linha com maior estoque
            if col_linha:
                # Group by line and sum stock
                linha_grp = df.groupby(col_linha)[col_estoque].sum()
                if not linha_grp.empty:
                    maior_linha = linha_grp.idxmax()
                    qtd_linha = linha_grp.max()
                    total_estoque = df[col_estoque].sum()
                    perc = (qtd_linha / total_estoque * 100) if total_estoque > 0 else 0
                    self.metrics_labels["maior_estoque"].config(text=self.cards_data[4]["desc_template"].format(maior_linha, perc))
                else:
                    self.metrics_labels["maior_estoque"].config(text="Sem dados de linha")
            else:
                self.metrics_labels["maior_estoque"].config(text="Coluna de linha não encontrada")

            # 6. Mês de maior giro
            # This is tricky without a clear 'Sales' vs 'Stock' distinction in the unified DF if it's just a snapshot.
            # If the DF is 'Vendas' merged with 'Estoque', then rows are sales?
            # If rows are products, we can't calculate 'Giro' (Turnover) easily without sales history.
            # However, the user asked for "Mês de maior giro".
            # If the main DF is Vendas (which seems to be the case from dashboard_page.py: "Dashboard Unificado (Vendas + Estoque)"),
            # then we can count rows per month.
            if col_data:
                try:
                    df['dt_temp'] = pd.to_datetime(df[col_data], errors='coerce')
                    # Group by month name
                    # locale might be an issue for month names in PT-BR, so let's do manual mapping or simple approach
                    meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                             7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
                    
                    # Count occurrences (sales) per month
                    vendas_por_mes = df['dt_temp'].dt.month.value_counts()
                    if not vendas_por_mes.empty:
                        mes_idx = vendas_por_mes.idxmax()
                        nome_mes = meses.get(mes_idx, str(mes_idx))
                        self.metrics_labels["maior_giro"].config(text=self.cards_data[5]["desc_template"].format(nome_mes))
                    else:
                        self.metrics_labels["maior_giro"].config(text="Sem dados de data válidos")
                except Exception as e:
                    print(f"Erro ao calcular giro: {e}")
                    self.metrics_labels["maior_giro"].config(text="Erro ao calcular data")
            else:
                self.metrics_labels["maior_giro"].config(text="Coluna de data não encontrada")

        except Exception as e:
            print(f"Erro ao atualizar métricas: {e}")
            for lbl in self.metrics_labels.values():
                lbl.config(text="Erro no cálculo")
