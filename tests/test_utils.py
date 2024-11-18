from gitdashboard_app.utils import find_most_common_word, fetch_data


def test_find_most_common_word():
    test_string = "word1 word2 word2 word3"
    word, count = find_most_common_word(test_string)

    assert word == "word2"
    assert count == 2


def test_find_most_common_word_empty_string():
    test_string = ""
    word, count = find_most_common_word(test_string)

    assert word == ""
    assert count == 0


def test_fetch_data_with_sucess():
    URL = "https://api.github.com/users/torvalds/repos"
    response = fetch_data(URL)
    assert response.status_code == 200  # Validation of status code
    data = response.json()
    assert len(data) > 0
