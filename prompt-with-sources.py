import os
import sys
import argparse
import json

def read_source(fn: str) -> str:
    try:
        with open(fn, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def sources_from_folder(folder: str, ext: str) -> list:
    sources = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                sources.append(os.path.join(root, file))
    return sources

def main():
    sources = sources_from_folder('references', '.txt')

    prompt = """
    Por favor, considerando estas fontes de informação. Liste os alimentos que podem ser consumidos em uma dieta low-carb e aqueles que devem ser evitados. Agrupe os alimentos em categorias e forneça uma breve explicação sobre o motivo de serem recomendados ou evitados. Formate a saída como slides.
    # """
    

    source_list = []
    for source in sources:
        content = read_source(source)
        if content is not None:
            source_list.append({'path': source, 'content': content})
        else:
            print(f"Warning: File '{source}' not found and will be skipped.", file=sys.stderr)

    result = {
        # 'user_request': prompt + " Write only the necessary code to solve the problem and document it.",
        'user_request': prompt,
        'sources': source_list
    }

    json_result = json.dumps(result, indent=4)
    
    print(json_result)
    
    fn_prompt = 'prompt_content.json'
    print(f'\nSaving prompt to {fn_prompt}')
    with open(fn_prompt, 'w') as f:
        f.write(json_result)

if __name__ == "__main__":
    main()
