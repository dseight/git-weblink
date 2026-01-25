#!/usr/bin/env python3

import unittest
from git_weblink import (
    get_repo_url,
    get_commit_link,
    get_file_link,
    get_line_link,
    get_range_link,
)


class TestGitWeblink(unittest.TestCase):
    def test_get_repo_url(self):
        self.assertEqual(
            get_repo_url("git@github.com:git/git.git"), "https://github.com/git/git"
        )
        self.assertEqual(
            get_repo_url("https://github.com/git/git.git"), "https://github.com/git/git"
        )
        self.assertEqual(
            get_repo_url("git@github.com:torvalds/linux.git"),
            "https://github.com/torvalds/linux",
        )
        self.assertEqual(
            get_repo_url("git@github.com:torvalds/linux"),
            "https://github.com/torvalds/linux",
        )
        self.assertEqual(
            get_repo_url(
                "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git"
            ),
            # This is not a valid repo link on it's own because of the stripped ".git",
            # but this should be fixed in the host config
            "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux",
        )
        self.assertEqual(
            get_repo_url(
                "git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git"
            ),
            # This is not a valid repo link on it's own because of the stripped ".git",
            # but this should be fixed in the host config
            "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux",
        )
        self.assertEqual(
            get_repo_url("ssh://user@gerrit.googlesource.com:29418/plugins/lfs"),
            "https://gerrit.googlesource.com/plugins/lfs",
        )

    def test_get_commit_link(self):
        self.assertEqual(
            get_commit_link(
                "https://github.com",
                "fish-shell/fish-shell",
                "eb336889b7bcb88eb0e1f3dd678ae52275280186",
            ),
            "https://github.com/fish-shell/fish-shell/commit/eb336889b7bcb88eb0e1f3dd678ae52275280186",
        )
        self.assertEqual(
            get_commit_link(
                "https://gitlab.com",
                "gitlab-org/gitlab",
                "089916ca9f8d7a32dffa5ac2996ee3651bbfebe7",
            ),
            "https://gitlab.com/gitlab-org/gitlab/-/commit/089916ca9f8d7a32dffa5ac2996ee3651bbfebe7",
        )
        self.assertEqual(
            get_commit_link(
                "https://git.kernel.org",
                # Not a valid path on it's own, but valid as an internal representation
                "pub/scm/linux/kernel/git/torvalds/linux",
                "3c8ba0d61d04ced9f8d9ff93977995a9e4e96e91",
            ),
            "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3c8ba0d61d04ced9f8d9ff93977995a9e4e96e91",
        )
        self.assertEqual(
            get_commit_link(
                "https://codeberg.org",
                "forgejo/forgejo",
                "475e3471b4e8da8776fe7e66a3390c8a30c19f08",
            ),
            "https://codeberg.org/forgejo/forgejo/commit/475e3471b4e8da8776fe7e66a3390c8a30c19f08",
        )
        self.assertEqual(
            get_commit_link(
                "https://gerrit.googlesource.com",
                "plugins/lfs",
                "784f83838bfdc56b0a0e578005ce1b9e4abcfbad",
            ),
            "https://gerrit.googlesource.com/plugins/lfs/+/784f83838bfdc56b0a0e578005ce1b9e4abcfbad",
        )

    def test_get_file_link(self):
        self.assertEqual(
            get_file_link(
                "https://github.com",
                "dseight/git-weblink",
                "a89aa969116bfeebbd30a36ef3ac01c05c658e2d",
                "README.md",
            ),
            "https://github.com/dseight/git-weblink/blob/a89aa969116bfeebbd30a36ef3ac01c05c658e2d/README.md",
        )
        self.assertEqual(
            get_file_link(
                "https://gitlab.com",
                "qemu-project/qemu",
                "fea2d7a784fc3627a8aa72875f51fe7634b04b81",
                "Makefile",
            ),
            "https://gitlab.com/qemu-project/qemu/-/blob/fea2d7a784fc3627a8aa72875f51fe7634b04b81/Makefile",
        )
        self.assertEqual(
            get_file_link(
                "https://git.kernel.org",
                "pub/scm/utils/b4/b4",
                "477734000555ffc24bf873952e40367deee26f17",
                "README.rst",
            ),
            "https://git.kernel.org/pub/scm/utils/b4/b4.git/tree/README.rst?id=477734000555ffc24bf873952e40367deee26f17",
        )
        self.assertEqual(
            get_file_link(
                "https://codeberg.org",
                "forgejo/forgejo",
                "1951c51c8e087b92a981f71a7214198e1ca5ae84",
                "README.md",
            ),
            "https://codeberg.org/forgejo/forgejo/src/commit/1951c51c8e087b92a981f71a7214198e1ca5ae84/README.md",
        )
        self.assertEqual(
            get_file_link(
                "https://gerrit.googlesource.com",
                "jgit",
                "f8e960fc1097c4c3fca1df3399cd0c2139941a06",
                "README.md",
            ),
            "https://gerrit.googlesource.com/jgit/+/f8e960fc1097c4c3fca1df3399cd0c2139941a06/README.md",
        )

    def test_get_line_link(self):
        self.assertEqual(
            get_line_link(
                "https://github.com",
                "fish-shell/fish-shell",
                "2180777f735f5ffb35027cd7511f12eef2097246",
                "share/completions/meson.fish",
                107,
            ),
            "https://github.com/fish-shell/fish-shell/blob/2180777f735f5ffb35027cd7511f12eef2097246/share/completions/meson.fish#L107",
        )
        self.assertEqual(
            get_line_link(
                "https://gitlab.com",
                "inkscape/inkscape",
                "14defdf03aa0bbef3849e86e5ec3d23f5cd41884",
                "src/svg/svg-length.cpp",
                31,
            ),
            "https://gitlab.com/inkscape/inkscape/-/blob/14defdf03aa0bbef3849e86e5ec3d23f5cd41884/src/svg/svg-length.cpp#L31",
        )
        self.assertEqual(
            get_line_link(
                "https://git.kernel.org",
                # Not a valid path on it's own, but valid as an internal representation
                "pub/scm/linux/kernel/git/torvalds/linux",
                "3c8ba0d61d04ced9f8d9ff93977995a9e4e96e91",
                "include/linux/kernel.h",
                814,
            ),
            "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/linux/kernel.h?id=3c8ba0d61d04ced9f8d9ff93977995a9e4e96e91#n814",
        )
        self.assertEqual(
            get_line_link(
                "https://codeberg.org",
                "forgejo/forgejo",
                "d996dfb476e9d1028146707fdd4850d98e8555ac",
                ".editorconfig",
                27,
            ),
            "https://codeberg.org/forgejo/forgejo/src/commit/d996dfb476e9d1028146707fdd4850d98e8555ac/.editorconfig#L27",
        )

    def test_get_range_link(self):
        self.assertEqual(
            get_range_link(
                "https://github.com",
                "c-util/c-dvar",
                "9592e1f43b4abf4036948539e4e5d27c9b67acfd",
                "src/c-dvar.h",
                3,
                15,
            ),
            "https://github.com/c-util/c-dvar/blob/9592e1f43b4abf4036948539e4e5d27c9b67acfd/src/c-dvar.h#L3-L15",
        )
        self.assertEqual(
            get_range_link(
                "https://gitlab.com",
                "qemu-project/qemu",
                "fea2d7a784fc3627a8aa72875f51fe7634b04b81",
                "include/qom/object.h",
                435,
                474,
            ),
            "https://gitlab.com/qemu-project/qemu/-/blob/fea2d7a784fc3627a8aa72875f51fe7634b04b81/include/qom/object.h#L435-L474",
        )
        self.assertEqual(
            get_range_link(
                "https://codeberg.org",
                "forgejo/forgejo",
                "d996dfb476e9d1028146707fdd4850d98e8555ac",
                ".editorconfig",
                12,
                13,
            ),
            "https://codeberg.org/forgejo/forgejo/src/commit/d996dfb476e9d1028146707fdd4850d98e8555ac/.editorconfig#L12-L13",
        )


if __name__ == "__main__":
    unittest.main()
