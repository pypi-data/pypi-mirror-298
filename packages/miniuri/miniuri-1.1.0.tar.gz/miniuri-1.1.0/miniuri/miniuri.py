from __future__ import unicode_literals


class Uri:
    """
    miniuri is a universal URI parser class.
    The parser grants access to the following attributes:

    foo://username:password@test.com:808/go/to/index.php?pet=cat&name=bam#eye
    \_/   \_______________/ \______/ \_/       \___/ \_/ \_______________/\_/
     |           |             |      |          |    |       |            |
     |       userinfo       hostname  |          |    |      query   fragment
     |    \___________________________|/\________|____|_/
     |                  |             |      |   |    |
    scheme          authority         |    path  |  extension
                                      |          |
                                     port     filename
    """

    def __init__(self, uri=None):
        self._reset_attributes()
        if uri:
            self.uri = uri

    def _reset_attributes(self):
        self.scheme = None
        self.username = None
        self.password = None
        self.hostname = None
        self.port = None
        self._path = None
        self._filename = None
        self.query = None
        self.fragment = None
        self.extension = None

    def __str__(self):
        return self.uri or ""

    @property
    def uri(self):
        """Build and return URI from attributes."""
        scheme = "{}://".format(self.scheme) if self.scheme else ""
        authority = self.authority or ""
        return "{}{}{}".format(scheme, authority, self.relative_uri)

    @uri.setter
    def uri(self, uri):
        """Parse and set all URI attributes."""
        self._reset_attributes()
        if not uri:
            return
        if "://" in uri:
            self.scheme, uri = uri.split("://", 1)
        elif uri.startswith("//"):
            uri = uri.lstrip("//")
        if "#" in uri:
            uri, self.fragment = uri.split("#", 1)
        if "?" in uri:
            uri, self.query = uri.split("?", 1)
        parts = uri.split("/", 1)
        self.authority = parts[0]
        self.path = "/" + parts[1] if len(parts) > 1 else None

    @property
    def authority(self):
        """Return an authority string from attributes."""
        if self.hostname:
            authority = ""
            if self.username:
                authority += self.username
                if self.password:
                    authority += ":{}".format(self.password)
                authority += "@"
            authority += self.hostname
            if self.port:
                authority += ":{}".format(self.port)
            return authority

    @authority.setter
    def authority(self, authority):
        """Set all the attributes that make up an authority."""
        if authority:
            self.username = self.password = self.port = None
            self.hostname = authority
            if "@" in self.hostname:
                self.userinfo, self.hostname = authority.split("@", 1)
            if ":" in self.hostname:
                self.hostname, self.port = self.hostname.split(":", 1)
            if not self.hostname:
                self.hostname = None

    @property
    def relative_uri(self):
        """Return everything that isn't part of the authority."""
        path = self.path or ""
        query = "?{}".format(self.query) if self.query else ""
        fragment = "#{}".format(self.fragment) if self.fragment else ""
        return "{}{}{}".format(path, query, fragment)

    @property
    def userinfo(self):
        """Return username:password, username, or None."""
        if self.username:
            return (
                "{}:{}".format(self.username, self.password)
                if self.password
                else self.username
            )

    @userinfo.setter
    def userinfo(self, info):
        """Set username and password."""
        self.username, self.password = (info.split(":", 1) + [None])[:2]

    @property
    def path(self):
        """Return path."""
        path = self._path or ""
        filename = self.filename or ""
        return "{}{}".format(path, filename) if path or filename else None

    @path.setter
    def path(self, new_path):
        if new_path:
            self.filename = new_path.split("/")[-1]
            self._path = new_path[: -len(self.filename)] if self.filename else new_path
        else:
            self.filename = None
            self._path = None

    @property
    def filename(self):
        """Return filename."""
        if self._filename:
            return (
                "{}.{}".format(self._filename, self.extension)
                if self.extension
                else self._filename
            )

    @filename.setter
    def filename(self, new_filename):
        if new_filename:
            parts = new_filename.rsplit(".", 1)
            self._filename = parts[0]
            self.extension = parts[1] if len(parts) > 1 else None
        else:
            self._filename = None
            self.extension = None
