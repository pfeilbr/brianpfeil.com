+++
author = "Brian Pfeil"
categories = ["Java", "playground"]
date = 2017-10-29
description = ""
summary = "learning Minecraft Spigot Plugin"
draft = false
slug = "minecraft-spigot-plugin"
tags = ["minecraft","github",]
title = "Minecraft Spigot Plugin"
repoFullName = "pfeilbr/minecraft-spigot-plugin-playground"
repoHTMLURL = "https://github.com/pfeilbr/minecraft-spigot-plugin-playground"
truncated = true

+++

<!--
<a href="https://github.com/pfeilbr/minecraft-spigot-plugin-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/minecraft-spigot-plugin-playground</a>
-->


Learn plugin development for the [spigot](https://www.spigotmc.org/) minecraft server.

## Project Setup and Configuration

see [Creating a blank Spigot plugin in IntelliJIDEA](https://www.spigotmc.org/wiki/creating-a-blank-spigot-plugin-in-intellijidea/)

Add spigot.jar
![](https://www.evernote.com/l/AAHhcvybx3RKapL18y7xSp4ymKgZtUAbL84B/image.png)

Artifacts
![](https://www.evernote.com/l/AAE8M-RArFVHpoDLu6v2O_BvwzHKNoIeO90B/image.png)

Remote Debug Configuration
![](https://www.evernote.com/l/AAE21iCYOIJMoaW17bE5nbukROJw2lVRcV4B/image.png)



## Developing (hot swap/live coding)

1. launch minecraft server in debug mode
```sh
cd ./minecraft-spigot-server
./start.command
# java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar spigot-1.12.2.jar
```

2. Launch Debug confifguration in IntelliJ

![](https://www.evernote.com/l/AAFw9XSyXzpIX5t6QwLOch_j1PcMn1vmLW8B/image.png)

3. Set breakpoints, etc. in code

4. Launch minecraft and play

5. Breakpoints will be hit.

    Use Evaluate Code Fragment to explore while debugger is paused
    ![](https://www.evernote.com/l/AAGy9jk28LxLgaoP2bB-FCd4k4sGHAHOI9UB/image.png)

6. You can edit code, save, and build (cmd-F9).  It'll live apply/hot swap without stopping server.

## Resources

* <https://www.spigotmc.org/wiki/intellij-debug-your-plugin/>


