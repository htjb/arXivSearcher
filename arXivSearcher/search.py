import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta


class searcher():
    def __init__(self, search, **kwargs):
        self.split_search = search.split(" ")
        self.max_results = kwargs.pop('max_results', 5)
        self.date_limited = kwargs.pop('date_limited', False)
        self.print = kwargs.pop('print', True)

        def fill(find, i, updated, published):
            find['update_date'] = updated
            find['published_date'] = published
            find['title'] = title_elems[i].find('title').text
            find['id'] = title_elems[i].find('id').text
            authors = title_elems[i].find_all('name')
            find['authors_len'] = len(authors)
            for j in range(len(authors)):
                find['author_' + str(j)] = authors[j].text
            find['abstract'] = title_elems[i].find('summary').text

        today = str(date.today() - timedelta(1))

        url = ['http://export.arxiv.org/api/query?search_query=all:']
        for i in range(len(self.split_search)):
            if i != len(self.split_search) - 1:
                url.append(self.split_search[i] + '+AND+')
            else:
                url.append(self.split_search[i])
        url.append('&sortBy=lastUpdatedDate&sortOrder=descending&max_results=')
        url.append(str(self.max_results))
        url = ''.join(url)

        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'lxml')

        title_elems = soup.find_all('entry')
        self.finds = []
        for i in range(len(title_elems)):
            find = {}
            updated = title_elems[i].find('updated').text.split('T')[0]
            published = title_elems[i].find('published').text.split('T')[0]
            if self.date_limited is True:
                if today in set([updated, published]):
                    fill(find, i, updated, published)
            else:
                fill(find, i, updated, published)
            if find:
                self.finds.append(find)

        if self.print is True:
            print('arXiv search results for \"' + search + '\":\n')
            self.finds = list(reversed(self.finds))
            for i in range(len(self.finds)):
                print('~'*80 + '\n' +
                      'TITLE: ' + str(self.finds[i]['title']) + '\n\n' +
                      'URL: ' + str(self.finds[i]['id']) + '\n\n' +
                      'UPDATED: ' + str(self.finds[i]['update_date']) +
                      ', PUBLISHED: ' + str(self.finds[i]['published_date']) +
                      '\n\n' +
                      'AUTHORS: ' + ', '.join([
                        self.finds[i]['author_' + str(j)]
                        for j in range(self.finds[i]['authors_len'])]) +
                      '\n\n' +
                      'ABSTRACT: ' + str(self.finds[i]['abstract']))
            print(str(len(self.finds)) +
                  ' results returned. Max search results set at '
                  + str(self.max_results))
