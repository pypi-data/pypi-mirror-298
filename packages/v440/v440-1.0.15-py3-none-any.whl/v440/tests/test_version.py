import operator
import unittest

import packaging.version

from v440 import Version, VersionError

VERSION_STRINGS = [
    # Basic Versioning
    "1.0.0",
    "0.9.1",
    "2.1.0",
    "10.5.3",
    "0.0.1",
    "0.0.0",
    "0.1",
    "1.2",
    "2.4",
    # Pre-releases (alpha, beta, release candidate)
    "1.0.0a1",
    "2.0b3",
    "0.9.1rc4",
    "1.1.0-alpha",
    "3.0.0b2",
    "4.1.0-rc.1",
    "1.1a0",
    "1.1.0-alpha.2",
    "5.0rc1",
    # Post-releases
    "1.0.0.post1",
    "2.1.0.post4",
    "3.2.1.post7",
    "1.2.post.3",
    "1.2.0-post4",
    "0.9.0post5",
    # Development releases
    "1.0.0.dev1",
    "2.0.0.dev2",
    "0.9.1.dev10",
    "2.1.dev0",
    "1.0dev5",
    "1.1.0-dev3",
    "0.5.0.dev4",
    # Local Versions
    "1.0.0+local",
    "2.0.1+20130313144700",
    "1.0.0+exp.sha.5114f85",
    "1.0.0+abc.5.1",
    "1.0.1+2019.10.22",
    "0.9.0+ubuntu1",
    "2.1.0+build.12345",
    "3.2.1+dfsg1",
    # Epoch Versions
    "1!0.1.0",
    "2!1.0.0",
    "1!2.3.4",
    "0!0.0.1",
    "3!1.2.0",
    # Mixed Versions (combining post, dev, pre-releases, etc.)
    "1.0.0a1.post2",
    "2.1.0b2.dev3",
    "1.2.3rc1+build123",
    "1!1.0.0a1.dev1",
    "1.2.3.post4+exp.sha.5114f85",
    "3.2.1rc2.post1.dev3",
    "0!0.9.0.post5.dev7+local.5",
    "2!3.4.5a2+ubuntu1",
    # Edge Cases / Special Forms
    "1.0",
    "v2.0",  # Some might write v prefix in tags, though it's non-standard
    "1.2.3-456",
    "2.0.0-beta",
    "1.0.0.dev1234567",
    "1.0.0.post123456789",
    "1.2.3+abc.123",
    "1.0+deadbeef",
    "0.1+build.1",
    # Invalid or Potentially Problematic Cases (for error handling)
    "1..0",  # double dot
    "1.0.0+@build",  # invalid character
    "1.2.3-beta",  # non-PEP 440 pre-release format
    "01.0.0",  # leading zero
    "1.0.0beta1",  # invalid beta format
    "v1.2.3"  # use of v, technically non-standard
    # Increasing complexity with more combinations
    "1.0.0a1.post2.dev3",
    "1!2.0.0b3.post1+exp.sha.1234abcd",
    "1!1.0.0.dev4567.post9+20190101",
    "0.9.0.post99.dev1000+ubuntu12.04.5",
    "3!2.1.0-alpha.5+build.34567abcd",
    "1.2.3a1.post11.dev7+sha256.abc123def456",
    "0!0.0.0a1.post9999.dev8888+local-build.0",
    "42!1.0.0rc999.post999.dev9999+exp.build.local1",
    # Combining epochs with local versions
    "2!1.0.0+local.version.1234",
    "1!2.0.1.post3.dev1+local.hash.deadbeef",
    "3!4.5.6a2.post8.dev9+build.sha.abcdef123456",
    # Advanced pre-release + post-release + development combinations
    "0.1a1.post2.dev0+local.build.1234abc",
    "2!5.6.7b5.post10.dev1000+exp.sha12345678",
    "1.0.0b99.post8888.dev7777+local.version.abcdef",
    "0.5.0rc1.post1111.dev987+local.build.exp123",
    "0!1.1a1.post1.dev100+local.build.hash99999",
    # Very large versions with long numeric parts
    "1.0.0.post999999.dev9999999+build.1234567890",
    "0!99999999.99999.99999+local.version.9876543210",
    "100!0.0.0a0.post0.dev0+exp.sha.0",
    "2!999.999.999a999.post9999.dev9999+local.build.9",
    # Complex strings with multiple epochs, large numbers, and combinations
    "10!9999.8888.7777a6666.post5555.dev4444+build.hash123abc",
    "1!1.1a1000000000.post1000000000.dev1000000000+local.0",
    # Mixed use of pre-release and post-release with complex local versions
    "1.0.0a1.post2+ubuntu16.04",
    "2.0.0-rc.1.post2+build.sha.e91e63f0",
    "1.0.0-alpha+linux-x86_64",
    "0.1.0-beta+20190506.commit.gdeadbeef",
    # Invalid cases (testing error handling for extreme cases)
    "0.0.0a1.post0.dev0+local.build.invalid_character#",
    "1.0.0-alpha_1",  # invalid separator
    "1.0.0a1..post2",  # double dot
    "1!2.0.0+",  # trailing plus sign
    "v1.0.0.post0.dev0",  # 'v' prefix with multiple post/dev releases
    "1.0.0.a1",  # invalid pre-release format
    "2!1..0",  # double dot with epoch
    "1.0.0++local.version.doubleplus",  # double plus in local version
    "1.2.3alpha1.post2",  # invalid pre-release format
    "00!1.0.0",  # invalid epoch with leading zero
    "1.0.0a01.post00.dev01+build00",  # invalid leading zeros
    "1.0.0+build@sha.123",  # invalid character in local version
    "v1.0.0-0",  # invalid pre-release number
    "1.0.0alpha_beta",  # invalid underscore in pre-release
    "1.0.0...dev",  # triple dots
    # Extreme cases with very long versions
    "0.1.0a12345678901234567890.post12345678901234567890.dev12345678901234567890+build12345678901234567890",
    "1.2.3+local.version.with.extremely.long.identifier.123456789012345678901234567890",
    "0!0.0.0a9999999999999.post9999999999999.dev9999999999999+build.sha.9999999999999",
    # Cases with inconsistent pre-release and post-release ordering
    "1.0.0.post1a1",  # post before alpha (invalid)
    "1.0.0.dev1rc1",  # dev before rc (invalid)
    "2!1.0.0rc1.post1a1",  # rc and post combined in wrong order (invalid)
    "3!1.0.0a1.dev1rc1+build123",  # rc after dev (invalid)
]


