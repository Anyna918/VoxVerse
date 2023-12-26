from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models.encoder import inference as encoder
from models.vocoder.hifigan import inference as gan_vocoder
from models.synthesizer.inference import Synthesizer
from pathlib import Path
from scipy.io.wavfile import write
import librosa
import re
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# 模型配置
encoder_path = 'data\ckpt\encoder\pretrained.pt'
synthesizer_path = 'data\ckpt\synthesizer\pretrained.pt'
vocoder_path = 'data\ckpt\\vocoder\pretrained\g_hifigan.pt'
encoder.load_model(Path(encoder_path))
current_synt = Synthesizer(Path(synthesizer_path))
gan_vocoder.load_model(Path(vocoder_path))

# 文件存储配置
origin_audio_path = 'source\\origin'
result_audio_path = 'source\\result\\result_audio.wav'

"""
作用：标准化音频
参数：
    音频文件
    音频类型
"""


def process_audio(audio, type_value):
    # 实时录音
    if type_value == 1:
        with open(audio, "w+b") as f:
            f.write(audio.as_bytes())
            f.seek(0)
        wav, sample_rate = librosa.load(audio)
    # 上传文件
    else:
        wav, sample_rate = librosa.load(audio)

    # 确保获得正确的wav格式
    write(audio, sample_rate, wav)


"""
作用：上传音频文件
参数：
    音频名称
    音频文件
    音频类型
"""


@app.route('/upload', methods=['POST'])
def upload_audio():
    print('开始上传')
    if 'audio_file' not in request.files:
        return jsonify({'message': '未上传文件'}), 400
    file = request.files['audio_file']
    print('文件名称：', file.filename)

    # 检查是否有文本数据
    if 'text' not in request.form:
        return 'No text part', 400
    # 获取文本数据
    text_data = request.form.get('text', '')

    if 'type' not in request.form:
        return 'No type part', 400
    type_value = request.form.get('type')

    if 'audio_name' not in request.form:
        return 'No type part', 400
    audio_name = request.form.get('audio_name')

    # 修改文件名
    if file.filename:
        filename = secure_filename(file.filename)  # 使用 Werkzeug 的 secure_filename 函数来确保文件名安全
        new_filename = f"{audio_name}.mp3"
        file.filename = new_filename
        print('修改后的文件名：', file.filename)

    # 保存文件
    if not os.path.exists(origin_audio_path):
        os.makedirs(origin_audio_path)  # 如果文件夹不存在，则创建文件夹
    filepath = os.path.join(origin_audio_path, file.filename)
    file.save(filepath)

    # 规范音频文件
    process_audio(filepath, type_value)

    return jsonify({'message': '上传成功'}), 200


"""
作用：返回已经上传的音频文件名称列表
"""


@app.route('/list-audio', methods=["GET"])
def list_audios():
    files = os.listdir(origin_audio_path)
    if not files:
        return jsonify({'message': 'No audio found', 'files': []}), 200
    return jsonify({'files': files}), 200


"""
作用：删除含有的音频
"""


@app.route('/delete-audio', methods=['GET'])
def delete_audio():
    audio_name = request.json.get('audioName')
    if not audio_name:
        return jsonify({'message': 'Invalid audioi'}), 400

    audio_file_path = os.path.join(origin_audio_path, audio_name + '.wav')

    if not os.path.exists(audio_file_path):
        return jsonify({'message': 'Audio file not found'}), 404

    try:
        os.remove(audio_file_path)
        return jsonify({'message': 'Delete successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


"""
作用：利用选中的音频进行合成
参数：
    音频名称：audio_name
    文本: text_data
"""


@app.route('/synthesize', methods=["POST"])
def synthesize():

    data = request.json
    # 获取文本数据
    text_data = data.get('text')
    print(text_data)

    audio_name = data.get('audio_name')

    # 载入音频文件
    wav, sample_rate = librosa.load(os.path.join(origin_audio_path, audio_name))

    source_spec = Synthesizer.make_spectrogram(wav)

    # 预处理
    encoder_wav = encoder.preprocess_wav(wav, sample_rate)
    embed, _, _ = encoder.embed_utterance(encoder_wav, return_partials=True)

    # 加载文本
    texts = filter(None, text_data.split("\n"))
    punctuation = '！，。、,'  # punctuate and split/clean text
    processed_texts = []
    for text in texts:
        for processed_text in re.sub(r'[{}]+'.format(punctuation), '\n', text).split('\n'):
            if processed_text:
                processed_texts.append(processed_text.strip())
    texts = processed_texts

    # 合成音频
    embeds = [embed] * len(texts)
    specs = current_synt.synthesize_spectrograms(texts, embeds)
    spec = np.concatenate(specs, axis=1)
    sample_rate = Synthesizer.sample_rate
    wav, sample_rate = gan_vocoder.infer_waveform(spec)

    # 保存文件
    write(result_audio_path, sample_rate, wav)  # Make sure we get the correct wav
    return 'success', 200

@app.route('/download', methods=["GET"])
def result():
    return send_file(result_audio_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug='true')

