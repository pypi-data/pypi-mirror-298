from typing import Optional

import typer
from validio_sdk import ValidioError
from validio_sdk.graphql_client.enums import Role
from validio_sdk.graphql_client.input_types import (
    NamespaceCreateInput,
    NamespaceRolesUpdateInput,
    NamespaceRoleWithId,
)

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    _single_resource_if_specified,
    get_client_and_config,
    output_json,
    output_text,
)

app = AsyncTyper(help="Namespaces used to separate resources")


@app.async_command(help="Get namespaces")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = typer.Argument(default=None, help="Namespace name"),
) -> None:
    vc, _ = await get_client_and_config(config_dir)

    namespaces = await vc.list_namespaces()
    # TODO(UI-2311): Fully support list/get/get_by_resource_name
    namespaces = _single_resource_if_specified(namespaces, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(namespaces, identifier)

    return output_text(
        namespaces,
        fields={
            "name": OutputSettings(attribute_name="id"),
        },
    )


@app.async_command(help="[red][bold]BETA[/bold][/red] Create a namespace")
async def create(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = typer.Argument(..., help="Namespace name"),
    role: Role = typer.Option(None, help="The role to assign --api-key and --member"),
    api_key: list[str] = typer.Option(
        [],
        "--api-key",
        help="API key to assign the --role. Can be specified multiple times",
    ),
    member: list[str] = typer.Option(
        [],
        "--member",
        help="Member id to assign to the --role. Can be specified multiple times",
    ),
    name: Optional[str] = None,
) -> None:
    vc, cfg = await get_client_and_config(config_dir)

    if (member or api_key) and not role:
        raise ValidioError("--role is required when specifying --member or --api-key")

    if role and not (member or api_key):
        raise ValidioError(
            "--role is specified but no --member or --api-key to assign the role"
        )

    ns_api_keys = [
        NamespaceRoleWithId(
            id=cfg.access_key,
            role=Role.ADMIN,
        )
    ]
    for ak in api_key:
        ns_api_keys.append(NamespaceRoleWithId(id=ak, role=role))

    ns_members = []
    for m in member:
        ns_members.append(NamespaceRoleWithId(id=m, role=role))

    namespaces = await vc.create_namespace(
        NamespaceCreateInput(
            id=identifier,
            name=name or identifier,
            members=ns_members,
            api_keys=ns_api_keys,
        )
    )

    if output_format == OutputFormat.JSON:
        return output_json(namespaces, identifier)

    return output_text(
        namespaces.namespace,
        fields={
            "id": None,
            "name": None,
        },
    )


@app.async_command(help="[red][bold]BETA[/bold][/red] Update a namespace")
async def update(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = typer.Argument(..., help="Namespace name"),
    role: Role = typer.Option(None, help="The role to assign --api-key and --member"),
    api_key: list[str] = typer.Option(
        [],
        "--api-key",
        help="API key to assign the --role. Can be specified multiple times",
    ),
    member: list[str] = typer.Option(
        [],
        "--member",
        help="Member id to assign to the --role. Can be specified multiple times",
    ),
) -> None:
    vc, _ = await get_client_and_config(config_dir)

    if (member or api_key) and not role:
        raise ValidioError("--role is required when specifying --member or --api-key")

    if role and not (member or api_key):
        raise ValidioError(
            "--role is specified but no --member or --api-key to assign the role"
        )

    ns_api_keys = []
    for ak in api_key:
        ns_api_keys.append(NamespaceRoleWithId(id=ak, role=role))

    ns_members = []
    for m in member:
        ns_members.append(NamespaceRoleWithId(id=m, role=role))

    namespace = await vc.get_namespace(identifier)
    if namespace is None:
        raise ValidioError(f"namespace '{identifier}' not found")

    api_keys = [
        NamespaceRoleWithId(id=x.api_key.id, role=x.role)
        for x in namespace.api_keys
        if x.api_key.id not in api_key
    ] + ns_api_keys

    members = [
        NamespaceRoleWithId(id=x.user.id, role=x.role)
        for x in namespace.members
        if x.user.id not in member
    ] + ns_members

    namespaces = await vc.update_namespace_roles(
        NamespaceRolesUpdateInput(
            namespace_id=identifier,
            members=members,
            api_keys=api_keys,
        )
    )

    if output_format == OutputFormat.JSON:
        return output_json(namespaces, identifier)

    return output_text(
        namespaces.namespace,
        fields={
            "id": None,
            "name": None,
        },
    )


@app.async_command(help="Remove a namespace")
async def remove(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    identifier: str = typer.Argument(..., help="Namespace name"),
) -> None:
    vc, _ = await get_client_and_config(config_dir)

    result = await vc.delete_namespaces(ids=[identifier])

    if output_format == OutputFormat.JSON:
        return output_json(result, identifier)

    status = "OK" if len(result.errors) == 0 else "ERROR"

    return output_text(
        {"status": status},
        fields={
            "status": OutputSettings(pass_full_object=True, reformat=lambda _: status),
        },
    )
