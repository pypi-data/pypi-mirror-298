from iro import Iro, FGColor, Style

values_nested = (
    "Hello! I'm ",
    (
        FGColor.RED,
        Style.DOUBLY_UNDERLINE,
        "Iro!",
    ),
    " Nice to meet you!",
)
values_flatten = ("Hello! I'm ", FGColor.RED, Style.DOUBLY_UNDERLINE, "Iro!", Style.RESET, " Nice to meet you!")
print()
print(Iro(values_nested))
print(Iro(values_flatten))
print(Iro(values_flatten, collect_styles_first=False))
print()
