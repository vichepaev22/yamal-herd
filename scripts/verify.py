#!/usr/bin/env python3
"""Статическая верификация сборки «ЯМАЛ: СОБЕРИ СТАДО».
Проверяет: баланс скобок во всех inline-скриптах, существование всех DOM-id,
наличие 31 уровня, ключевых систем и обязательных PWA/SEO-элементов."""
import io, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'index.html')
fail, warn = [], []

def read(p):
    return io.open(p, encoding='utf-8').read()

if not os.path.exists(HTML):
    print('FAIL: index.html не найден'); sys.exit(1)
s = read(HTML)

# ── 1. баланс скобок в каждом inline <script> ────────────────────────────────
def scan(src, tag):
    i, n, line, stack = 0, len(src), 1, []
    pairs = {')': '(', ']': '[', '}': '{'}
    while i < n:
        c = src[i]
        if c == '\n': line += 1; i += 1; continue
        if c == '/' and i+1 < n and src[i+1] == '/':
            while i < n and src[i] != '\n': i += 1
            continue
        if c == '/' and i+1 < n and src[i+1] == '*':
            i += 2
            while i+1 < n and not (src[i] == '*' and src[i+1] == '/'):
                if src[i] == '\n': line += 1
                i += 1
            i += 2; continue
        if c in '"\'':
            q = c; i += 1
            while i < n and src[i] != q:
                if src[i] == '\\': i += 1
                if i < n and src[i] == '\n': line += 1
                i += 1
            i += 1; continue
        if c == '`':
            i += 1
            while i < n and src[i] != '`':
                if src[i] == '\\': i += 1
                if src[i] == '\n': line += 1
                i += 1
            i += 1; continue
        if c in '([{': stack.append((c, line))
        elif c in ')]}':
            if not stack: return f'{tag}: лишняя "{c}" (строка {line})'
            op, ln = stack.pop()
            if op != pairs[c]: return f'{tag}: "{op}" (стр.{ln}) закрыта "{c}" (стр.{line})'
        i += 1
    if stack: return f'{tag}: не закрыта "{stack[-1][0]}" (строка {stack[-1][1]})'
    return None

blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s, re.S)
if not blocks: fail.append('не найдено ни одного inline <script>')
for k, b in enumerate(blocks):
    err = scan(b, f'script#{k+1}')
    if err: fail.append(err)
    else:   print(f'   script#{k+1}: скобки OK ({len(b.splitlines())} строк)')

# ── 2. DOM-id: все $('id') и getElementById существуют в разметке ────────────
ids_html = set(re.findall(r'\bid="([A-Za-z0-9_\-]+)"', s))
used = set(re.findall(r"\$\('([A-Za-z0-9_\-]+)'\)", s))
used |= set(re.findall(r"getElementById\('([A-Za-z0-9_\-]+)'\)", s))
missing = sorted(u for u in used if u not in ids_html)
if missing: fail.append(f'JS обращается к несуществующим id: {missing}')
else: print(f'   DOM-id: {len(used)} обращений, все присутствуют ({len(ids_html)} id в разметке)')

# ── 3. уровни: tutorial + 30, без пропусков и дублей ────────────────────────
# Уровни определяются по наличию поля count (главы id 1–3 его не имеют).
lv = [int(x) for x in re.findall(r'\{id:(\d+),name:[^}]*?count:', s)]
if not lv: fail.append('список LEVELS не найден')
else:
    if sorted(lv) != list(range(0, max(lv)+1)): fail.append(f'пропуски/дубли в LEVELS: {sorted(lv)}')
    if len(lv) < 31: warn.append(f'уровней {len(lv)} (ожидается 31: tutorial + 30)')
    print(f'   LEVELS: {len(lv)} шт., id {min(lv)}..{max(lv)}')

# ── 4. обязательные системы ─────────────────────────────────────────────────
must = ['class Engine','InputController','KeyboardInput','TouchInput','GamepadInput',
        'worldToMinimapPosition','dirToMinimapAngle','pulseAlpha','startDogEvent',
        'PLAY_WITH_REINDEER','HERD_ASSIST','RETURN_HOME','DISTRACTED','curMin',
        'objective()','computeMods','COLLECTIBLE_CONFIG','DOG_CONFIG','UPGRADE_CONFIG',
        'CHILDMODE_CONFIG','MAP_PULSE','CHAPTERS','buildTerrainGeo','applyWeather',
        'perfTick','applyPixelRatio','makeIcon','SAVE_KEY','OLD_KEYS','DEBUG_WORLD_BOUNDS']
for k in must:
    if k not in s: fail.append(f'не найдена обязательная сущность: {k}')
print(f'   системы: {len(must)} проверено')

# ── 5. сумма deliveryPattern == count для уровней с паттерном ────────────────
pats = re.findall(r'count:(\d+),pattern:\[([\d,]+)\]', s)
bad = [(c, p) for c, p in pats if sum(int(x) for x in p.split(',')) != int(c)]
if bad: fail.append(f'pattern не совпадает с count: {bad}')
else: print(f'   deliveryPattern: {len(pats)} уровней, суммы совпадают')

# ── 6. максимум оленей не выше прежнего (26) ────────────────────────────────
counts = [int(x) for x in re.findall(r'\{id:\d+,name:[^}]*?count:(\d+)', s)]
if counts and max(counts) > 26: warn.append(f'максимум оленей {max(counts)} > 26')
else: print(f'   макс. оленей на уровне: {max(counts) if counts else "—"} (лимит 26)')

# ── 7. PWA / SEO / мобильная база ───────────────────────────────────────────
web = {'viewport':'name="viewport"', 'viewport-fit':'viewport-fit=cover', 'theme-color':'name="theme-color"',
       'manifest':'rel="manifest"', 'og:title':'property="og:title"', 'description':'name="description"',
       'safe-area':'env(safe-area-inset-', 'touch-action':'touch-action:none', 'noscript':'<noscript>',
       'lang':'<html lang="ru"', 'apple-mobile':'apple-mobile-web-app-capable'}
for name, needle in web.items():
    if needle not in s: fail.append(f'в index.html отсутствует {name} ({needle})')
print(f'   web-база: {len(web)} проверок')

for f in ['manifest.webmanifest','robots.txt','sitemap.xml','404.html','public/icon.svg',
          'public/icon-192.png','public/icon-512.png','README.md','LICENSE',
          '.github/workflows/deploy.yml','.github/workflows/ci.yml']:
    if not os.path.exists(os.path.join(ROOT, f)): fail.append(f'нет файла: {f}')

print()
for w in warn: print('WARN:', w)
for f in fail: print('FAIL:', f)
if fail:
    print(f'\n✖ VERIFY FAILED ({len(fail)})'); sys.exit(1)
print('\n✔ VERIFY PASSED — сборка готова к публикации')
