import unittest

from myrrh.core.exts import registry
from hello import Hello


class BasicTests(unittest.TestCase):
    def test_basic_findall(self):
        exts = registry.Registry().findall("myrrh.core.exts:")
        self.assertIn("myrrh.core.exts:/registry", exts)
        exts = registry.Registry().findall("myrrh.core.exts:/registry")
        self.assertIn("myrrh.core.exts:/registry", exts)
        exts = registry.Registry().findall("myrrh.core.exts:/nonexistent")
        self.assertEqual([], exts)

    def test_basic_load(self):
        registry.Registry().load("myrrh.core.exts")

        self.assertIn("myrrh.core.exts:/registry", registry.Registry().loaded)

    def test_basic_extend(self):
        registry.Registry().extend("myrrh.core.exts:/hello", Hello())
        with registry.Registry().open(
            "myrrh.core.exts:/hello?=hello&myname=PyAnjel7"
        ) as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7"])

        registry.Registry().extend("myrrh.core.exts:/hello/hello2", None)
        with registry.Registry().open(
            "myrrh.core.exts:/hello/hello2?=hello&myname=PyAnjel7"
        ) as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7 from /hello2"])

        registry.Registry().extend("myrrh.core.exts:/root", registry.Root())
        registry.Registry().extend("myrrh.core.exts:/root/hello", Hello())
        registry.Registry().extend("myrrh.core.exts:/root/hello/hello2", None)
        registry.Registry().extend("myrrh.core.exts:/root/hello/hello2/hello3", None)

        with registry.Registry().open(
            "myrrh.core.exts:/root/hello?=hello&myname=PyAnjel7"
        ) as s:
            v = s.read(1)
        self.assertEqual(v, ["Hello PyAnjel7"])

        with registry.Registry().open(
            "myrrh.core.exts:/root/hello/hello2?=hello&myname=PyAnjel7"
        ) as s:
            v = s.read(1)

        self.assertEqual(v, ["Hello PyAnjel7 from /hello2"])

        with registry.Registry().open(
            "myrrh.core.exts:/root/hello/hello2/hello3?=hello&myname=PyAnjel7"
        ) as s:
            v = s.read(1)

        self.assertEqual(v, ["Hello PyAnjel7 from /hello2/hello3"])

    def test_basic_client(self):
        registry.Registry().extend("myrrh.core.exts:/hello", Hello())
        c = registry.Registry().client("myrrh.core.exts:/hello")

        with c.open() as s:
            v = s.hello("PyAnjel7")

        self.assertEqual(v, "Hello PyAnjel7")

    def test_auto_load(self):
        import urllib.request

        registry.Registry().opener = urllib.request.OpenerDirector()
        with registry.Registry().open("myrrh.core.exts:/registry?=loaded") as s:
            v = s.read(1)
        self.assertEqual(v, [["myrrh.core.exts:/registry"]])


if __name__ == "__main__":
    unittest.main()
