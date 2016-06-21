from __future__ import unicode_literals
from securetrading.test import abstract_test


class Abstract_Test_StObjects(abstract_test.TestCase):

    def setUp(self):
        super(Abstract_Test_StObjects, self).setUp()
        self.class_ = None

    def test___setitem__(self):
        generic_stobject = self.class_()
        for s in ["_set_test", "_validate_testing"]:
            setattr(generic_stobject, s, self.mock_method(
                    exception=Exception("{0} called".format(s))))
            self.assertRaisesRegexp(Exception, "{0} called".format(s),
                                    generic_stobject.__setitem__,
                                    s.split("_")[-1], "VALUE")

        generic_stobject.__setitem__("newkey", "newvalue")
        self.assertEqual(generic_stobject["newkey"], "newvalue")

    def test_update(self):
        generic_stobject = self.class_()
        set_keys = []

        def test_func(key, value):
            set_keys.append(key)

        generic_stobject.__setitem__ = test_func
        set_data = {"key1": "value1",
                    "key2": "value2",
                    "key3": "value3",
                    "key4": "value4",
                    }
        generic_stobject.update(set_data)
        self.assertEqual(set_keys, list(set_data.keys()))
