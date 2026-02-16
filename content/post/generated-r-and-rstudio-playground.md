+++
author = "Brian Pfeil"
categories = ["", "playground"]
date = 2022-07-06
description = ""
summary = " "
draft = false
slug = "r-and-rstudio"
tags = ["machine-learning"]
title = "R and RStudio"
repoFullName = "pfeilbr/r-and-rstudio-playground"
repoHTMLURL = "https://github.com/pfeilbr/r-and-rstudio-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/r-and-rstudio-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/r-and-rstudio-playground</a>
</div>


learn R and RStudio

---

## General

- R - cli environment
- Rscript - used to run R scripts from the command line . E.g.`Rscript -e "date()" -e "format(Sys.time(), \"%a %b %d %X %Y\")"`
- RStudio - desktop app
- RStudio Server -  provide a browser based interface to a version of R running on a remote Linux server, bringing the power and productivity of the RStudio IDE to server-based deployments of R.
- RStudio Workbench
  - The ability to develop in RStudio and Jupyter
  - Load balancing
  - Tutorial API
  - Data connectivity and RStudio Professional Drivers
  - Collaboration and project sharing
  - Scale with Kubernetes and SLURM
  - Authentication, access, & security
  - Run multiple concurrent R and Python sessions
  - Remote execution with Launcher
  - Auditing and monitoring
  - Advanced R and Python session management
- RStudio Connect is a publishing platform for the work your teams create in R and Python. RStudio Connect allows you to share the following, and more, in one convenient place: Shiny applications. R Markdown reports. Plumber APIs.


## SageMaker RStudio

- browser based rstudio workbench 
- launch rstudio app win sm domain 
- launch rstudio session
	- select ec2 instance type
- session has user home directory backed by s3
	- installed r pkgs are preserved in home dir
	- every session uses same home dir
- shiny apps
- plumber apis
- r reticulate package offers integration with python for working w sm easily from R
	- import py package and ref from r variable.  proxies calls from r to py
-  coming soon - rstudio connect managed by sm
RStudio Connect is a publishing platform for the work your teams create in R and Python. RStudio Connect allows you to share the following, and more, in one convenient place: Shiny applications. R Markdown reports. Plumber APIs.

---

## Running RStudio in Docker

```sh

# run
docker run --rm -p 8787:8787 -e PASSWORD=password01 rocker/rstudio

# open IDE in browser
open https://localhost:8787

# username: rstudio, password: password01

```

## Resources

- [R](https://www.r-project.org/)
- [CRAN (The Comprehensive R Archive Network)](https://cran.r-project.org/)
- [Rocker Project](https://www.rocker-project.org/) - Docker Containers for the R Environment
- <https://docs.rstudio.com/>
- [pfeilbr/rstudio-on-sagemaker-playground](https://github.com/pfeilbr/rstudio-on-sagemaker-playground)
