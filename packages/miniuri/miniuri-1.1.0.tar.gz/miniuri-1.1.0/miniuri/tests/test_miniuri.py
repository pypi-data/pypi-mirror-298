from unittest import TestCase
from ..miniuri import Uri


class TestMiniUri(TestCase):
    def setUp(self):
        # "http://www.foxhop.net/samsung/HL-T5087SA/red-LED-failure"
        self.u = Uri("https://fox:pass@www.foxhop.net:81/path/filename.jpg?p=2#5")

    def test_uri(self):
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_scheme(self):
        self.assertEqual(self.u.scheme, "https")

    def test_authority(self):
        self.assertEqual(self.u.authority, "fox:pass@www.foxhop.net:81")

    def test_userinfo(self):
        self.assertEqual(self.u.userinfo, "fox:pass")

    def test_username(self):
        self.assertEqual(self.u.username, "fox")

    def test_password(self):
        self.assertEqual(self.u.password, "pass")

    def test_hostname(self):
        self.assertEqual(self.u.hostname, "www.foxhop.net")

    def test_port(self):
        self.assertEqual(self.u.port, "81")

    def test_path(self):
        self.assertEqual(self.u.path, "/path/filename.jpg")

    def test_filename(self):
        self.assertEqual(self.u.filename, "filename.jpg")

    def test_extension(self):
        self.assertEqual(self.u.extension, "jpg")

    def test_query(self):
        self.assertEqual(self.u.query, "p=2")

    def test_fragment(self):
        self.assertEqual(self.u.fragment, "5")

    # Test edge case URIs

    def test_uri_no_path(self):
        self.u = Uri("https://fox:pass@www.foxhop.net:81?p=2#5")
        self.assertEqual(self.u.uri, "https://fox:pass@www.foxhop.net:81?p=2#5")
        self.assertEqual(self.u.username, "fox")
        self.assertEqual(self.u.password, "pass")
        self.assertEqual(self.u.hostname, "www.foxhop.net")
        self.assertEqual(self.u.port, "81")
        self.assertIsNone(self.u.path)
        self.assertIsNone(self.u.filename)
        self.assertIsNone(self.u.extension)

    def test_uri_filename_only_path(self):
        self.u = Uri("https://fox:pass@www.foxhop.net:81/filename.jpg?p=2#5")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/filename.jpg?p=2#5"
        )
        self.assertEqual(self.u.username, "fox")
        self.assertEqual(self.u.password, "pass")
        self.assertEqual(self.u.hostname, "www.foxhop.net")
        self.assertEqual(self.u.port, "81")
        self.assertEqual(self.u.path, "/filename.jpg")
        self.assertEqual(self.u.filename, "filename.jpg")
        self.assertEqual(self.u.extension, "jpg")

    def test_uri_trailing_slash_only_path(self):
        self.u = Uri("https://fox:pass@www.foxhop.net:81/?p=2#5")
        self.assertEqual(self.u.path, "/")
        self.assertEqual(self.u.uri, "https://fox:pass@www.foxhop.net:81/?p=2#5")

    # Test change attributes:

    def test_change_uri(self):
        self.u.uri = "http://zell:sapp@wwws.foxhop.net:82/my/file.png?p=3#6"
        self.assertEqual(
            self.u.uri, "http://zell:sapp@wwws.foxhop.net:82/my/file.png?p=3#6"
        )

    def test_change_scheme(self):
        self.u.scheme = "http"
        self.assertEqual(self.u.scheme, "http")
        self.assertEqual(
            self.u.uri, "http://fox:pass@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_change_authority(self):
        self.u.authority = "zell:ssap@wwws.foxhop.net:82"
        self.assertEqual(self.u.authority, "zell:ssap@wwws.foxhop.net:82")
        self.assertEqual(
            self.u.uri, "https://zell:ssap@wwws.foxhop.net:82/path/filename.jpg?p=2#5"
        )

    def test_change_userinfo(self):
        self.u.userinfo = "zell:ssap"
        self.assertEqual(self.u.userinfo, "zell:ssap")
        self.assertEqual(
            self.u.uri, "https://zell:ssap@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )
        self.u.userinfo = "zell"
        self.assertEqual(self.u.userinfo, "zell")
        self.assertEqual(
            self.u.uri, "https://zell@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_change_username(self):
        self.u.username = "zell"
        self.assertEqual(self.u.username, "zell")
        self.assertEqual(
            self.u.uri, "https://zell:pass@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_change_password(self):
        self.u.password = "ssap"
        self.assertEqual(self.u.password, "ssap")
        self.assertEqual(
            self.u.uri, "https://fox:ssap@www.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_change_hostname(self):
        self.u.hostname = "wwws.foxhop.net"
        self.assertEqual(self.u.hostname, "wwws.foxhop.net")
        self.assertEqual(
            self.u.uri, "https://fox:pass@wwws.foxhop.net:81/path/filename.jpg?p=2#5"
        )

    def test_change_port(self):
        self.u.port = "82"
        self.assertEqual(self.u.port, "82")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:82/path/filename.jpg?p=2#5"
        )

    def test_change_path(self):
        self.u.path = "/my/file.png"
        self.assertEqual(self.u.path, "/my/file.png")
        self.assertEqual(self.u.filename, "file.png")
        self.assertEqual(self.u.extension, "png")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/my/file.png?p=2#5"
        )

    def test_change_filename(self):
        self.u.filename = "file.png"
        self.assertEqual(self.u.filename, "file.png")
        self.assertEqual(self.u.extension, "png")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/path/file.png?p=2#5"
        )

    def test_change_extension(self):
        self.u.extension = "png"
        self.assertEqual(self.u.filename, "filename.png")
        self.assertEqual(self.u.extension, "png")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/path/filename.png?p=2#5"
        )

    def test_change_query(self):
        self.u.query = "p=3"
        self.assertEqual(self.u.query, "p=3")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/path/filename.jpg?p=3#5"
        )

    def test_change_fragment(self):
        self.u.fragment = "6"
        self.assertEqual(self.u.fragment, "6")
        self.assertEqual(
            self.u.uri, "https://fox:pass@www.foxhop.net:81/path/filename.jpg?p=2#6"
        )

    def test_relative_uri(self):
        self.assertEqual(self.u.relative_uri, "/path/filename.jpg?p=2#5")

    def test_only_relative_uri(self):
        u = Uri("/about.html")
        self.assertEqual(u.relative_uri, "/about.html")
        self.assertEqual(u.filename, "about.html")
        self.assertEqual(u.extension, "html")
        self.assertIsNone(u.fragment)
        self.assertIsNone(u.hostname)
        self.assertIsNone(u.scheme)
        self.assertIsNone(u.authority)

    def test_empty_uri_sets_attrs_to_none(self):
        self.u.uri = ""
        self.assertEqual(self.u.uri, "")
        self.assertIsNone(self.u.scheme)
        self.assertIsNone(self.u.username)
        self.assertIsNone(self.u.password)
        self.assertIsNone(self.u.hostname)
        self.assertIsNone(self.u.port)
        self.assertIsNone(self.u.path)
        self.assertIsNone(self.u.filename)
        self.assertIsNone(self.u.query)
        self.assertIsNone(self.u.fragment)
        self.assertIsNone(self.u.extension)
        self.assertIsNone(self.u.authority)

    def test_empty_uri_sets_attrs_to_none2(self):
        # Same as above but tests the constructor.
        self.u = Uri("")
        self.assertEqual(self.u.uri, "")
        self.assertIsNone(self.u.scheme)
        self.assertIsNone(self.u.username)
        self.assertIsNone(self.u.password)
        self.assertIsNone(self.u.hostname)
        self.assertIsNone(self.u.port)
        self.assertIsNone(self.u.path)
        self.assertIsNone(self.u.filename)
        self.assertIsNone(self.u.query)
        self.assertIsNone(self.u.fragment)
        self.assertIsNone(self.u.extension)
        self.assertIsNone(self.u.authority)

    def test_none_uri_sets_attrs_to_none(self):
        self.u.uri = None
        self.assertEqual(self.u.uri, "")
        self.assertIsNone(self.u.scheme)
        self.assertIsNone(self.u.username)
        self.assertIsNone(self.u.password)
        self.assertIsNone(self.u.hostname)
        self.assertIsNone(self.u.port)
        self.assertIsNone(self.u.path)
        self.assertIsNone(self.u.filename)
        self.assertIsNone(self.u.query)
        self.assertIsNone(self.u.fragment)
        self.assertIsNone(self.u.extension)
        self.assertIsNone(self.u.authority)

    def test_none_uri_sets_attrs_to_none2(self):
        # Same as above but tests the constructor.
        self.u = Uri(None)
        self.assertEqual(self.u.uri, "")
        self.assertIsNone(self.u.scheme)
        self.assertIsNone(self.u.username)
        self.assertIsNone(self.u.password)
        self.assertIsNone(self.u.hostname)
        self.assertIsNone(self.u.port)
        self.assertIsNone(self.u.path)
        self.assertIsNone(self.u.filename)
        self.assertIsNone(self.u.query)
        self.assertIsNone(self.u.fragment)
        self.assertIsNone(self.u.extension)
        self.assertIsNone(self.u.authority)

    def test_ssm_uri(self):
        self.u = Uri("ssm:///path/to/my/parameter")
        self.assertEqual(self.u.uri, "ssm:///path/to/my/parameter")
        self.assertEqual(self.u.scheme, "ssm")
        self.assertIsNone(self.u.username)
        self.assertIsNone(self.u.password)
        self.assertIsNone(self.u.hostname)
        self.assertIsNone(self.u.port)
        self.assertEqual(self.u.path, "/path/to/my/parameter")
        self.assertEqual(self.u.filename, "parameter")
        self.assertIsNone(self.u.query)
        self.assertIsNone(self.u.fragment)
        self.assertIsNone(self.u.extension)
        self.assertIsNone(self.u.authority)

    # New tests for additional edge cases

    def test_no_scheme(self):
        u = Uri("//www.example.com/path")
        self.assertIsNone(u.scheme)
        self.assertEqual(u.authority, "www.example.com")
        self.assertEqual(u.path, "/path")
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    def test_no_authority(self):
        u = Uri("/path/to/resource")
        self.assertIsNone(u.scheme)
        self.assertIsNone(u.authority)
        self.assertEqual(u.path, "/path/to/resource")
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    def test_no_path(self):
        u = Uri("http://hostname")
        self.assertEqual(u.scheme, "http")
        self.assertEqual(u.authority, "hostname")
        self.assertIsNone(u.path)
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    def test_no_query_or_fragment(self):
        u = Uri("http://hostname/path")
        self.assertEqual(u.scheme, "http")
        self.assertEqual(u.authority, "hostname")
        self.assertEqual(u.path, "/path")
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    def test_unicode_handling(self):
        u = Uri("http://hostname/路径")
        self.assertEqual(u.scheme, "http")
        self.assertEqual(u.authority, "hostname")
        self.assertEqual(u.path, "/路径")
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    # Test for invalid inputs
    def test_invalid_uri(self):
        u = Uri("http://:80")
        self.assertEqual(u.scheme, "http")
        self.assertIsNone(u.username)
        self.assertIsNone(u.password)
        self.assertIsNone(u.hostname)
        self.assertEqual(u.port, "80")
        self.assertIsNone(u.path)
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)

    def test_malformed_uri(self):
        u = Uri("http://user@:80")
        self.assertEqual(u.scheme, "http")
        self.assertEqual(u.username, "user")
        self.assertIsNone(u.password)
        self.assertIsNone(u.hostname)
        self.assertEqual(u.port, "80")
        self.assertIsNone(u.path)
        self.assertIsNone(u.query)
        self.assertIsNone(u.fragment)
