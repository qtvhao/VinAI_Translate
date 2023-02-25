from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
import signal

app = Flask(__name__)

cache_dir = '/root/.cache/huggingface/hub'

tokenizer_en2vi = AutoTokenizer.from_pretrained("vinai/vinai-translate-en2vi", src_lang="en_XX", cache_dir=cache_dir)
model_en2vi = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-en2vi", cache_dir=cache_dir)

def handler(signum, frame):
    raise Exception("Timed out")

@app.route('/translate/en2vi', methods=['POST'])
def translate_en2vi():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)  # set a 30 second timeout

    try:
        en_text = request.json['en_text']
        input_ids = tokenizer_en2vi(en_text, return_tensors="pt").input_ids
        output_ids = model_en2vi.generate(
            input_ids,
            do_sample=True,
            top_k=100,
            top_p=0.8,
            decoder_start_token_id=tokenizer_en2vi.lang_code_to_id["vi_VN"],
            num_return_sequences=1,
        )
        vi_text = tokenizer_en2vi.batch_decode(output_ids, skip_special_tokens=True)
        vi_text = " ".join(vi_text)
        return jsonify({'vi_text': vi_text})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        signal.alarm(0)  # clear the alarm

if __name__ == '__main__':
    with signal_handler(signal.SIGINT, handler):
        app.run(host='0.0.0.0', port=80)
