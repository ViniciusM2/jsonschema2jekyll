import os
from datetime import date
from pandas import date_range
from unidecode import unidecode
import regex as re


def jekyllalize(o):
    # cópia de o é criada
    jekyll_o = ''.join(o)
    jekyll_o = jekyll_o.replace('.md', '')
    jekyll_o = unidecode(jekyll_o)
    jekyll_o = '#/' + jekyll_o
    return jekyll_o

def generate_jekyll_headers(meta_headers):
    for meta in meta_headers:
        # print(meta,end='\n\n')
        if meta.get('level', None) == 0:
            # print(meta,end='\n\n')
            meta['category'] = meta['title']

    root_metas = list(filter(lambda meta: meta.get(
        'category') is not None, meta_headers))
    # print(metas_with_category,end='\n\n')

    for root in root_metas:
        meta_category_of_root = root['meta_category']
        category_of_root = root['category']
        for meta in meta_headers:
            if meta.get('level', None) != 0:
                if meta_category_of_root == meta.get('meta_category', None):
                    meta['category'] = category_of_root

    for meta in meta_headers:
        filename = meta['path']

        # print(meta, end='\n\n')
        result = ''
        with open(filename, 'r+') as file:
            file.seek(0)
            file_content = file.read()
            jekyll_h = gen_jekyll_header(meta['title'], meta['category'], meta['level'])
            print(jekyll_h)
            result = jekyll_h + file_content
        
        with open(filename, 'w') as file:
            file.write(result)

def gen_jekyll_header(title, category, subarticle):
    return f"""---
title: '{title}'
category: {category}
subarticle: {subarticle}

layout: null
---\n\n"""