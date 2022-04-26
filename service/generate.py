import os
import tensorflow as tf

from modeling import GPT2Model, tokenizer, vocab, tf_top_k_top_p_filtering


def generate_sent_sda(seed_word, model, max_step=200, greedy=False, top_k=0, top_p=0.):
    sent = seed_word
    toked = tokenizer(sent)
    count = 0

    for _ in range(max_step):
        input_ids = tf.constant([vocab[vocab.bos_token], ] + vocab[toked])[None, :]
        outputs = model(input_ids)[:, -1, :]
        if greedy:
            gen = vocab.to_tokens(tf.argmax(outputs, axis=-1).numpy().tolist()[0])
        else:
            output_logit = tf_top_k_top_p_filtering(outputs[0], top_k=top_k, top_p=top_p)
            gen = vocab.to_tokens(tf.random.categorical(output_logit, 1).numpy().tolist()[0])[0]
        if gen == '</s>':
            break
        sent += gen.replace('▁', ' ')
        toked = tokenizer(sent)

        if gen == '.' and count > 1:
            break
        count += 1

    return sent

def generate_algorithm(keyword, size):
    fullTextList = []
    finetuning_model_path = './asset'
    model_name = 'dentist_model' #초기 치과 버전 -> type 별로 수정 필요

    sda_save_path = os.path.join(finetuning_model_path, model_name)

    sda_gpt_model = GPT2Model(sda_save_path)

    keyword = generate_sent_sda(keyword, sda_gpt_model, top_k=0, top_p=0.95)

    fullTextList.append(keyword)  # 초기 문장

    for i in range(size):
        # i 가 2 이하일 때는 전체 리스트로 생성
        # i 가 3 이상일 때는  i-3, i 까지 리스트 문장을 가져와서 생성, 3 => 변수로 설정
        keywordText = "\n".join(fullTextList) if i < 3 else "\n".join(fullTextList[i - 3:])

        newText = generate_sent_sda(keywordText, sda_gpt_model, top_k=0, top_p=0.95)

        limitSize = len(keywordText)

        newText = newText[limitSize:]

        fullTextList.append(newText)
    fullText = "\n".join(fullTextList)

    return fullText


def response_body_sda(keyword, size):
    result = {}

    text = generate_algorithm(keyword,size)
    result['text'] = text

    return result
