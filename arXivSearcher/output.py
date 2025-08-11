def output_type(finds, search, max_results):
    
    print('arXivSearcher results for \"' + search + '\":\n')

    finds = list(reversed(finds))
    for i in range(len(finds)):
        print('~'*80 + '\n' +
                'TITLE: ' + str(finds[i]['title']) + '\n\n' +
                'URL: ' + str(finds[i]['id']) + '\n\n' +
                'UPDATED: ' + str(finds[i]['update_date']) +
                ', PUBLISHED: ' + str(finds[i]['published_date']) +
                '\n\n' +
                'AUTHORS: ' + ', '.join([
                finds[i]['author_' + str(j)]
                for j in range(finds[i]['authors_len'])]) +
                '\n\n' +
                'ABSTRACT: ' + str(finds[i]['abstract']))
    print(str(len(finds)) +
            ' results returned. Max search results set at '
            + str(max_results))