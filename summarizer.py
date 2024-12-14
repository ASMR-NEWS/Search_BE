from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("gogamza/kobart-summarization")

# 텍스트 길이 제한 함수
def limit_text_length(text, max_length=1000):
    return text[:max_length]

# 요약 함수
def summarize_text(texts):
    summaries = []
    for text in texts:
        text = limit_text_length(text)
        input_ids = tokenizer.encode(text, return_tensors="pt")
        summary_ids = model.generate(
            input_ids=input_ids,
            max_length=128,
            min_length=32,
            length_penalty=1.0,
            num_beams=4,
            early_stopping=True
        )
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))
    return summaries
