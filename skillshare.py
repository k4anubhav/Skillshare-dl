import shutil
import requests, json, sys, re, os
from slugify import slugify


class Skillshare(object):

    def __init__(
            self,
            cookie,
            pk='BCpkADawqM2OOcM6njnM7hf9EaK6lIFlqiXB0iWjqGWUQjU7R8965xUvIQNqdQbnDTLz0IAO7E6Ir2rIbXJtFdzrGtitoee0n1XXRliD-RH9A-svuvNW9qgo3Bh34HEZjXjG4Nml4iyz3KqF',
            brightcove_account_id=3695997568001,
    ):
        self.cookie = cookie.strip().strip('"')
        # self.download_path = download_path
        self.pk = pk.strip()
        self.brightcove_account_id = brightcove_account_id
        self.pythonversion = 3 if sys.version_info >= (3, 0) else 2

    # just remove the characters which can't be used in windows file name
    def is_unicode_string(self, string):
        if (self.pythonversion == 3 and isinstance(string, str)) or (
                self.pythonversion == 2 and isinstance(string, unicode)):
            return True

        else:
            return False

    # get class id from url and sends to download_course_by_class_id
    def download_course_by_url(self, url, boolSubtitle, boolResources):
        class_id = self.course_is_url_to_id(url)

        if not class_id:
            raise Exception('Failed to parse class ID from URL')

        self.download_course_by_class_id(class_id, boolSubtitle, boolResources)

    # check is the course link is right
    def course_is_url_to_id(self, url):

        m = re.match('.*skillshare.com/classes/.*?/(\\d+)', url)
        self.classId = m.group(1)
        return m.group(1)

    # download course by giving id
    def download_course_by_class_id(self, class_id, boolSubtitle, boolResources):
        data = self.fetch_course_data_by_class_id(class_id=class_id)
        teacher_name = None

        # find teacher name
        if 'vanity_username' in data['_embedded']['teacher']:
            teacher_name = data['_embedded']['teacher']['vanity_username']

        if not teacher_name:
            teacher_name = data['_embedded']['teacher']['full_name']

        if not teacher_name:
            # self.setDetailLabel('Failed to read teacher name from data')
            print("")

        if self.is_unicode_string(teacher_name):
            teacher_name = teacher_name.encode('ascii', 'replace')

        # class title
        title = data['title']

        # ui class name change to class title
        print("ClassName : " + title)

        if self.is_unicode_string(title):
            title = title.encode('ascii', 'replace')

            # download base path
        download_path = os.getcwd()
        self.base_path = os.path.abspath(
            os.path.join(
                download_path,
                'Skillshare_Downloads',
                slugify(teacher_name),
                slugify(title)
            )
        ).rstrip('/')

        # temp path
        temp_base_path = os.path.abspath(
            os.path.join(
                self.base_path,
                slugify('temp')
            )
        ).rstrip('/')

        self.temp_base_path = temp_base_path

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        if not os.path.exists(temp_base_path):
            os.makedirs(temp_base_path)

        for u in data['_embedded']['units']['_embedded']['units']:
            for s in u['_embedded']['sessions']['_embedded']['sessions']:
                video_id = None

                if 'video_hashed_id' in s:
                    if s['video_hashed_id']:
                        video_id = s['video_hashed_id'].split(':')[1]

                    assert video_id, 'Failed to read video ID from data'

                    s_title = s['title']

                    if self.is_unicode_string(s_title):
                        s_title = s_title.encode('ascii', 'replace')

                    file_name = '{} - {}'.format(
                        str(s['index'] + 1).zfill(2),
                        slugify(s_title),
                    )

                    self.download_video(
                        fpath='{base_path}/{session}.mp4'.format(base_path=self.base_path, session=file_name),
                        video_id=video_id,
                        tpath='{t_path}/{session}.mp4'.format(t_path=temp_base_path, session=file_name),
                        boolSubtitle=boolSubtitle
                    )

        self.downloadResources(boolResources)
        print("Download Completed :D\ncheck {}".format(self.base_path))
        try:
            os.startfile(self.base_path)
        except Exception as e:
            print("")
        return ''

    # download subtitle
    def subtitleDownload(self, meta_res, fpath, tpath):
        subPath = fpath.replace(".mp4", ".vtt")

        subTPath = tpath.replace(".mp4", ".vtt")

        if os.path.exists(subPath):
            # self.setDetailLabel('Downloading {}...'.format(subPath) + '\nAlready Downloaded Skipping')
            return 0
        try:
            for x in meta_res.json()['text_tracks']:
                sub_url = x['src']
                break

            # self.setDetailLabel('Downloading sub {}...'.format(subPath))
            self.downloadToStorage(sub_url, subPath, subTPath)

        except:
            print('error on subtitle download')

    # This actually download files
    def downloadToStorage(self, url, path, tpath):
        if os.path.exists(path):
            print('Downloading {}...'.format(path) + '\n Already Downloaded Skipping')
            return 0

        with open(tpath, 'wb') as (f):
            response = requests.get(url, allow_redirects=True, stream=True)
            total_length = response.headers.get('content-length')
            file_size = 'File Size : ' + str(round(int(total_length)/1e+6)) + ' mb'

            if not total_length:
                f.write(response.content)

            else:
                dl = 0
                total_length = int(total_length)

                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %s" % ('=' * done, ' ' * (100 - done), file_size))
                    sys.stdout.flush()
        print('\n')
        shutil.move(tpath, path)

    def downloadResources(self, boolResources):
        if boolResources:
            basePath = os.path.abspath(
                os.path.join(
                    self.base_path,
                    'resources'
                )
            ).rstrip('/')

            if not os.path.exists(basePath):
                os.makedirs(basePath)

            headers = {
                'authority': 'www.skillshare.com',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'none',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '1',
                'sec-fetch-dest': 'document',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': self.cookie,
            }

            response = requests.get('https://www.skillshare.com/classes/Animate-Your-Illustrations-with-After-Effects/{}/projects'.format(self.classId), headers=headers)
            data = response.text
            if data.__contains__('"hasAttachments":true'):
                pattern = re.compile(r'attachments":\[{".+"}],"hasA')
                matches = pattern.finditer(data)
                for match in matches:
                    index = match.span()
                    freq = data[index[0]:index[1]]
                    freq = freq.strip(r'attachments":')
                    freq = freq.strip(r',"hasA')
                    print(freq)
                    RES = json.loads(freq)
                    for data in RES:
                        path = os.path.abspath(
                            os.path.join(
                                basePath,
                                data['title']
                            )
                        )

                        tpath = os.path.abspath(
                            os.path.join(
                                self.temp_base_path,
                                data['title']
                            )
                        )
                        print(path, data['size'])
                        self.downloadToStorage(data['url'], path, tpath)
                print('')
            else:
                if data.__contains__('"hasAttachments":false'):
                    print('no resources in this course')
                else:
                    print('error in resources')

    # get course data from skillshare
    def fetch_course_data_by_class_id(self, class_id):
        res = requests.get(url=('https://api.skillshare.com/classes/{}'.format(class_id)),
                           headers={
                               'Accept': 'application/vnd.skillshare.class+json;,version=0.8',
                               'User-Agent': 'Skillshare/5.3.13; Android 9.0.1',
                               'Host': 'api.skillshare.com',
                               # 'Referer': 'https://www.skillshare.com/',
                               'cookie': self.cookie,
                           }
                           )

        if res.status_code != 200:
            return 'Fetch error, code == {}'.format(res.status_code)
        return res.json()

    def download_video(self, fpath, video_id, tpath, boolSubtitle):
        meta_url = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'.format(
            account_id=(self.brightcove_account_id),
            video_id=video_id,
        )

        meta_res = requests.get(
            meta_url,
            headers={
                'Accept': 'application/json;pk={}'.format(self.pk),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69',
                'Origin': 'https://www.skillshare.com',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty'
            }
        )

        assert not meta_res.status_code != 200, 'Failed to fetch video meta'

        for x in meta_res.json()['sources']:
            if 'container' in x:
                if x['container'] == 'MP4' and 'src' in x:
                    dl_url = x['src']
                    self.downloadToStorage(dl_url, fpath, tpath)
                    break

        '''Subtitle download it takes same file path as .mp4 cause it auto replace the extension'''
        if boolSubtitle:
            self.subtitleDownload(meta_res, fpath, tpath)
