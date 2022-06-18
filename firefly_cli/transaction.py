from datetime import datetime

from firefly_cli.utils import json_serial, tabulate


class Transaction:

    inline_transaction_fields = {
        "amount": True,
        "description": True,
        "source_name": True,
        "destination_name": True,
        "category_name": False,
        "budget_name": False,
    }

    def __init__(self, **kwargs):
        # Allow arguments to be comma-separated, but argparse splits by space instead
        kwargs["transaction"] = list(
            map(str.strip, " ".join(kwargs["transaction"]).split(","))
        )

        self.__dict__.update(kwargs)

    def __eq__(self, other):
        return self.to_dict(remove_none=True, include_header=False) == other.to_dict(
            remove_none=True, include_header=False
        )

    @classmethod
    def from_argparse(cls, args):
        args = vars(args)

        # Delete cmd2 arguments
        for k in list(args):
            if k.startswith("cmd2_"):
                args.pop(k)

        return cls(**args)

    def mandatory_fields_missing(self):

        mandatory_fields = [
            field
            for field, mandatory in Transaction.inline_transaction_fields.items()
            if mandatory
        ]

        not_set = []
        for field in mandatory_fields:
            if not getattr(self, field, None):
                not_set.append(field)

        return not_set

    def parse_inline_transaction_to_attributes(self):
        """Sets the object attributes if not already set by the optional arguments.
        Optional arguments always take precedence over positional, comma-separated arguments
        """

        for transaction_field, field in zip(
            self.transaction, self.inline_transaction_fields
        ):
            if not getattr(self, field, None):
                self.__setattr__(field, transaction_field)

    def to_dict(
        self,
        remove_none=False,
        include_header=True,
        api_safe=False,
        tabulate_safe=False,
    ):
        if tabulate_safe:
            remove_none = True
            api_safe = True

        d = self.__dict__

        if remove_none:
            d = {k: v for k, v in d.items() if v is not None}

        if not include_header:
            d = {k: v for k, v in d.items() if not k.startswith("header__")}

        # Do several casts to be json compatible
        if api_safe:
            for k, v in d.items():
                if isinstance(v, datetime):
                    # If tabulate_safe, then iso_format=False, so that date is in a readable format
                    d[k] = json_serial(v, iso_format=not tabulate_safe)

        # If for tabulate, each value must be a list
        if tabulate_safe:
            d = {k: [v] for k, v in d.items()}

        return d

    def get_tabulates(self):
        d = self.to_dict(tabulate_safe=True)
        d_header = {k: v for k, v in d.items() if k.startswith("header__")}
        d_body = {
            k: v
            for k, v in d.items()
            if not k.startswith("header__") and k != "transaction"
        }

        # Order d_body first with the date, then inline transaction fields and lastly all the remaining, alphabetically
        d_body = {
            **{"date": d_body["date"]},
            **{
                k: d_body[k]
                for k in Transaction.inline_transaction_fields
                if k in d_body
            },
            **{
                k: d_body[k]
                for k in sorted(d_body)
                if k not in Transaction.inline_transaction_fields
            },
        }

        tab_header = tabulate(d_header)
        tab_body = tabulate(d_body)

        return tab_header, tab_body
