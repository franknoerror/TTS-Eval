import os 
import json

guide_info = "Given example native pronunciation of a phone, decide whether corresponding phone in wrod(s) is a standard one or not. \nYes-standard, No-not standard, Not sure-not sure"

def build_nc_config():
    nc_config_list = []
    base_rel_dir = 'static/data'
    for ep in os.listdir(base_rel_dir):
        ep_config = {}
        print(ep)
        ep_type, ep_name = ep.strip().split('-')
        ep_dir = os.path.join(base_rel_dir, ep)
        ep_config['name'] = ep_name
        ep_config['type'] = ep_type
        ep_config['guide'] = guide_info
        ep_config['cur_ep_id'] = 1
        ep_config['tot_eps_num'] = len(os.listdir(ep_dir))
        ep_config['eps_list'] = []
        for ph in os.listdir(ep_dir):
            ph_info = {}
            ph_dir = os.path.join(ep_dir, ph)
            ph_info['ep'] = []
            for wav_name in os.listdir(ph_dir):
                rel_wav_name = os.path.join(ph_dir, wav_name)
                if 'categorical_' in rel_wav_name:
                    ph_info['cate'] = rel_wav_name
                else:
                    word = wav_name.split('_')[0].strip()
                    anno_seq = wav_name.split('_')[1].split('.')[0].strip()
                    word_trans = word + '(' + anno_seq + ')'
                    wav_info = {}
                    wav_info['src'] = rel_wav_name
                    wav_info['eval'] = 'Yes'
                    wav_info['trans'] = word_trans
                    ph_info['ep'].append(wav_info)
            ph_info['ts'] = 'Native pronunciation of phone {}'.format(ph)
            ep_config['eps_list'].append(ph_info)
        nc_config_list.append(ep_config)
    return nc_config_list 


if __name__ == "__main__":
    nc_config_list = build_nc_config()
    config_str = json.JSONEncoder().encode(nc_config_list)
    config_str = "var config = " + config_str
    saving_path = 'static/scripts/config.js'
    with open(saving_path, 'w') as f:
        f.write(config_str)