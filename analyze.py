import os
import json
import numpy as np
import scipy.stats

SCORE_MAP = {'bad': 1., 'poor': 2., 'fair': 3., 'good': 4., 'excellent': 5.}
MODEL_MAP = {'0': 'GT-wav', '1': 'GT_HiFi-GAN', '2': 'Tacotron2', '3': 'Glow-TTS',
             '4': 'BVAE-TTS', '5': 'FastSpeech2', '6': 'VAENAR-TTS', '7': 'VAENAR-TTS-R-5',
             '8': 'VAENAR-TTS-R-4', '9': 'VAENAR-TTS-R-3'}


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h


def read_json(json_f):
    evals = {}
    with open(json_f, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for d in data[0]['eps_list']:
            lst = d['ep']
            for item in lst:
                score = SCORE_MAP[item['eval']]
                if item['src'][21] not in evals:
                    evals[item['src'][21]] = [score]
                else:
                    evals[item['src'][21]].append(score)
    fn = json_f.split('-')[0].split('\\')[1]
    print('\nSubject {}:'.format(fn))
    for i in range(10):
        m, h = mean_confidence_interval(np.reshape(evals['{}'.format(i)], -1))
        print(MODEL_MAP[str(i)], "{}±{}".format(m, h), evals['{}'.format(i)])
    # print(evals)
    return evals


def average_scores():
    all_scores = {'0': [], '1': [], '2': [], '3': [], '4': [], '5': [], '6': [],
                  '7': [], '8': [], '9': []}
    files = [os.path.join('results', f) for f in os.listdir('results')]
    print("{} subjects in total...".format(len(files)))
    for f in files:
        score = read_json(f)
        for k in score.keys():
            all_scores[k].append(score[k])
    print('\nOverall:')
    for i in range(10):
        # print(MODEL_MAP[str(i)], all_scores['{}'.format(i)])
        m, h = mean_confidence_interval(np.reshape(all_scores['{}'.format(i)], -1))
        print(MODEL_MAP[str(i)], "{}±{}".format(m, h))
    return all_scores


if __name__ == '__main__':
    scores = average_scores()
