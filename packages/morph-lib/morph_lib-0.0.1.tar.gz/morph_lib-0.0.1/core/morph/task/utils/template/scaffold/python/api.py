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
    # This is where you write your code.
    # should return a dictionary
    return {"message": "ok"}
