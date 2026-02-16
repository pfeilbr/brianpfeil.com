+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2020-10-05
description = ""
summary = " "
draft = false
slug = "aws-cloud9"
tags = ["aws","cloud9"]
title = "AWS Cloud9"
repoFullName = "pfeilbr/aws-cloud9-playground"
repoHTMLURL = "https://github.com/pfeilbr/aws-cloud9-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/aws-cloud9-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/aws-cloud9-playground</a>
</div>


* learn [AWS Cloud9](https://aws.amazon.com/cloud9/)
* setup remote development environment

## Enabling SSH Connectivity

* add SSH inbound rule to Security Group
    ![](https://www.evernote.com/l/AAEY_BSM7g5PVa72gIFEevDXgdKE1E-zAdoB/image.png)
* add `~/.ssh/id_rsa.pub` to `/home/ec2-user/.ssh/authorized_keys`.  do this via Cloud9 IDE shell
    ![](https://www.evernote.com/l/AAGhf-SuVVRDtpS8fMS9lRQmHCwQSs6A1v8B/image.png)
* ssh -i ~/.ssh/id_rsa  ubuntu@dev01.brianpfeil.com


### Troubleshooting

* may need to connect via Cloud9 IDE to "wake up"/start instance due to "auto stop" of EC2 instance after
X minutes.
* May need to remote remote host in `~/.ssh/known_hosts` on client if the following error
    ```sh
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    SHA256:<deleted>
    Please contact your system administrator.
    Add correct host key in ~/.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in ~/.ssh/known_hosts:37
    ECDSA host key for dev01.brianpfeil.com has changed and you have requested strict checking.
    Host key verification failed.
    ```

## VS Code Remote Development on Cloud9

* perform "Enabling SSH Connectivity" steps
* see [vscode | Remote development over SSH](https://code.visualstudio.com/docs/remote/ssh-tutorial)

**vscode remotely SSH connected screenshot**

![](https://www.evernote.com/l/AAFjZ-9n0FZKAYf1bAOao7RJcTKpfeEMEy4B/image.png)

## Resources

* [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)
* [vscode | Remote development over SSH](https://code.visualstudio.com/docs/remote/ssh-tutorial)
