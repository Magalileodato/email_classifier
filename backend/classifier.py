from __future__ import annotations
from typing import Dict, Tuple

# Labels possíveis para a classificação de e-mails
CANDIDATE_LABELS = ["Produtivo", "Improdutivo"]


class EmailClassifier:
    def __init__(self) -> None:
        """
        Inicializa o classificador de e-mails.
        - Tenta carregar o modelo Hugging Face (zero-shot classification).
        - Se não conseguir, usa um fallback baseado em palavras-chave.
        """
        self.pipeline = None
        self.model_loaded = False

        try:
            # Importação dentro do construtor (lazy import)
            from transformers import pipeline  

            # Carrega a pipeline zero-shot (faz download do modelo se necessário)
            self.pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            self.model_loaded = True

        except Exception as e:
            # Caso o modelo não possa ser carregado (ex: sem internet),
            # o sistema continua funcionando com regras simples.
            print(f"[classifier] Aviso: não foi possível carregar o modelo HF. Usando fallback. Motivo: {e}")
            self.pipeline = None
            self.model_loaded = False

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
        if self.pipeline is not None:
            try:
                result = self.pipeline(text, candidate_labels=CANDIDATE_LABELS)

                # Extrai labels e scores retornados pelo modelo
                labels = result.get("labels", [])
                scores = result.get("scores", [])

                # Cria dicionário {label: score}
                score_map = {lbl: float(scr) for lbl, scr in zip(labels, scores)}

                # O labels[0] vem com a maior probabilidade
                predicted = labels[0] if labels else "Produtivo"

                # Garante que sempre haja as duas chaves
                for lbl in CANDIDATE_LABELS:
                    score_map.setdefault(lbl, 0.0)

                return predicted, score_map

            except Exception as e:
                # Caso a inferência falhe, usa o fallback
                print(f"[classifier] Falha na inferência HF. Caindo para fallback. Motivo: {e}")

        # --- 2) Fallback: baseado em palavras-chave ---
        lowered = text.lower()

        # Conta quantas keywords de cada categoria aparecem no texto
        prod_hits = sum(1 for kw in self.prod_keywords if kw in lowered)
        impr_hits = sum(1 for kw in self.improd_keywords if kw in lowered)

        # Heurística simples para decidir a classe final
        if prod_hits > impr_hits:
            label = "Produtivo"
        elif impr_hits > prod_hits:
            label = "Improdutivo"
        else:
            # Empate: defaulta para Produtivo (prioriza ação)
            label = "Produtivo"

        # Converte contagens em "pseudo-scores" normalizados (0..1)
        total = max(prod_hits + impr_hits, 1)  # evita divisão por zero
        scores = {
            "Produtivo": prod_hits / total,
            "Improdutivo": impr_hits / total
        }

        return label, scores
