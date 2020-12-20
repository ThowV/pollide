class OptionOverflowError(Exception):
    message = ''
    reason = ''

    def __init__(self, option_max, option_amount, reason):
        self.message = f'This command supports {option_max} options but {option_amount} were provided'

        self.reason = reason