class TestExample(unittest.TestCase):

    def test_example_1(self):
        v = Version("v1.0.0")
        self.assertEqual(str(v), "1")  # Initial version
        self.assertEqual(v.format("3"), "1.0.0")  # Initial version formatted

    def test_example_2(self):
        v = Version("2.5.3")
        self.assertEqual(str(v), "2.5.3")  # Modified version
        v.release[1] = 64
        v.release.micro = 4
        self.assertEqual(str(v), "2.64.4")  # Further modified version

    def test_example_3(self):
        v1 = Version("1.6.3")
        v2 = Version("1.6.4")
        self.assertEqual(str(v1), "1.6.3")  # v1
        self.assertEqual(str(v2), "1.6.4")  # v2
        self.assertFalse(v1 == v2)  # v1 == v2 gives False
        self.assertTrue(v1 != v2)  # v1 != v2 gives True
        self.assertFalse(v1 >= v2)  # v1 >= v2 gives False
        self.assertTrue(v1 <= v2)  # v1 <= v2 gives True
        self.assertFalse(v1 > v2)  # v1 > v2 gives False
        self.assertTrue(v1 < v2)  # v1 < v2 gives True

    def test_example_3a(self):
        v1 = Version("1.6.3")
        v2 = "1.6.4"
        self.assertEqual(str(v1), "1.6.3")  # v1
        self.assertEqual(str(v2), "1.6.4")  # v2
        self.assertFalse(v1 == v2)  # v1 == v2 gives False
        self.assertTrue(v1 != v2)  # v1 != v2 gives True
        self.assertFalse(v1 >= v2)  # v1 >= v2 gives False
        self.assertTrue(v1 <= v2)  # v1 <= v2 gives True
        self.assertFalse(v1 > v2)  # v1 > v2 gives False
        self.assertTrue(v1 < v2)  # v1 < v2 gives True

    def test_example_3b(self):
        v1 = "1.6.3"
        v2 = Version("1.6.4")
        self.assertEqual(str(v1), "1.6.3")  # v1
        self.assertEqual(str(v2), "1.6.4")  # v2
        self.assertFalse(v1 == v2)  # v1 == v2 gives False
        self.assertTrue(v1 != v2)  # v1 != v2 gives True
        self.assertFalse(v1 >= v2)  # v1 >= v2 gives False
        self.assertTrue(v1 <= v2)  # v1 <= v2 gives True
        self.assertFalse(v1 > v2)  # v1 > v2 gives False
        self.assertTrue(v1 < v2)  # v1 < v2 gives True

    def test_example_4(self):
        v = Version("2.5.3.9")
        self.assertEqual(str(v), "2.5.3.9")  # before sorting
        v.release.sort()
        self.assertEqual(str(v), "2.3.5.9")  # after sorting

    def test_example_5(self):
        v = Version("2.0.0-alpha.1")
        self.assertEqual(str(v), "2a1")  # Pre-release version
        v.pre = "beta.2"
        self.assertEqual(str(v), "2b2")  # Modified pre-release version
        v.pre[1] = 4
        self.assertEqual(str(v), "2b4")  # Further modified pre-release version
        v.pre.phase = "PrEvIeW"
        self.assertEqual(str(v), "2rc4")  # Even further modified pre-release version

    def test_example_6(self):
        v = Version("1.2.3")
        v.post = "post1"
        v.local = "local.7.dev"
        self.assertEqual(str(v), "1.2.3.post1+local.7.dev")  # Post-release version
        self.assertEqual(v.format("-1"), "1.2.post1+local.7.dev")  # Formatted version
        v.post = "post.2"
        self.assertEqual(str(v), "1.2.3.post2+local.7.dev")  # Modified version
        del v.post
        self.assertEqual(str(v), "1.2.3+local.7.dev")  # Modified without post
        v.post = "post", 3
        v.local.sort()
        self.assertEqual(str(v), "1.2.3.post3+dev.local.7")  # After sorting local
        v.local.append(8)
        self.assertEqual(str(v), "1.2.3.post3+dev.local.7.8")  # Modified with new local
        v.local = "3.test.19"
        self.assertEqual(str(v), "1.2.3.post3+3.test.19")  # Modified local again

    def test_example_7(self):
        v = Version("5.0.0")
        self.assertEqual(str(v), "5")  # Original version
        del v.data
        self.assertEqual(str(v), "0")  # After reset
        v.base = "4!5.0.1"
        self.assertEqual(str(v), "4!5.0.1")  # Before error
        with self.assertRaises(Exception) as context:
            v.base = "9!x"
        self.assertTrue(
            "not a valid numeral segment" in str(context.exception)
        )  # Error
        self.assertEqual(str(v), "4!5.0.1")  # After error

    def test_example_8(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        v.release.bump(index=7, amount=5)
        self.assertEqual(str(v), "1.2.3.4.5.6.7.13")  # Bumping


class TestSlicing(unittest.TestCase):
    def test_slicing_1(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        v.release[-8:15:5] = "777"
        self.assertEqual(str(v), "1.2.7.4.5.6.7.7.9.10.0.0.7")

    def test_slicing_2(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        try:
            v.release[-8:15:5] = 777
        except Exception as e:
            error = e
        else:
            error = None
        self.assertNotEqual(error, None)

    def test_slicing_3(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        v.release[3:4] = 777
        self.assertEqual(str(v), "1.2.3.777.5.6.7.8.9.10")

    def test_slicing_4(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        v.release[3:4] = "777"
        self.assertEqual(str(v), "1.2.3.7.7.7.5.6.7.8.9.10")

    def test_slicing_5(self):
        v = Version("1")
        v.release[3:4] = "777"
        self.assertEqual(str(v), "1.0.0.7.7.7")

    def test_slicing_6(self):
        v = Version("1")
        v.release[3:4] = 777
        self.assertEqual(str(v), "1.0.0.777")

    def test_slicing_7(self):
        v = Version("1.2.3.4.5.6.7.8.9.10")
        del v.release[-8:15:5]
        self.assertEqual(str(v), "1.2.4.5.6.7.9.10")


class TestPackaging(unittest.TestCase):
    def test_strings(self):

        pure = list()

        for x in VERSION_STRINGS:
            try:
                a = packaging.version.Version(x)
            except:
                continue
            else:
                pure.append(x)

        for x in pure:
            a = packaging.version.Version(x)
            b = Version(x).packaging()
            self.assertEqual(a, b, "should match packaging.version.Version")

        ops = [
            operator.eq,
            operator.ne,
            operator.gt,
            operator.ge,
            operator.le,
            operator.lt,
        ]
        for x in pure:
            a = packaging.version.Version(x)
            b = Version(x).packaging()
            for y in pure:
                c = packaging.version.Version(y)
                d = Version(y).packaging()
                for op in ops:
                    self.assertEqual(
                        op(a, c),
                        op(b, d),
                        f"{op} should match for {x!r} and {y!r}",
                    )


class TestVersionRelease(unittest.TestCase):

    def setUp(self):
        # Create a version class instance
        self.version = Version()

    def test_release_basic_assignment(self):
        # Test simple assignment of a list of non-negative integers
        self.version.release = [1, 2, 3]
        self.assertEqual(self.version.release, [1, 2, 3])

    def test_release_trailing_zeros(self):
        # Test that trailing zeros are removed
        self.version.release = [1, 2, 3, 0, 0]
        self.assertEqual(self.version.release, [1, 2, 3])

    def test_release_zero(self):
        # Test that a single zero is allowed
        self.version.release = [0]
        self.assertEqual(self.version.release, [])

    def test_release_empty_list(self):
        # Test empty list assignment
        self.version.release = []
        self.assertEqual(self.version.release, [])

    def test_release_conversion_string(self):
        # Test assignment of string that can be converted to numbers
        self.version.release = ["1", "2", "3"]
        self.assertEqual(self.version.release, [1, 2, 3])

    def test_release_conversion_mixed(self):
        # Test assignment of mixed string and integer values
        self.version.release = ["1", 2, "3"]
        self.assertEqual(self.version.release, [1, 2, 3])

    def test_release_invalid_value(self):
        # Test that invalid values raise an appropriate error
        with self.assertRaises(VersionError):
            self.version.release = ["a", 2, "3"]

    def test_major_minor_micro_aliases(self):
        # Test major, minor, and micro aliases for the first three indices
        self.version.release = [1, 2, 3]
        self.assertEqual(self.version.release.major, 1)
        self.assertEqual(self.version.release.minor, 2)
        self.assertEqual(self.version.release.micro, 3)
        self.assertEqual(self.version.release.patch, 3)  # 'patch' is an alias for micro

    def test_release_modify_aliases(self):
        # Test modifying the release via major, minor, and micro properties
        self.version.release = [1, 2, 3]
        self.version.release.major = 10
        self.version.release.minor = 20
        self.version.release.micro = 30
        self.assertEqual(self.version.release, [10, 20, 30])
        self.assertEqual(self.version.release.patch, 30)

    def test_release_with_tailing_zeros_simulation(self):
        # Test that the release can simulate arbitrary high number of tailing zeros
        self.version.release = [1, 2]
        simulated_release = self.version.release[:5]
        self.assertEqual(simulated_release, [1, 2, 0, 0, 0])

    def test_release_assignment_with_bool_conversion(self):
        # Test that boolean values get converted properly to integers
        self.version.release = [True, False, 3]
        self.assertEqual(self.version.release, [1, 0, 3])

    def test_release_empty_major(self):
        # Test that an empty release still has valid major, minor, micro values
        self.version.release = []
        self.assertEqual(self.version.release.major, 0)
        self.assertEqual(self.version.release.minor, 0)
        self.assertEqual(self.version.release.micro, 0)
        self.assertEqual(self.version.release.patch, 0)

    def test_release_modify_with_alias_increase_length(self):
        # Test that modifying an alias can extend the length of release
        self.version.release = [1]
        self.version.release.minor = 5  # This should make release [1, 5]
        self.assertEqual(self.version.release, [1, 5])
        self.version.release.micro = 3  # This should make release [1, 5, 3]
        self.assertEqual(self.version.release, [1, 5, 3])

    def test_release_modify_major_only(self):
        # Test that setting just the major property works
        self.version.release.major = 10
        self.assertEqual(self.version.release, [10])

    def test_release_modify_minor_only(self):
        # Test that setting just the minor property extends release
        self.version.release = []
        self.version.release.minor = 1
        self.assertEqual(self.version.release, [0, 1])

    def test_release_modify_micro_only(self):
        # Test that setting just the micro (patch) property extends release
        self.version.release = []
        self.version.release.micro = 1
        self.assertEqual(self.version.release, [0, 0, 1])

    def test_release_large_numbers(self):
        # Test that release can handle large integers
        self.version.release = [1000000000, 2000000000, 3000000000]
        self.assertEqual(self.version.release, [1000000000, 2000000000, 3000000000])


if __name__ == "__main__":
    unittest.main()
