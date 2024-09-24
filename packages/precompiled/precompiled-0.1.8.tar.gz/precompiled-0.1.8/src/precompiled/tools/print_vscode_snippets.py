import json

if __name__ == '__main__':
    code = """
from precompiled.all import *
@dataclass
class Args:
    $1: $2 
    $3: $4
    // add


@dataclass
class LTestCase:
    name: str
    args: Args
    want: $5  # replace


class TestSolution(TestCase):
    # replace name
    def test_$6(self):
        cases: list[LTestCase] = [
            # add args
            LTestCase("1", Args(), ),
            # LTestCase("2", Args(), ),
            # LTestCase("3", Args(), ),
        ]
        s = Solution()
        for case in cases:
            with self.subTest(case=case.name):
                # may be replace func name
                self.assertEqual(s.$6(**case.args.__dict__), case.want)
"""
    code_lines = code.split("\n")
    code_json = json.dumps(code_lines)
    print(code_json)
