from django.conf import settings
from django.core.files.storage import FileSystemStorage


class DevFileSystemStorage(FileSystemStorage):
    def size(self, name):
        if settings.FAKE_MISSING_FILE_SIZE:
            try:
                return super(DevFileSystemStorage, self).size(name)
            except OSError:
                return 1337
        else:
            return super(DevFileSystemStorage, self).size(name)
