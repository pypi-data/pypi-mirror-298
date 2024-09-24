# This is replaced during release process.
__version_suffix__ = '228'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.30.2"
KUBECTL_SHA512 = {
    "linux": "3e3a18138e0436c055322e433398d7ae375e03862cabae71b51883bb78cf969846b9968e426b816e3543c978a4af542e0b292428b00b481d7196e52cf366edbe",
    "darwin": "0ccc6091ac956e108169b282dc085a0bde956dd22d32ce53594ae5c7eac9157f118170b1240b65a918c5d3f4c9d693b492463225428c6fb51a9fb5419eb949a8",
}
STERN_VERSION = "1.30.0"
STERN_SHA256 = {
    "linux": "ea1bf1f1dddf1fd4b9971148582e88c637884ac1592dcba71838a6a42277708b",
    "darwin": "4eaf8f0d60924902a3dda1aaebb573a376137bb830f45703d7a0bd89e884494a",
}
KUBELOGIN_VERSION = "v1.30.0"
KUBELOGIN_SHA256 = {
    "linux": "3e61379ff750e7e74b64807a8003b755c9733b919a9cae0f22634bd19589b636",
    "darwin": "e63f0bd1d9c193b2f7efb6419fd7528b7f23f802247e5872ace3440706f0e530",
}
ZALANDO_AWS_CLI_VERSION = "0.5.9"
ZALANDO_AWS_CLI_SHA256 = {
    "linux": "885f1633c4882a332b10393232ee3eb6fac81e736e0c07b519acab487bb6dc63",
    "darwin": "908ed91553b6648182de6e67074f431a21a2e79a4ea45c4aa3d7084578fd5931",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
