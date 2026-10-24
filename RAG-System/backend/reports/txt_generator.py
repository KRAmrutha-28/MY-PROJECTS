# reports/txt_generator.py

def create_txt(
    report_text,
    output_path
):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report_text)

    return output_path