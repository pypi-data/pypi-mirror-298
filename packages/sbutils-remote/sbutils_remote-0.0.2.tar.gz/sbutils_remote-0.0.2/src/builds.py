import re
import requests

from .printing import print, input


def get_build_link(release: str, substring: str) -> str:
    '''
    Get the build link for the given release.
    '''
    release_short = release.replace('.', '')[:3]
    page = f'http://build.stone.branch/rel/agent/release/RB_WA_{release_short}/current/'
    links = listings(page, substring)
    if not links:
        raise ValueError(f'No builds found for release {release} and matching {substring}')

    if len(links) == 1:
        return page + links[0]

    print('Available builds:\n')
    for i, link in enumerate(links):
        print(f'{i+1}'.ljust(3), ':', link)
    print()
    choice = input('ACTION REQUIRED >> Enter the number of the build to download: ')
    print()
    return page + links[int(choice)-1]


def listings(url, substring):
    response = requests.get(url).text
    response = response.replace('\\n', '\n')
    links = re.findall('href="(.+?)"', response)
    result = []
    for link in links:
        if substring in link and not link.endswith('.asc'):
            result.append(link)
    return result
