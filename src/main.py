from dataclasses import dataclass
import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests_cache import CachedSession
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR,
                       MAIN_DOC_URL,
                       MAIN_PEP_URL,
                       EXPECTED_STATUS,
                       PEP_STATUS_COUNTER)
from outputs import control_output
from utils import find_tag, get_response


@dataclass
class PEPObject:
    abbr: str
    internal_link: str

    def __post_init__(self):
        self.internal_link = urljoin(MAIN_PEP_URL, self.internal_link)

    @property
    def internal_status(self):
        session = CachedSession()
        response = get_response(session, self.internal_link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features='lxml')
        article = find_tag(soup, 'article')
        pattern = re.compile(r'rfc2822 \w+')
        rfc_tag = find_tag(article, 'dl', attrs={'class': pattern})
        inner_status = ''
        for idx in range(len(rfc_tag.find_all())):
            if rfc_tag.find_all()[idx].text == 'Status:':
                inner_status = rfc_tag.find_all()[idx+2].text
        return inner_status


def pep(session):
    response = session.get(MAIN_PEP_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    pep_article = soup.find('article')
    pep_content = pep_article.find(id='pep-content')
    content_sections = pep_content.find(id='index-by-category')
    tr_tags = content_sections.find_all('tr')

    pep_objects = []

    for tag in tr_tags:
        if tag.find('abbr'):
            obj = PEPObject(
                tag.find('abbr').text,
                tag.find(
                    'a', attrs={'class': 'pep reference internal'}
                )['href']
            )
            pep_objects.append(obj)

    for obj in tqdm(pep_objects, desc='Обработка данных'):
        if obj.internal_status not in EXPECTED_STATUS[obj.abbr[1:]]:
            logging.error(
                'Несовпадающие статусы:\n'
                f'{obj.internal_link}\n'
                f'Статус в карточке: {obj.internal_status}\n'
                'Ожидаемые статусы:\n'
                f'{EXPECTED_STATUS[obj.abbr[1:]]}'
            )
        if obj.internal_status in PEP_STATUS_COUNTER.keys():
            PEP_STATUS_COUNTER[obj.internal_status] += 1
        else:
            PEP_STATUS_COUNTER['Other'] += 1

    PEP_STATUS_COUNTER['Total'] = len(pep_objects)

    return PEP_STATUS_COUNTER


def whats_new(session):
    # Вместо константы WHATS_NEW_URL, используйте переменную whats_new_url.
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    response.encoding = 'utf-8'

    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')

    step_1 = find_tag(soup, 'section', attrs={'id': "what-s-new-in-python"})
    step_2 = find_tag(step_1, 'div', attrs={'class': 'toctree-wrapper'})
    step_3 = step_2.find_all('li', attrs={'class': 'toctree-l1'})

    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]

    for tag in tqdm(step_3, desc='Парсинг...'):
        version_a_tag = find_tag(tag, 'a')
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        response.encoding = 'utf-8'

        if response is None:
            continue

        soup = BeautifulSoup(response.text, features='lxml')
        response.encoding = 'utf-8'
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        result.append((version_link, h1.text, dl_text))

    return result


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    response.encoding = 'utf-8'

    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebar'})
    ul_tags = sidebar.find_all('ul')
    result = [('Ссылка на документацию', 'Версия', 'Статус')]

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception('Ничего не нашлось')

    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for tag in a_tags:
        link = tag["href"]
        if re.match(pattern, tag.text):
            version, status = re.match(pattern, tag.text).group(1, 2)
        else:
            version = tag.text
            status = ""
        result.append((link, version, status))

    return result


def download(session):
    # Вместо константы DOWNLOADS_URL, используйте переменную downloads_url.
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    response.encoding = 'utf-8'

    if response is None:
        return

    soup = BeautifulSoup(response.text, features='lxml')
    table = find_tag(soup, 'table', attrs={'class': 'docutils'})

    pdf_tag = table.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})

    pdf_a4_link = pdf_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)

    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)

    archive_path = downloads_dir / filename

    archive_response = get_response(session, archive_url)
    response.encoding = 'utf-8'

    with open(archive_path, 'wb') as file:
        file.write(archive_response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
