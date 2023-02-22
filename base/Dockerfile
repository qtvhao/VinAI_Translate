FROM pytorch/pytorch

WORKDIR /app

RUN apt-get update && apt-get install -y git libsndfile1 sox unzip wget

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
tokenizer = AutoTokenizer.from_pretrained('vinai/vinai-translate-en2vi', src_lang='en_XX'); \
model = AutoModelForSeq2SeqLM.from_pretrained('vinai/vinai-translate-en2vi');"
