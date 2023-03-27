#
# To start the NiFi server on an EC2 instance
#

sudo docker-compose -d up

#
# A note on VM heap size
#
By default, the NiFi server starts with the VM heap size of 512m. To change this size, the docker-compose.yml include 
environment variables NIFI_VM_HEAP_INIT and NIFI_VM_HEAP_MAX, which are currently set to 4096m and 8192m, respectively.

#
# A note on NiFi cluster configuration
#
Currently, the docker-compose.yml does not dictate the creation of NiFi cluster, i.e., it creates a single node NiFI
server. At the workload increases, we'll need to migrate to a multi-node NiFi cluster. The number of nodes is to be 
determined and the docker-compose.yml file shall be revised accordingly. 

#
# To start the NiFi server as a Kubernetes Pod on AWS Fargate
#

kubectl apply -f kube-deploy.yaml

#
# To start the NiFi server on local machine for local access only
#
If you want to start a NiFi instance on a local machine, use the following command. Note however that (a) this NiFi instance is unsecured and does not enforce authentication and (b) the Web UI for this NiFI instance cannot be accessed remotely.

sudo docker-compose -f docker-compose.local.yml -d up

#
# To access the NiFi server via Web UI
#
Do the following steps:

   1. Install ./nifi-toolkit-1.15.3/tls/client/'CN=admin_OU=NIFI.p12' as a user certificate on the browser. When prompted to enter password, enter stoutagtechnifi20220131. It is the client certificate to be provided to the NiFi server for two-way TLS authentication.

   2. Install ./nifi-toolkit-1.15.3/tls/nifi-cert.pem as an authority certificate on the browser. It is the CA cert to be provided to the NiFI server for two-way TLS authentication.

   3. Restart the browser.

   4. Enter https://nifi.stoutagtech.dev:9443/nifi into the address bar.

Now you are logged in the admin user who has all the privileges. PLEASE DO NOT CHANGE ANYTHING ON CANVAS unless you are pre-approved to do so by the admin.

#
# To access the NiFi server installed on local machine via Web UI
#
If you started the NiFi server on a local machine, you don't need to install certificates in the browser. You may just enter http://localhost:8080/nifi

#
# To create dataflows via NiFi Web UI
#
The dataflow, which is represented by a group of NiFi components (such as 
InputPort, Processes, ProcessGroups, Connections, and/or OutputPort) can be 
created on the NiFi Web UI canvas. The properties of each of these components 
shall be configured to suit the specific needs of the application. To learn
how a dataflow can be created and its components configured, refer to NiFi 
User Guide at 

https://nifi.apache.org/docs/nifi-docs/html/user-guide.html

Any addition or change to the dataflow on NiFi Web UI canvas is automatically 
written to /opt/nifi/nifi-current/conf/flow.xml.gz, which is continually 
archived in the /opt/nifi/nifi-current/conf/archive directory. The archived 
flow.xml.gz files can be used to rollback or restore the dataflow as of a given
point of time. 

##
## To enable version control for dataflows
##
Each ProcessGroup can be placed under version control. To do this, right-click on 
a ProcessGroup and select "Version → Start version control" from the context menu.
The dataflow created on NiFi Web UI canvas can be committed as a version at any
moment. Once comitted, the dataflow will be stored as a new version in the 
NiFi Registry server, which is located at 

https://nifi-registry.stoutagtech.dev:18443/nifi-registry

#
# To import versioned dataflow onto the canvas via NiFi Web UI
#
Any workflow, in any version, can be imported from the NiFi Registry by selecting
one from the menu that appears when you drag and drop the ProcessGroup icon into
the NiFi Web UI.