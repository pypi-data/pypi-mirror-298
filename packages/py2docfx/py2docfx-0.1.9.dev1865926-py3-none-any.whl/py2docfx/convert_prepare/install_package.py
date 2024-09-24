from py2docfx.convert_prepare.package_info import PackageInfo
import py2docfx.convert_prepare.pip_utils as pip_utils

def install_package(pkg: PackageInfo):
    package_name, options = pkg.get_install_command()
    pip_utils.install(package_name, options)
