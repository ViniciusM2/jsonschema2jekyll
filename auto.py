import os
from datetime import date
from pandas import date_range
from unidecode import unidecode
import regex as re

from func.func import jekyllalize, generate_jekyll_headers, gen_jekyll_header


if not os.path.exists('./docs'):
    os.system('jsonschema2md -d schemas -o docs')

    filenames = os.listdir('./docs')

    dates = date_range(
        periods=len(filenames),
        end=date.today(),
    ).to_pydatetime().tolist()

    # print(f"Nomes dos arquivos: {filenames}")

    filenames.sort()

    # print(f"Nomes dos arquivos pós sort: {filenames}")

    iso_dates = map(lambda date: date.date().isoformat(), dates)

    print(f'Número de datas igual a númemro de arquivos: {len(dates) == len(filenames)}')

    dates_filenames = list(zip(iso_dates, filenames))

    for date, filename in dates_filenames:
        new_filename = f'{date}' + '-' + filename
        new_filename = unidecode(new_filename)
        os.rename(f'./docs/{filename}', f'./docs/{new_filename}')

    # filenames = os.listdir('./docs')

    # for filename in filenames:
    #     with open(os.path.join(os.getcwd() + '/docs/', filename), 'r+') as file:
    #         file.seek(0)
    #         first_line = file.readline()
    #         # print(file.name + ' ' + first_line)
    #         splitted = first_line.split(' ')
    #         # print(splitted)

else:
    filenames = os.listdir('./docs')
    headers_meta = []

    for filename in filenames:
        result = ''
        with open(os.path.join(os.getcwd() + '/docs/', filename), 'r+') as file:
            file.seek(0)
            matches = []
            rgx_ref = re.compile(r'[\p{L} -]+[\p{L}].md')
            file_content = file.read()
            occurrences = rgx_ref.findall(file_content)
            # print(occurrences)
            sanitized_occurrences = []

            result = file_content
            for o in occurrences:
                result = result.replace(o, jekyllalize(o), 1)

            # print(result)

        with open(os.path.join(os.getcwd() + '/docs/', filename), 'w') as file:
            file.write(result)

    meta_categories = []
    for filename in filenames:
        with open(os.path.join(os.getcwd() + '/docs/', filename), 'r+') as file:
            file.seek(0)
            first_line = file.readline()
            # print(file.name + '\n' + first_line)
            splitted = first_line.split(' ')
            # print(splitted)
            splitted.pop(0)
            splitted.pop(len(splitted) - 1)
            # print(splitted)
            rejoined = ' '.join(splitted)

            title = rejoined
            # print(title)

            splitted = file.name.split('/')
            splitted = splitted[len(splitted) - 1]
            splitted = splitted.split('-')
            splitted = splitted[3:]

            index_of_properties = None
            try:
                index_of_properties = splitted.index('properties')
            except:
                index_of_properties = None

            # print(splitted)
            # print(index_of_properties)

            if index_of_properties:
                splitted = splitted[0:index_of_properties]

            # print(splitted)

            rejoined = ''.join(splitted)

            tmp_category = rejoined

            tmp_category = tmp_category.replace('.md', '')

            # print(tmp_category)

            meta_categories.append(tmp_category)

            tmp = file.name.split('/')
            tmp = tmp[len(tmp) - 1]
            tmp = tmp.split('-')
            level = tmp.count('properties')
            # print(f'level: {level}')

            print(
                f'título:{title}\ncategoria:{tmp_category}\nprofundidade:{level}\n\n')

            headers_meta.append({
                "title": title,
                "meta_category": tmp_category,
                "level": level,
                "path": file.name
            })

    # print(f"meta: {headers_meta}")
    generate_jekyll_headers(headers_meta)
    # print(f"categories: {tmp_categories}")
