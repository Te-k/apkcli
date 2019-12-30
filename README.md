# apk tool

Command line tool gathering information on APKs

## Install

## Plugins

```
usage: apk [-h] {cert,strings,manifest,frosting,info,shell,dex} ...

positional arguments:
  {cert,strings,manifest,frosting,info,shell,dex}
                        Plugins
    cert                Show the certificate
    strings             Extract strings from the DEX files
    manifest            Show the manifest
    frosting            Check if Google Play metadata (frosting) is in the APK
    info                Show the certificate
    shell               Launch ipython shell to analyze the APK file
    dex                 Extract the dex files

optional arguments:
  -h, --help            show this help message and exit
```

## License

This code is released under MIT license.
