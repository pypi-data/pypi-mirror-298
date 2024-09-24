import numpy as np
from openai import OpenAI
import os
import plotly.graph_objects as go
from scipy.special import logsumexp
from .utils import get_completion

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class FlexibleScorer:
    def __init__(self, criteria, model="gpt-4o-mini"):
        self.model = model
        self.criteria = criteria
        self.categories = list(range(1, 11))  # 1 to 10

    def map_token_to_category(self, token):
        token = token.strip().lower()
        mapping = {
            '1': ['1', 'one', '一', '١', '१'],
            '2': ['2', 'two', '二', '٢', '२'],
            '3': ['3', 'three', '三', '٣', '३'],
            '4': ['4', 'four', '四', '٤', '४'],
            '5': ['5', 'five', '五', '٥', '५'],
            '6': ['6', 'six', '六', '٦', '६'],
            '7': ['7', 'seven', '七', '٧', '७'],
            '8': ['8', 'eight', '八', '٨', '८'],
            '9': ['9', 'nine', '九', '٩', '९'],
            '10': ['10', 'ten', '十', '١٠', '१०']
        }

        for category, tokens in mapping.items():
            if token in tokens:
                return category
        return None

    def score(self, text, additional_instructions=""):
        prompt = f"""You are an expert at evaluating content based on specific criteria. Your task is to rate the following content on a scale of 1 to 10 for the given criteria.

Criteria to evaluate: {self.criteria}

Scale definition:
1 - Lowest possible score for the given criteria
3 - Significantly below average for the criteria
5 - Average or moderate level for the criteria
7 - Significantly above average for the criteria
10 - Highest possible score, exceptional level for the criteria

Instructions:
1. Carefully examine the content provided.
2. Consider only the specified criteria, ignoring other aspects unless they directly relate to the criteria.
3. If the criteria are complex or multi-faceted, consider all aspects in your evaluation.
4. Use the full range of the scale from 1 to 10.
5. Compare the content to a broad range of other content you're aware of, considering diverse contexts and styles.
6. Ensure your rating accurately reflects how well the content meets the specified criteria.
7. Do not let the length of the content unduly influence your rating - focus on the quality of the content, not the quantity of text.

{additional_instructions}

Content to evaluate:
{text}

Provide your rating as a single integer between 1 and 10. Do not include any other text, explanation, or commentary in your response.

Rating:"""
        response = get_completion([{"role": "user", "content": prompt}], model=self.model)

        all_logprobs = {str(cat): [] for cat in self.categories}

        print("\nDetailed logprobs for each token:")
        for token_info in response.choices[0].logprobs.content:
            print(f"\nToken: {token_info.token}")
            for logprob in token_info.top_logprobs:
                print(f"  {logprob.token}: {logprob.logprob:.4f}")
                mapped_token = self.map_token_to_category(logprob.token)
                if mapped_token:
                    all_logprobs[mapped_token].append(logprob.logprob)
                    print(f"    Mapped to category: {mapped_token}")

        print("\nAccumulated logprobs for each category:")
        for cat, lps in all_logprobs.items():
            print(f"  Category {cat}: {lps}")

        # Convert logprobs to log-probabilities
        log_probs = {}
        print("\nConverting logprobs to log-probabilities:")
        for cat, lps in all_logprobs.items():
            if lps:
                log_prob = logsumexp(lps)
            else:
                log_prob = -np.inf
            log_probs[cat] = log_prob
            print(f"  Category {cat}: {log_prob:.6f}")

        # Normalize log-probabilities
        log_total = logsumexp(list(log_probs.values()))
        normalized_log_probs = {cat: lp - log_total for cat, lp in log_probs.items()}

        print("\nNormalized log-probabilities:")
        for cat, log_prob in normalized_log_probs.items():
            print(f"  Category {cat}: {log_prob:.6f}")

        # Convert to probabilities for final calculation
        normalized_probs = {cat: np.exp(lp) for cat, lp in normalized_log_probs.items()}
        print("\nNormalized probabilities:")
        for cat, prob in normalized_probs.items():
            print(f"  Category {cat}: {prob:.6e}")

        # Calculate weighted average score
        weighted_score = sum(float(cat) * prob for cat, prob in normalized_probs.items())
        print(f"\nWeighted score: {weighted_score:.6f}")

        # Normalize to 0-1 range
        final_score = (weighted_score - 1) / 9  # (score - min) / (max - min)
        print(f"Final normalized score: {final_score:.6f}")

        return round(final_score, 3)

    def plot_results(self, texts, scores):
        fig = go.Figure(data=[go.Bar(
            x=[f"Text {i + 1}" for i in range(len(texts))],
            y=scores,
            text=[f"{score:.3f}" for score in scores],
            textposition='auto',
            hovertext=texts,
            marker_color='rgb(158,202,225)',
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1.5,
            opacity=0.6
        )])

        fig.update_layout(
            title=f'Scores based on criteria: "{self.criteria}"',
            xaxis_title='Texts',
            yaxis_title='Score',
            yaxis_range=[0, 1],
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Rockwell"
            )
        )

        fig.show()


