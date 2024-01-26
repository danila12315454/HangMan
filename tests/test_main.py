from src.hangman.main import (
    MainProcess,
    Source,
    parse_word_from_local,
    parse_word_from_site,
)


def test_parse_word_from_local():
    assert isinstance(parse_word_from_local(), str)


def test_parse_word_from_site():
    assert isinstance(parse_word_from_site(), str)


def test_get_word():
    main_process = MainProcess(Source(1))
    assert isinstance(main_process.get_word(), str)
