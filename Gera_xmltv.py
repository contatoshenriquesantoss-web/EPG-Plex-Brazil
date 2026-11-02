import xml.etree.ElementTree as ET
import urllib.request
import gzip
import lzma
import io

# Seus links de EPG
EPG_URLS = [
"https://althierestm.github.io/Lista-RadarTV/epg.xml",
"http://epgontvhdbr.com/",
"https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/br.xml",
"https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/claro.xml",
"https://raw.githubusercontent.com/rootcoder/epgtv/main/guide.xml.gz",
"https://i.mjh.nz/PlutoTV/br.xml",
"https://raw.githubusercontent.com/LITUATUI/M3UPT/refs/heads/main/EPG/epg-rytec-pt.xml.xz",
"https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/epg.xml",
"https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/vivoplay.xml",
"https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/globo.xml",
"https://epgshare01.online/epgshare01/epg_ripper_BR2.xml.gz",
"https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz"
]

def fetch_and_parse(url):
try:
print(f"Baixando: {url}")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=20) as response:
content = response.read()

if url.endswith('.gz') or content[:2] == b'\x1f\x8b':
content = gzip.decompress(content)
elif url.endswith('.xz'):
content = lzma.decompress(content)

return ET.fromstring(content)
except Exception as e:
print(f"Erro ao processar {url}: {e}")
return None

def merge_epgs():
root_merged = ET.Element('tv')

for url in EPG_URLS:
tree = fetch_and_parse(url)
if tree is not None:
for elem in tree:
if elem.tag in ['channel', 'programme']:
root_merged.append(elem)

merged_tree = ET.ElementTree(root_merged)

with open('plex_epg_brasil.xml', 'wb') as f:
merged_tree.write(f, encoding='utf-8', xml_declaration=True)
print("EPG unificado gerado com sucesso!")

if __name__ == '__main__':
merge_epgs()
