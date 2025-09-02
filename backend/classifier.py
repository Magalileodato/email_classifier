from __future__ import annotations
from typing import Dict, Tuple

# Labels possíveis para a classificação de e-mails
CANDIDATE_LABELS = ["Produtivo", "Improdutivo"]


class EmailClassifier:
    def __init__(self, model_name: str = "facebook/distilbart-large-mnli") -> None:
        """
        Inicializa o classificador de e-mails.
        - Não carrega o modelo imediatamente (lazy loading).
        - Se o modelo não puder ser carregado, usa fallback.
        """
        self.pipeline = None
        self.model_loaded = False
        self.model_name = model_name  # modelo leve para reduzir memória

        # Palavras-chave usadas no fallback baseado em regras
        self.prod_keywords = {
            "status", "andamento", "atualização", "suporte", "erro", "problema", "acesso",
            "pedido", "solicitação", "requisicao", "requerimento", "caso", "chamado", "contrato",
            "fatura", "pagamento", "anexo", "documento", "prazo", "urgente", "bloqueio", "dúvida"
        }

        self.improd_keywords = {
            "obrigado", "agradeço", "feliz", "parabéns", "bom dia", "boa tarde", "boa noite",
            "atenciosamente", "saudações", "boas festas", "natal", "ano novo", "congratulações"
        }

    def _load_pipeline(self):
        """
        Carrega o pipeline Hugging Face apenas na primeira requisição.
        """
        if self.pipeline is None:
            try:
                from transformers import pipeline  # importação lazy

                self.pipeline = pipeline("zero-shot-classification", model=self.model_name)
                self.model_loaded = True
            except Exception as e:
                print(f"[classifier] Aviso: não foi possível carregar o modelo HF. Usando fallback. Motivo: {e}")
                self.pipeline = None
                self.model_loaded = False

    def classify(self, text: str) -> Tuple[str, Dict[str, float]]:
        """
        Classifica um e-mail como "Produtivo" ou "Improdutivo".
        Retorna:
            - Label predito
            - Dicionário com scores para cada classe
        """

        # Pré-processamento: remove espaços extras e garante string válida
        text = (text or "").strip()
        if not text:
            return "Improdutivo", {"Produtivo": 0.0, "Improdutivo": 1.0}

        # --- 1) Caminho preferencial: modelo zero-shot da Hugging Face ---
        self._load_pipeline()
        if self.pipeline is not None:
            try:
                result = self.pipeline(text, candidate_labels=CANDIDATE_LABELS)

                labels = result.get("labels", [])
                scores = result.get("scores", [])

                score_map = {lbl: float(scr) for lbl, scr in zip(labels, scores)}
                predicted = labels[0] if labels else "Produtivo"

                for lbl in CANDIDATE_LABELS:
                    score_map.setdefault(lbl, 0.0)

                return predicted, score_map

            except Exception as e:
                print(f"[classifier] Falha na inferência HF. Caindo para fallback. Motivo: {e}")

        # --- 2) Fallback: baseado em palavras-chave ---
        lowered = text.lower()
        prod_hits = sum(1 for kw in self.prod_keywords if kw in lowered)
        impr_hits = sum(1 for kw in self.improd_keywords if kw in lowered)

        if prod_hits > impr_hits:
            label = "Produtivo"
        elif impr_hits > prod_hits:
            label = "Improdutivo"
        else:
            label = "Produtivo"

        total = max(prod_hits + impr_hits, 1)
        scores = {
            "Produtivo": prod_hits / total,
            "Improdutivo": impr_hits / total
        }

        return label, scores
