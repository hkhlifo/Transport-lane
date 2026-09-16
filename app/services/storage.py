transporter_quotes = {}


def save_quotes(quotes):
    transporter_quotes.clear()
    transporter_quotes.update(quotes)


def get_quotes():
    return transporter_quotes


def clear_quotes():
    transporter_quotes.clear()