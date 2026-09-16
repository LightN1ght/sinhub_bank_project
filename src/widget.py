from src import masks


def mask_account_card(user_account: str) -> str:
    account_type = " ".join(user_account.split()[:-1])
    account_number = user_account.split()[-1]

    if account_type == "Счет":
        masked_card = masks.get_mask_account(account_number)
    else:
        masked_card = masks.get_mask_card_number(account_number)

    return f"{account_type} {masked_card}"
