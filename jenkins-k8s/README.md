# Jenkins O11y

This POC is for [INFRA-30304](https://jira.splunk.com/browse/INFRA-30304).

The purpose of this POC is to determine if we can use pod annotation on the pod that is running Jenkins to dynamically create a monitor in SignalFx Smart Agent. This will mean that we will not need to update the Smart Agent configuration everytime we create a new Jenkins instance that needs to be monitored.

This POC is using a local minikube instance as its k8s cluster.

# Install Jenkins

Jenkins is deployed with the [Jenkins Operator][1].

To deploy the Jenkins Operator run:

```
make install-jenkins-crd
make install-jenkins-operator
```

Create a Jenkins CR to instantiate a Jenkins master

`make deploy-jenkins`

# Install SignalFx Smart Agent

The Smart Agent is deployed using a helm chart. 
The values for the helm chart is stored in `signalfx-agent/values.yaml`.

Runt he followin to deploy the agent.

`make deploy-signalfx`

# How service discovery works?

The Smart Agent has a feature that allows [service discovery][5] to detect the presence of any new services you want to monitor.

Service discovery requires 3 components:

1. The [Observer][6] - enable the [k8s-api][4] observer on the Smart Agent. This observer is enabled by default in the helm chart.
2. The Monitor - the monitor we are using in this case is the [collectd/jenkins][2] monitor. To allow service discovery we need to setup the monitoring with a `discoveryRule` what will match any instances of the Jenkins.  
The follow rule will create a monitor for every container that contains the name "jenkins-master"
    ```yaml
    monitors:
    - type: collectd/jenkins
      discoveryRule: 'container_name =~ "jenkins-master"'
    ```
3. Annotation on the Target - specific [annotations][3] are required on the target, the jenkins pod in this instance, for the Smart Agent to recognise that this application needs to be monitored. In our case the annotation required are:  
    ```yaml
    agent.signalfx.com/monitorType.http: collectd/jenkins
    agent.signalfx.com/configFromSecret.http.metricsKey: jenkins-metrics-key/metricsKey
    agent.signalfx.com/config.http.host: jenkins-operator-http-example
    agent.signalfx.com/config.http.port: "8080"
    ```

Once the above 3 components are in place the Smart Agent will auto discover any new Jenkins instances that gets created which matches the discoveryRule defined in the monitor.

# TO-DOs

- Automate the generation of the metricKey in Jenkins and pass it to collectd/jenkins (i.e. the Annotations on the target)
- Not all metrics listed in [collectd/jenkins][2] are being collected. There are at least 2 missing. These are the errors causing it. This needs to be investigated and fixed.  
    ```
    time="2021-02-17T09:02:12Z" level=error msg="Error making API call (403 Client Error: Forbidden for url: http://jenkins-operator-http-example:8080/computer/api/json/) http://jenkins-operator-http-example:8080/computer/api/json/" createdTime=1.6135525326240585e+09 lineno=99 logger=root monitorID=13 monitorType=collectd/jenkins runnerPID=17 sourcePath=/collectd-python/jenkins/jenkins.py
    time="2021-02-17T09:02:12Z" level=error msg="Unable to get data from http://jenkins-operator-http-example:8080/computer/api/json/ for computer" createdTime=1.6135525326244915e+09 lineno=471 logger=root monitorID=13 monitorType=collectd/jenkins runnerPID=17 sourcePath=/collectd-python/jenkins/jenkins.py
    time="2021-02-17T09:02:12Z" level=error msg="Error making API call (403 Client Error: Forbidden for url: http://jenkins-operator-http-example:8080/api/json/) http://jenkins-operator-http-example:8080/api/json/" createdTime=1.613552532716318e+09 lineno=99 logger=root monitorID=13 monitorType=collectd/jenkins runnerPID=17 sourcePath=/collectd-python/jenkins/jenkins.py
    time="2021-02-17T09:02:12Z" level=error msg="Unable to get data from http://jenkins-operator-http-example:8080/api/json/ for jenkins" createdTime=1.6135525327166686e+09 lineno=471 logger=root monitorID=13 monitorType=collectd/jenkins runnerPID=17 sourcePath=/collectd-python/jenkins/jenkins.py
    ```
        
# References

1. [Jenkins Operator][1]
2. [collectd/jenkins][2]
3. [Observer Annotations][3]
4. [k8s-api][4]
5. [SignalFx Discovery Service][5]
6. [Smart Agent Observers][6]

[1]: https://jenkinsci.github.io/kubernetes-operator/docs/getting-started/latest/schema/ "Jenkins Operator"
[2]: https://docs.signalfx.com/en/latest/integrations/agent/monitors/collectd-jenkins.html "collectd/jenkins"
[3]: https://docs.signalfx.com/en/latest/integrations/kubernetes/k8s-monitors-observers.html#configuring-the-observer-using-kubernetes-annotations "Smart Agent Observer"
[4]: https://docs.signalfx.com/en/latest/integrations/agent/observers/k8s-api.html "k8s-api Observer"
[5]: https://docs.signalfx.c
[6]: https://docs.signalfx.com/en/latest/integrations/agent/observers/_observer-config.html