#!/usr/bin/env python3
import os
import shutil

INSTALLED_PATH = '/Applications/League of Legends.app/Contents/LoL/RADS/projects/league_client/releases'
# INSTALLED_PATH = '/Users/jongwony/Downloads'

replaces = [
    {'origin': r'rso_platform_id: OC1', 'old_new': ('OC1', 'KR')},
    {'origin': r'chat_host: chat.oc1.lol.riotgames.com', 'old_new': ('oc1', 'kr')},
    {'origin': r'discoverous_service_location: lolriot.pdx1.oc1', 'old_new': ('pdx1.oc1', 'icn1.kr')},
    {'origin': r'discoverous_service_location: lolriot.pdx1.oc1', 'old_new': ('pdx1.oc1', 'icn1.kr')},
    {'origin': r'lcds_host: prod.oc1.lol.riotgames.com', 'old_new': ('oc1', 'kr')},
    {'origin': r'login_queue_url: https://lq.oc1.lol.riotgames.com/login-queue/rest/queues/lol', 'old_new': ('oc1', 'kr')},
    {'origin': r'eula: http://oce.leagueoflegends.com/{language}/legal/eula', 'old_new': ('oce.leagueoflegends.com/{language}/legal/eula', 'www.leagueoflegends.co.kr/?m=rules&cid=3')},
    {'origin': r'terms_of_use: http://oce.leagueoflegends.com/{language}/legal/termsofuse', 'old_new': ('oce.leagueoflegends.com/{language}/legal/termsofuse', 'www.leagueoflegends.co.kr/?m=rules&cid=1')},
    {'origin': r'payments_host: https://plstore.oc1.lol.riotgames.com', 'old_new': ('oc1', 'kr')},
    {'origin': r'rms_url: wss://us.edge.rms.si.riotgames.com:443', 'old_new': ('us', 'asia')},
    {'origin': r'api_url: https://status.leagueoflegends.com/shards/oce/synopsis', 'old_new': ('oce', 'kr')},
    {'origin': r'human_readable_status_url: https://status.leagueoflegends.com/#oce', 'old_new': ('oce', 'kr')},
    {'origin': r'store_url: https://store.oc1.lol.riotgames.com', 'old_new': ('oc1', 'kr')},
    {'origin': r'voice_domain: riotp0apse2.vivox.com', 'old_new': ('apse2', 'apne1')},
    {'origin': r'voice_url: https://riotp0apse2.www.vivox.com/api2', 'old_new': ('apse2', 'apne1')},
    {'origin': r'web_region: oce', 'old_new': ('oce', 'kr')},
]


def replace_iter(string):
    for piece in replaces:
        if string.strip() == piece['origin']:
            yield string.replace(*piece['old_new'])
        else:
            continue

if __name__ == '__main__':
    patch_dirs = [os.path.join(INSTALLED_PATH, patch_dir) for patch_dir in os.listdir(INSTALLED_PATH)]
    recent_patch_dir = max(patch_dirs, key=os.path.getmtime)
    recent_patch_message = 'Recent Patch: {}'.format(recent_patch_dir)
    print(recent_patch_message)

    yaml_file = os.path.join(recent_patch_dir, 'deploy', 'system.yaml')
    copy_yaml_file = os.path.join(recent_patch_dir, 'deploy', 'system.yaml.backup')

    if not os.path.isfile(copy_yaml_file):
        shutil.copy2(yaml_file, copy_yaml_file)

        with open(copy_yaml_file, mode='r') as f:
            data = f.read()

        split_data = data.split('\n')
        for i, origin in enumerate(split_data):
            try:
                found = next(replace_iter(origin))
                if found:
                    origin = found
                    print(origin)
            except StopIteration:
                pass

            split_data[i] = origin

        with open(yaml_file, mode='w') as f:
            f.write('\n'.join(split_data))

        print('Success!')
    else:
        print('system.yaml.backup exists!')

    os.popen('open {}'.format(os.path.join(recent_patch_dir, 'deploy', 'leagueClient')))

