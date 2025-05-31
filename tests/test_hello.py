"""テストコード."""

from _pytest.capture import CaptureFixture

import hello


def test_main(capsys: CaptureFixture[str]) -> None:
    """メイン関数."""
    hello.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
