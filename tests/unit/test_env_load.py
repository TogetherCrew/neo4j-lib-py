from python_library import Sample


def test_env_load():
    """
    test whether the env is loaded correctly
    """
    sample = Sample()

    env_value = sample.sample_get_env()

    assert env_value is not None
