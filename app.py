from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import signal
import os

app = Flask(__name__)

cache_dir = '/root/.cache/huggingface/hub'

tokenizer_en2vi = AutoTokenizer.from_pretrained("vinai/vinai-translate-en2vi", src_lang="en_XX", cache_dir=cache_dir)
model_en2vi = AutoModelForSeq2SeqLM.from_pretrained("vinai/vinai-translate-en2vi", cache_dir=cache_dir)

@app.route('/translate/en2vi', methods=['POST'])
def translate_en2vi():
    en_text = request.json['en_text']
    input_ids = tokenizer_en2vi(en_text, return_tensors="pt").input_ids

    # Set a 10-second timeout for model generation
    signal.signal(signal.SIGALRM, lambda signum, frame: raise_exception(Exception("Model generation timeout")))
    signal.alarm(30)

    try:
        output_ids = model_en2vi.generate(
            input_ids,
            do_sample=True,
            top_k=100,
            top_p=0.8,
            decoder_start_token_id=tokenizer_en2vi.lang_code_to_id["vi_VN"],
            num_return_sequences=1,
        )
        signal.alarm(0)  # Cancel the timeout if the model generates output within 10 seconds
    except:
        return jsonify({'error': 'Model generation timed out'})

    # Set a 10-second timeout for decoding
    signal.signal(signal.SIGALRM, lambda signum, frame: raise_exception(Exception("Decoding timeout")))
    signal.alarm(30)
    
    try:
        vi_text = tokenizer_en2vi.batch_decode(output_ids, skip_special_tokens=True)
        vi_text = " ".join(vi_text)
        signal.alarm(0)  # Cancel the timeout if the decoding completes within 10 seconds
    except:
        return jsonify({'error': 'Decoding timed out'})

    return jsonify({'vi_text': vi_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
