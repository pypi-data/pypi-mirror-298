from __future__ import absolute_import, annotations

from pathlib import Path
from unittest import mock

from pytest import CaptureFixture

from kslurm.cli.kbatch import kbatch


def test_batch_submits_testmode(capsys: CaptureFixture[str]):
    with mock.patch("subprocess.run") as subprocess:

        kbatch.cli(
            [
                "kbatch",
                "-t",
                "--account",
                "ctb-akhanf",
                "command",
            ]
        )

        out = capsys.readouterr()
        print(out)
        assert (
            "--account=ctb-akhanf --time=03:00:00 --cpus-per-task=1 --mem=4000"
            in str(out)
        )
        subprocess.assert_called_with(
            "echo '#!/bin/bash\n\ncommand' | cat", shell=True, stdout=-1, stderr=-2
        )


def test_params_can_be_altered(capsys: CaptureFixture[str]):
    with mock.patch("subprocess.run") as subprocess:
        starting_cwd = Path.cwd()

        kbatch.cli(
            [
                "kbatch",
                "1-33:11",
                "5G",
                "gpu",
                "--account",
                "some-account",
                "-j",
                "Regular",
                "./kslurm",
                "command",
            ],
        )

        out = capsys.readouterr()
        print(str(out))
        assert (
            "--account=some-account --time=2-09:11:00 --cpus-per-task=8 "
            "--mem=5000 --gres=gpu:1" in str(out)
        )
        subprocess.assert_called_with(
            "echo '#!/bin/bash\n\ncommand' | sbatch --account=some-account "
            "--time=2-09:11:00 --cpus-per-task=8 --mem=5000 --gres=gpu:1 "
            "--parsable ",
            shell=True,
            stdout=-1,
            stderr=-2,
        )
        assert Path.cwd() == starting_cwd / "kslurm"
