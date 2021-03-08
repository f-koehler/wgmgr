from typer import Option

config_file = Option(
    ...,
    "-c",
    "--config",
    envvar="WGMGR_CONFIG",
    help="path of the config file",
)
