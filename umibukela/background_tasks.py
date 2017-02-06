from background_task import background
from os import makedirs, path, walk
from tempfile import mkdtemp, NamedTemporaryFile
import re
import requests
import shutil
from zipfile import ZipFile
from django.core.files import File
from models import Cycle


@background(schedule=60)
def create_zip(cycle_id, artifacts):
    tmpdir = mkdtemp()
    try:
        to_archive = []
        for artifact in artifacts:
            archive_dir = artifact['dir']
            localdir = path.join(tmpdir, archive_dir)
            if not path.isdir(localdir):
                makedirs(localdir)
            r = requests.get(artifact['url'], stream=True)
            d = r.headers['content-disposition']
            filename = re.findall("filename=\"(.+)\"", d)[0]
            local_filename = path.join(localdir, filename)
            archive_filename = path.join(archive_dir, filename)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            to_archive.append({
                'local_filename': local_filename,
                'archive_filename': archive_filename,
            })
        ziptmpdir = mkdtemp()
        try:
            with NamedTemporaryFile(dir=ziptmpdir, delete=False) as zfh:
                with ZipFile(zfh, 'w') as zf:
                    for file in to_archive:
                        zf.write(file['local_filename'], file['archive_filename'])
                cycle = Cycle.objects.get(id=cycle_id)
                cycle.materials.save('cycle-materials.zip', File(zfh))
        finally:
            shutil.rmtree(ziptmpdir)
    finally:
        shutil.rmtree(tmpdir)
