OLD_NEWS = [
    ("O-measure", "OMeasure"),
    ("P-measure", "PMeasure"),
    ("P-plus", "PPlusMeasure"),
    ("Q-measure", "QMeasure"),
    (",P", "P"),
    (",BR", "BR"),
    ("Q@", "QMeasure@"),
    ("\nP@", "\nPrecision@"),
]
def ntcireval_formatting(output):
    output = output.strip().replace(" ", "")
    for old, new in OLD_NEWS:
        output = output.replace(old, new)
    return output
