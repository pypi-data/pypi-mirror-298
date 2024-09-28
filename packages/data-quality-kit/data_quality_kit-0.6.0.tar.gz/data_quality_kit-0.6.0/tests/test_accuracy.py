from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.accuracy import assert_that_type_value


def test_assert_that_type_value_correct():
    assert_that(assert_that_type_value(df_global, 'column1', int)).is_true()
    assert_that(assert_that_type_value(df_global, 'column3', str)).is_true()


def test_assert_that_type_value_incorrect():
    assert_that(assert_that_type_value(df_global, 'column3', int)).is_false()
    assert_that(assert_that_type_value(df_global, 'column2', str)).is_false()


def test_assert_that_type_value_in_nonexistent_column():
    error_msg = 'Column "nonexistent" not in DataFrame.'
    assert_that(assert_that_type_value).raises(ValueError).when_called_with(
        df_global, "nonexistent", int
    ).is_equal_to(error_msg)
