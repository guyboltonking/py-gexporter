import plistlib
import os
from pathlib import Path

from objc_util import ns, NSURL


_BOOKMARKS_FILE = os.path.expanduser("~/Bookmarks.plist")


def get_bookmark_paths() -> Path:
    """Return the paths at which external folders are mapped into Pythonista"""

    if not os.path.isfile(_BOOKMARKS_FILE):
        return None

    with open(_BOOKMARKS_FILE, "rb") as in_file:
        content = plistlib.readPlist(in_file)

        if not content:
            return None

        paths = []
        for data in content:
            url = NSURL.URLByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
                ns(data.data), 1 << 8, None, None, None
            )
            if url and url.isFileURL():
                paths.append(Path(str(url.path())))

        return paths


def get_bookmark_path_for(external_folder):
    """Get the bookmark path for the named external_folder (which is the
    basename of the folder)"""

    for path in get_bookmark_paths():
        if path.name == external_folder:
            return path
    return None
