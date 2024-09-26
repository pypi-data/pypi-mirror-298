from morph_lib.api import ref, send_email

import morph
from morph import MorphGlobalContext


# morph.func is a decorator that takes in the following parameters:
# name: The identifier for the file alias. The function name will be used if not provided.
# description: The description for the function.
# output_paths: The destination paths for the output.
# output_type: The return type of the function
@morph.func(
    name="${MORPH_NAME}",
    description="${MORPH_DESCRIPTION}",
    output_paths=["_private/{name}/{now()}{ext()}"],
    output_type="json",
)
def main(context: MorphGlobalContext) -> dict:
    # The `send_email` function sends an email to the specified recipients with the attachments of the specified cells.
    send_email(
        [
            ref("${MORPH_PARENT_NAME}")
        ],  # replace `your_cell_name` with the name of the cell you want to include in the email
        ["example@email.com"],  # email recipients
        "Subject",  # email subject
        "Body",  # email body
    )

    return {"message": "ok"}
