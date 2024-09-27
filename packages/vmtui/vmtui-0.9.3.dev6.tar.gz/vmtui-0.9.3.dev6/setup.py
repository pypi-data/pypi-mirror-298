from setuptools import setup, find_packages

setup(setup_requires=["pbr"],
      pbr=True,
      include_package_data=True,
      package_dir={"":"src"},
      entry_points={'console_scripts': ['vmtui=vmtui.vmtui:main', 'gen_libvirt_polkit_acl=vmtui.gen_libvirt_polkit_acl:main']})
