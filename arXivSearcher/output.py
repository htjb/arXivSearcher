import smtplib
import imapclient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import sys

class output_type():
    def __init__(self, type, finds, search, max_results):
        self.type = type
        self.finds = finds

        if self.type == 'print' or self.type == 'txt':
            if self.type == 'txt':
                sys.stdout = open('arXiv_search_' +
                                  '_'.join(search.split(' ')) + '.txt', 'w')
            print('arXivSearcher results for \"' + search + '\":\n')
            if self.type == 'print':
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
                  + str(max_results))
            if self.type == 'txt':
                sys.stdout.close()

        if self.type == 'email':

            email = input('Enter your email address: ')
            password = getpass.getpass('Enter your password: ')

            s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
            s.starttls()
            s.login(email, password)

            msg = MIMEMultipart()

            msg['From'] = email
            msg['To'] = email
            msg['Subject']= 'arXivSearcher results for \"' + search + '\"'

            parts = []
            preamble = 'arXivSearcher results for \"' + search + '\":\n\n'
            count = 0
            for i in range(len(self.finds)):
                if 'title' in self.finds[i]:
                    parts.append(
                        '~'*100 + '\n' +
                        'TITLE: ' + str(self.finds[i]['title']) + '\n\n' +
                        'URL: ' + str(self.finds[i]['id']) + '\n\n' +
                        'UPDATED: ' + str(self.finds[i]['update_date']) +
                        ', PUBLISHED: ' +
                        str(self.finds[i]['published_date']) + '\n\n' +
                        'AUTHORS: ' + ', '.join([
                            self.finds[i]['author_' + str(j)]
                            for j in range(self.finds[i]['authors_len'])]) +
                        '\n\n' +
                        'ABSTRACT: ' + str(self.finds[i]['abstract']))
                    count += 1
            preamble += str(count) + \
                ' results returned. Max search results set at ' + \
                str(max_results) + '\n\n'
            msg.attach(MIMEText(preamble + '\n'.join(parts),'plain'))
            s.send_message(msg)
            s.quit()
            del msg

            box = imapclient.IMAPClient('imap-mail.outlook.com', ssl=True)
            box.login(email, password)
            box.select_folder('Sent Items')
            IDs = box.search('SUBJECT "arXivSearcher results for"')
            box.delete_messages(IDs)
            box.expunge()
            box.logout()
