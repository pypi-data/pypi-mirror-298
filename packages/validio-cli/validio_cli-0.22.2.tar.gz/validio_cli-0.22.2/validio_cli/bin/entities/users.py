import typer

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    get_client_and_config,
    output_json,
    output_text,
)

app = AsyncTyper(help="Users in the Validio platform")


@app.async_command(help="Get users")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = Identifier,
) -> None:
    vc, cfg = await get_client_and_config(config_dir)

    if identifier is not None:
        users = [
            await vc.get_user_by_resource_name(
                resource_name=identifier,
            )
        ]
    else:
        users = await vc.list_users()

    if output_format == OutputFormat.JSON:
        return output_json(users, identifier)

    return output_text(
        users,
        fields={
            "name": OutputSettings(attribute_name="resource_name"),
            "global_role": OutputSettings(reformat=lambda x: x.value),
            "status": OutputSettings(reformat=lambda x: x.value),
            "identities": OutputSettings(reformat=lambda x: len(x)),
            "age": OutputSettings(attribute_name="created_at"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
