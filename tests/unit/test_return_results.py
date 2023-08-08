from python_library import Sample


def test_random_computations_have_results():
    """
    test if the random copmutations results is not None
    """
    sample = Sample()
    result = sample.sample_compute()

    assert result is not None


def test_random_computations_integer_results():
    """
    test if the random computation result is integer
    """
    sample = Sample()
    result = sample.sample_compute()

    assert type(result) is int
