+++
author = "Brian Pfeil"
categories = ["Shell", "playground"]
date = 2018-09-21
description = ""
summary = " "
draft = false
slug = "v8-javascript-engine"
tags = ["v8",]
title = "V8 JavaScript Engine"
repoFullName = "pfeilbr/v8-javascript-engine-playground"
repoHTMLURL = "https://github.com/pfeilbr/v8-javascript-engine-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/v8-javascript-engine-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/v8-javascript-engine-playground</a>
</div>


project to learn and develop with [V8](https://developers.google.com/v8/)

> Root V8 source directory is @ `~/dev/v8` on local machine

## Build Source and Sample(s)

1. Follow steps at https://github.com/v8/v8/wiki/Building-from-Source up until, but not inlcuding `tools/dev/v8gen.py ...`
2. generate "debug" build files `tools/dev/v8gen.py x64.debug`
3. change contents of `v8/out.gn/x64.debug/args.gn` to
    ```
    is_debug = true
    target_cpu = "x64"
    v8_enable_backtrace = true
    v8_enable_slow_dchecks = true
    v8_optimized_debug = false
    v8_monolithic = true
    v8_use_external_startup_data = false
    is_component_build = false
    ```
    > needed to enable debugging
4. compile with `ninja -C out.gn/x64.debug`
5. compile debug version of `samples/hello-world.cc` with
    ```
    g++ -g -I. -Iinclude samples/hello-world.cc -o out.gn/x64.debug/hello_world -lv8 -lv8_libbase -lv8_libplatform -licuuc -licui18n -Lout.gn/x64.debug/ -pthread -std=c++0x
    ```
    > `-g` enables debug version
6. move into output directory `pushd out.gn/x64.debug`
7. set library path and run `LD_LIBRARY_PATH=./ ./hello_world`
8. return to v8 root `popd`

---

## Developing

1. configure: modify `script/env` for your setup
2. build: `./scripts/build src/playground.cc`
3. run: `./scripts/run src/playground.cc`
4. build and run on change (dev): `./scripts/build-and-run-on-change src/playground.cc`
    ![](https://www.evernote.com/l/AAEUVIkQELlEW4GZtid7LUwHMnwJbAyyDywB/image.png)

---

## vscode debugging

### `launch.json` configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(lldb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/out.gn/x64.debug/hello_world",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}/out.gn/x64.debug",
            "environment": [{"name": "LD_LIBRARY_PATH", "value": "./"}],
            "externalConsole": true,
            "MIMode": "lldb"
        }
    ]
}
```

> `${workspaceFolder}` is `v8` root directory

![](https://www.evernote.com/l/AAHCxYreY3BNyI56b_VU9HUCWfwMfOt8BsYB/image.png)




