from sodapy import Socrata
from os import mkdir, path
from csv import writer
from requests import get, HTTPError
from re import compile, sub, findall, search
from math import ceil
from threading import Thread
from queue import Queue
from json import dump
from zipfile import ZipFile, BadZipfile
from io import BytesIO


def main():
    path = r'D:\OpenCalgary_2020_11_22_8'

    data_downloader = DataDownloader(path)
    data_downloader.download()


class DataDownloader:
    PATH_REGEX = compile(r'[/\\]')
    ENTRIES_COUNT_REGEX = compile('([0-9]+)(?= results)')
    DOMAIN = 'data.calgary.ca'
    TOKEN = 'PWKgj81HB93VmNbc4I3GvcwNr'

    def __init__(self, directory_path):
        self.PATH = path.abspath(directory_path)
        self.data_set_identifiers = []
        self.log = {}
        self.number_of_data_sets = 0

    def download(self):
        self._create_directory()

        client = Socrata(self.DOMAIN, self.TOKEN)

        print('Getting data set identifiers')

        self._get_data_set_identifiers()
        self.number_of_data_sets = len(self.data_set_identifiers)

        print('{} data sets found'.format(self.number_of_data_sets))

        for index, data_set_identifier in enumerate(self.data_set_identifiers):
            print('{}/{} Getting data set "{}"'.format((index + 1), self.number_of_data_sets, data_set_identifier))

            self.log[data_set_identifier] = {}

            metadata = client.get_metadata(data_set_identifier)

            sanitized_name = sub(self.PATH_REGEX, '', metadata['name'])
            sanitized_name = sub(r"[-:%]", " ", sanitized_name)
            directory_name = sub(r"[-:%]", "", sanitized_name) + ' ({})'.format(data_set_identifier)
            directory_path = path.join(self.PATH, directory_name)

            if not path.exists(directory_path):
                mkdir(directory_path)

            file_path = path.join(directory_path, 'metadata.json')

            with open(file_path, 'w') as output_metadata:
                dump(metadata, output_metadata)

            # Get CSV if available
            try:
                csv_file = client.get(data_set_identifier, 'csv')

                file_name = sanitized_name + '.csv'
                file_path = path.join(directory_path, file_name)

                with open(file_path, 'w', newline='') as output_json:
                    csv_writer = writer(output_json)

                    for row in csv_file:
                        try:
                            csv_writer.writerow(row)
                        except UnicodeEncodeError:
                            csv_writer.writerow(['Error'])

                self.log[data_set_identifier]['csv'] = True
            except HTTPError:
                self.log[data_set_identifier]['csv'] = False

            # Get JSON if available
            try:
                json_file = client.get(data_set_identifier, 'json')

                file_name = sanitized_name + '.json'
                file_path = path.join(directory_path, file_name)

                with open(file_path, 'w') as output_json:
                    dump(json_file, output_json)

                self.log[data_set_identifier]['json'] = True
            except HTTPError:
                self.log[data_set_identifier]['json'] = False

            # Get shapefiles if available
            try:
                shapefile_url = 'https://data.calgary.ca/api/geospatial/{}?method=export&format=Shapefile'.format(
                    data_set_identifier)
                shapefile = get(shapefile_url, stream=True)

                shapefile_zip = ZipFile(BytesIO(shapefile.content))

                file_name = sanitized_name + ' (shapefiles)'
                file_path = path.join(directory_path, file_name)

                if not path.exists(file_path):
                    mkdir(file_path)

                shapefile_zip.extractall(path=file_path)

                self.log[data_set_identifier]['shapefile'] = True
            except (HTTPError, BadZipfile):
                self.log[data_set_identifier]['shapefile'] = False

            # Get .xls if available
            try:
                xls_url = 'https://data.calgary.ca/download/{}/application%2Fvnd.ms-office'.format(
                    data_set_identifier)
                xls_file = get(xls_url, stream=True)

                if xls_file.ok:
                    file_name = sanitized_name + '.xls'
                    file_path = path.join(directory_path, file_name)

                    with open(file_path, 'wb') as output_xls:
                        output_xls.write(xls_file.content)

                    self.log[data_set_identifier]['csv'] = True
                else:
                    self.log[data_set_identifier]['shapefile'] = False
            except (HTTPError, BadZipfile):
                self.log[data_set_identifier]['shapefile'] = False

    def _create_directory(self):
        if not path.exists(self.PATH):
            mkdir(self.PATH)

    def _get_data_set_identifiers(self):
        data_sets_search = get('https://data.calgary.ca/browse?&page=1').text
        entries_count = int(search(self.ENTRIES_COUNT_REGEX, data_sets_search).group())

        number_of_pages = int(ceil(entries_count / 10.0))

        queue = Queue()

        threads = []
        for i in range(1, (number_of_pages + 1)):
            link = 'https://data.calgary.ca/browse?&page={}'.format(i)
            identifier_scraper = self.IdentifierScraper(queue, link)
            threads.append(identifier_scraper)
            identifier_scraper.start()

        for thread in threads:
            thread.join()

        all_identifiers = []
        for i in range(1, (number_of_pages + 1)):
            all_identifiers += queue.get(block=False)

        self.data_set_identifiers = set(all_identifiers)

    class IdentifierScraper(Thread):
        ENTRIES_REGEX = compile('(?<=/)([0-9a-z]{4}-[0-9a-z]{4})(?=")')

        def __init__(self, queue, link):
            Thread.__init__(self)
            self.queue = queue
            self.link = link

        def run(self):
            page = get(self.link).text
            results = findall(self.ENTRIES_REGEX, page)

            identifiers = []
            if results:
                for result in results:
                    identifiers.append(result)

            self.queue.put(identifiers)
            self.queue.task_done()


if __name__ == '__main__':
    main()
