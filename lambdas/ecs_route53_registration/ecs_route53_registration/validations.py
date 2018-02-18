from builtins import ValueError


def ensure_present(value, absent_message):
    if not value or value == '':
        raise ValueError(absent_message)

    return value


def ensure_one_of(values, value, failure_message):
    if value not in values:
        raise ValueError(failure_message % values)

    return value
