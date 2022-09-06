def commalize(amount: str) -> str:
    main_amount, *fractional_amount = amount.split(".")
    main_amount = decommalize(main_amount)
    main_amount = "{:,d}".format(int(main_amount)) if main_amount else ""
    return ".".join([main_amount] + fractional_amount)


def decommalize(amount: str) -> str:
    return amount.replace(",", "")
