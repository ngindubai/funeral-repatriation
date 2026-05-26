import os, re

dirs = ['site/content/cremation-transfer','site/content/bringing-ashes-home','site/content/embassy-contacts']
bad = []
for d in dirs:
    for fn in os.listdir(d):
        if fn.endswith('.md') and fn != '_index.md':
            content = open(os.path.join(d,fn),encoding='utf-8').read()
            m = re.search(r'description: "(.+?)"', content)
            if m:
                desc = m.group(1)
                last_word = desc.rstrip('.').rsplit(' ',1)[-1] if ' ' in desc else ''
                if len(last_word) <= 3 and desc.endswith('.') and len(desc) > 100:
                    bad.append((d.split('/')[-1], fn, len(desc), desc[-40:]))

print(f'Potentially bad truncations: {len(bad)}')
for item in bad[:30]:
    print(item)
