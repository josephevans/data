import unittest

from torcharrow import Scope, IStringColumn
import torcharrow.dtypes as dt


class TestStringColumn(unittest.TestCase):
    def setUp(self):
        self.ts = Scope({"device": "cpu"})

    def test_empty(self):
        empty = self.ts.Column(dt.string)
        self.assertTrue(isinstance(empty, IStringColumn))
        self.assertEqual(empty.dtype, dt.string)
        self.assertEqual(empty.length(), 0)
        self.assertEqual(empty.null_count(), 0)
        self.assertEqual(len(empty._data), 0)
        # self.assertEqual(len(empty._mask), 0)
        # self.assertEqual(empty._offsets[0], 0)

    def test_append_offsets(self):
        c = self.ts.Column(dt.string)
        c = c.append(["abc", "de", "", "f"])
        # self.assertEqual(list(c._offsets), [0, 3, 5, 5, 6])
        self.assertEqual(list(c), ["abc", "de", "", "f"])
        # TODO : check that error is thrown!
        # with self.assertRaises(TypeError):
        #     # TypeError: a dt.string is required (got type NoneType)
        #     c.append(None)

        c = self.ts.Column(["abc", "de", "", "f", None])
        # self.assertEqual(list(c._offsets), [0, 3, 5, 5, 6, 6])
        self.assertEqual(list(c), ["abc", "de", "", "f", None])

    # TODO add once dataframe is done..
    def test_string_split_methods(self):
        c = self.ts.Column(dt.string)
        s = ["hello.this", "is.interesting.", "this.is_24", "paradise"]
        c = c.append(s)
        self.assertEqual(
            list(c.str.split(".", 2, expand=True)),
            [
                ("hello", "this", None),
                ("is", "interesting", ""),
                ("this", "is_24", None),
                ("paradise", None, None),
            ],
        )

    def test_string_lifted_methods(self):
        c = self.ts.Column(dt.string)
        s = ["abc", "de", "", "f"]
        c = c.append(s)
        self.assertEqual(list(c.str.length()), [len(i) for i in s])
        # cat
        self.assertEqual(list(c.str.slice(0, 2)), [i[0:2] for i in s])
        # slice from

        # self.assertEqual(list(c.str.replace(0,2)), [i[0:2] for i in s])

        c = self.ts.Column(dt.string)
        s = ["hello.this", "is.interesting.", "this.is_24", "paradise"]
        c = c.append(s)

        #     # TODO needs IListColumn -- add back once List is implemented
        #     # self.assertEqual(list(c.str.split('.', 2, expand=False)), [])
        #     # expand = True needs Dataframes
        #     # -- add back once recursive imports are solved

        self.assertEqual(
            list(self.ts.Column(["1", "", "+3.0", "-4"]).str.isinteger()),
            [True, False, False, True],
        )
        self.assertEqual(
            list(self.ts.Column(["1.0", "", "+3.e12", "-4.0"]).str.isfloat()),
            [True, False, True, True],
        )

        self.assertEqual(list(self.ts.Column(["abc123"]).str.isalnum()), [True])
        self.assertEqual(list(self.ts.Column(["abc"]).str.isalnum()), [True])
        self.assertEqual(list(self.ts.Column(["abc"]).str.isascii()), [True])
        self.assertEqual(list(self.ts.Column(["abc"]).str.isdigit()), [False])
        self.assertEqual(
            list(self.ts.Column([".abc", "abc.a", "_"]).str.isidentifier()),
            [False, False, True],
        )
        self.assertEqual(list(self.ts.Column([".abc"]).str.islower()), [True])
        self.assertEqual(
            list(self.ts.Column(["+3.e12", "abc", "0"]).str.isnumeric()),
            [False, False, True],
        )
        self.assertEqual(
            list(self.ts.Column(["+3.e12", "abc"]).str.isprintable()), [True, True]
        )
        self.assertEqual(
            list(self.ts.Column(["\n", "\t", " ", "", "a"]).str.isspace()),
            [True, True, True, False, False],
        )
        self.assertEqual(
            list(self.ts.Column(["A B C", "abc", " "]).str.istitle()),
            [True, False, False],
        )
        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower"]).str.isupper()), [True, False]
        )

        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower"]).str.capitalize()),
            ["Upper", "Lower"],
        )
        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower"]).str.swapcase()), ["upper", "LOWER"]
        )
        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower"]).str.lower()), ["upper", "lower"]
        )
        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower"]).str.upper()), ["UPPER", "LOWER"]
        )
        self.assertEqual(
            list(self.ts.Column(["UPPER", "lower", "midWife"]).str.casefold()),
            ["upper", "lower", "midwife"],
        )
        #     # Todo
        #     # self.assertEqual(list(self.ts.Column(['1', '22', '33']).str.repeat(2)), [])
        self.assertEqual(
            list(
                self.ts.Column(["UPPER", "lower", "midWife"]).str.pad(
                    width=10, side="center", fillchar="_"
                )
            ),
            ["__UPPER___", "__lower___", "_midWife__"],
        )
        # ljust, rjust, center
        self.assertEqual(list(self.ts.Column(["1", "22"]).str.zfill(3)), ["001", "022"])
        self.assertEqual(
            list(self.ts.Column(s).str.translate({ord("."): ord("_")})),
            ["hello_this", "is_interesting_", "this_is_24", "paradise"],
        )

        self.assertEqual(list(self.ts.Column(s).str.count(".")), [1, 2, 1, 0])
        self.assertEqual(
            list(self.ts.Column(s).str.startswith("h")), [True, False, False, False]
        )
        self.assertEqual(
            list(self.ts.Column(s).str.endswith("this")), [True, False, False, False]
        )
        self.assertEqual(list(self.ts.Column(s).str.find("this")), [6, -1, 0, -1])
        self.assertEqual(list(self.ts.Column(s).str.rfind("this")), [6, -1, 0, -1])
        with self.assertRaises(ValueError):
            self.assertEqual(list(self.ts.Column(s).str.index("this")), [6, -1, 0, -1])
        self.assertEqual(list(self.ts.Column(s).str.rindex("i")), [8, 11, 5, 5])


if __name__ == "__main__":
    unittest.main()
