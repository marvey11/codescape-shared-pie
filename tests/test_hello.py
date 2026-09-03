from codescape.shared import hello


def test_hello() -> None:
    assert hello() == "Hello from codescape-shared-pie!"
