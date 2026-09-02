+++
author = "Brian Pfeil"
categories = ["JavaScript", "playground"]
date = 2022-02-18
description = ""
summary = " "
draft = false
slug = "surveyjs-react"
tags = ["react","javascript"]
title = "SurveyJS React"
repoFullName = "pfeilbr/surveyjs-react-playground"
repoHTMLURL = "https://github.com/pfeilbr/surveyjs-react-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/surveyjs-react-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/surveyjs-react-playground</a>
</div>


- arch recommender based on cloud foundation principles - inline and link to them
- "cloud foundation principles" shows first with "get started" button
- top level categories
  - SaaS, compute, storage (file, db), COTS, integation, real-time (streaming), ML/AI, static employee facing site -> company cdn+waf solution link, pcf link (static build pack)
  - for each recommendation, show which principles it is tied to and give it a score
- recommender builder similar to aws pricing calculator.  comprehensive recommendations for your entire solution across compte, storage, integration, etc. e.g. add compute recommendation to plan, add storage recommendation to plan, ...
- do you have secrets like api keys, crdentials, tokens, etc. that your code needs to access -> secrets manager
- is business classification >= business critical (ha/dr) multi-az / multi-region
- is GxP -> 
- service icon next to each service recommendation
- have an example use case and show a recommendation
- for each recommended service have a link to the service pricing page and aws pricing calculator
- need help / have question about a service.  search / post in CoP
- don't have an account yet / get started / request an account link when complete
- IaC - tf/cfn always in recommendation
  - link to tf modules repo
- metrics / alarming - always in recommendations
- step fns / eb - always in recommendations
- host on static cloud site.  make generic / not tied to company version on brianpfeil.com (hugo)

---

# React quickstart boilerplate for SurveyJS: Survey Library and Survey Creator 

This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

## How to run this sample application
 - git clone https://github.com/surveyjs/surveyjs_react_quickstart.git
 - cd surveyjs_react_quickstart
 - npm i
 - npm start
 - open http://localhost:3000/ in your web browser



You can find the detailed information on how to perform common tasks in [this guide](https://github.com/facebookincubator/create-react-app/blob/master/packages/react-scripts/template/README.md).

## Add survey component on your page
```JavaScript
//In your react App.js or yourComponent.js file add these lines to import
import * as Survey from "survey-react";
import "survey-react/survey.css";

class App extends Component {
 //Define Survey JSON
 //Here is the simplest Survey with one text question
 json = {
  elements: [
   { type: "text", name: "customerName", title: "What is your name?", isRequired: true}
  ]
 };

 //Define a callback methods on survey complete
 onComplete(survey, options) {
  //Write survey results into database
  console.log("Survey results: " + JSON.stringify(survey.data));
 }
 render() {
  //Create the model and pass it into react Survey component
  //You may create survey model outside the render function and use it in your App or component
  //The most model properties are reactive, on their change the component will change UI when needed.
  var model = new Survey.Model(this.json);
  return (<Survey.Survey model={model} onComplete={this.onComplete}/>);
  /*
  //The alternative way. react Survey component will create survey model internally
  return (<Survey.Survey json={this.json} onComplete={this.onComplete}/>);
  */
  //You may pass model properties directly into component or set it into model
  // <Survey.Survey model={model} mode="display"/>
  //or 
  // model.mode="display"
  // <Survey.Survey model={model}/>
  // You may change model properties outside render function. 
  //If needed react Survey Component will change its behavior and change UI.
 }
} 
```

