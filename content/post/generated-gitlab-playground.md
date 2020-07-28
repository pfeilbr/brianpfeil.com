+++
author = "Brian Pfeil"
categories = ["<nil>", "playground"]
date = 2019-09-18
description = ""
summary = "learn Gitlab"
draft = false
slug = "gitlab"
tags = ["gitlab","playground",]
title = "Gitlab"
repoFullName = "pfeilbr/gitlab-playground"
repoHTMLURL = "https://github.com/pfeilbr/gitlab-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/gitlab-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/gitlab-playground</a>
</div>


learn gitlab. Uses [GitLab CE Docker image](https://hub.docker.com/r/gitlab/gitlab-ce/) to run locally

Based on steps in docs @ [GitLab Docker images](https://docs.gitlab.com/omnibus/docker/)


```sh
mkdir ~/dev/gitlab

# not ssh exposed on 2022 to not conflict with mac | System Prefs | Sharing | Remote Login
sudo docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 2022:22 \
  --name gitlab \
  --restart always \
  --volume ~/dev/gitlab/config:/etc/gitlab \
  --volume ~/dev/gitlab/logs:/var/log/gitlab \
  --volume ~/dev/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest

# ***NOTE*** can take up to 10 min to load
# check logs via `sudo docker logs -f gitlab` or Kitematic UI | Container Logs

open http://localhost

# will need to set root password
# login with username: root, password: YOUR_PASSWORD

# add ssh key via User Settings | SSH Keys
cat ~/.ssh/id_rsa.pub | pbcopy

# create project in UI (`project01`)

# note port 2022
git clone ssh://git@localhost:2022/root/project01.git

# stopping
sudo docker stop gitlab
```

---

Container Logs via Kitematic UI
![](https://www.evernote.com/l/AAHs12CyIodBZp3cOuZumtkxJG2f-3Az3DQB/image.png)

Project view
![](https://www.evernote.com/l/AAEuFGfKNfxALLJSmQZ0GC7DCox1cV1MwqUB/image.png)



