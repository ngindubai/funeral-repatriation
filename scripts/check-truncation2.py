import os, re

BAD_ENDINGS = {'and', 'the', 'to', 'of', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'from', 'or'}

dirs = ['site/content/cremation-transfer','site/content/bringing-ashes-home','site/content/embassy-contacts']
bad = []
for d in dirs:
    for fn in os.listdir(d):
        if fn.endswith('.md') and fn != '_index.md':
            content = open(os.path.join(d,fn),encoding='utf-8').read()
            m = re.search(r'description: "(.+?)"', content)
            if m:
                desc = m.group(1)
                last_word = desc.rstrip('.').rsplit(' ',1)[-1].lower() if ' ' in desc else ''
                if last_word in BAD_ENDINGS:
                    bad.append((d.split('/')[-1], fn, len(desc), desc[-50:]))

print(f'Genuinely bad truncations: {len(bad)}')
for item in bad:
    print(item)
