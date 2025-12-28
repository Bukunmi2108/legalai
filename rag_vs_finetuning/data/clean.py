import os, json, re
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), 'full_contract_txt')
DOC_NAME_XLSX = os.path.join(os.path.dirname(__file__), 'Label Report - Document Name.xlsx')
GOV_LAW_XLSX = os.path.join(os.path.dirname(__file__), 'Label Report - Governing Law.xlsx')

def load_xlsx_mapping(xlsx_path, key_col, value_col):
	df = pd.read_excel(xlsx_path, engine='openpyxl')
	mapping = dict(zip(df[key_col].astype(str).str.strip(), df[value_col].astype(str).str.strip()))
	return mapping

def get_doc_id(filename):
	return os.path.splitext(filename)[0]

def clean_text(text):
	text = text.strip()
	text = re.sub(r'\n{2,}', '\n', text)
	return text

def main():
	# Load mappings from XLSX files
	doc_name_map = load_xlsx_mapping(DOC_NAME_XLSX, 'Filename', 'Document Name')
	gov_law_map = load_xlsx_mapping(GOV_LAW_XLSX, 'Filename', 'Governing Law')

	results = []
	for fname in os.listdir(DATA_DIR):
		if not fname.endswith('.txt'):
			continue
		fpath = os.path.join(DATA_DIR, fname)
		with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
			raw_text = f.read()
		doc_id = get_doc_id(fname)
		if fname.endswith('.txt'):
			base = fname.rsplit('.', 1)[0]
			if base.isupper():
				mapping_key = base + '.PDF'
			else:
				mapping_key = base + '.pdf'
		else:
			mapping_key = fname
			
		governing_law = gov_law_map.get(mapping_key, '')
		title = doc_name_map.get(mapping_key, '')
		text = clean_text(raw_text)
		results.append({
			'doc_id': doc_id,
			'title': re.sub(r'\s*\(.*?\)', '', title).strip(),
			'governing_law': re.sub(r'\s*\(.*?\)', '', governing_law).strip(),
			'text': text
		})
	return results

if __name__ == "__main__":
	contracts = main()
	output_path = os.path.join(os.path.dirname(__file__), 'contracts_cleaned.json')
	with open(output_path, 'w', encoding='utf-8') as f:
		json.dump(contracts, f, ensure_ascii=False, indent=2)
	print(f"Contracts written to {output_path}")
