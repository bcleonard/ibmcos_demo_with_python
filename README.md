# IBM COS DEMO w/Python
This is demo repository which will provide various demo's of specific features and functionality of IBM Cloud Object Storage On-Premise solutions.

**Notice:  The scripts and information in this toolkit are provided as-is, without any support.**

## Included:
* [Basic Demo](s3_demo_basic.py) - demo that creates creates vault, uploads file(s), deletes files(s), deletes bucket

## Requirements:
These demos were developed with the following:

* [Debian 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
* [Python3](https://www.python.org/)
* [Python venv](https://docs.python.org/3/library/venv.html)
* [pip](https://pypi.org/project/pip/)
* [Python Libraries](requirements.txt)
* [git](https://git-scm.com/)

## How to install:
All the following steps should be run on your debian instance.  You'll need to make sure python3, pip & venv are already installed.  You'll need internet access from your debian instance to download the libraries.

### Download the demo repo:
```
git clone https://github.com/bcleonard/ibmcos_demo_with_python.git
```

### Set up the virtual environment:
```
cd ibmcos_demo_with_python
python3 -m venv virtualenv
```

### Install the required python libraries:
```
cd ibmcos_demo_with_python
pip3 install -r requirements.txt
```

## How to configure:

To configure the demo, you'll need to edit the [demo_config.txt](demo_config.txt).  Each demo will have its own section.  At a minimum, you'll need to replace/update the Access Key, Secret Access Key & Accesser URL.  Each demo script may have additional fields that are neccessry to be filled out.

Please note that your define user will need to have the "Vault Provisioner" role and you will need to enable the "Provisioning API Configuration" with the ability for users to "Create and Delete".

## How to Use:

Activate the virtual environment:
```
cd ibmcos_demo_with_python
source virtualenv\bin\activate
```

Run your demos:
```
<demo script>
```

When you're done, deactivate your virtual environment:
```
deactivate
```

### IBM Documentation
IBM published resources for IBM COS:
* [IBM Cloud Object Storage System documentation](https://www.ibm.com/support/knowledgecenter/en/STXNRM) (IBM Cloud Object Storage System documentation)
* [IBM Cloud Object Storage System Product Guide](https://www.redbooks.ibm.com/abstracts/sg248439.html) (IBM Redbook)
* [IBM Cloud Object Storage Concepts and Architecture](https://www.redbooks.ibm.com/abstracts/redp5537.html) (IBM Redpaper)

Other resources for administrating IBM COS:
* [IBM COS Toolkit](https://github.com/bcleonard/ibm_cos_toolkit) (Toolkit for IBM Cloud Object Storage Administrators)
* [AWS Command Line Interface](https://aws.amazon.com/cli/) (unified tool to manage AWS services)
* [Object Generator](https://github.com/IBM/og) (http tool for load testing object storage APIs)
* [testssl.sh](https://testssl.sh/) (testing TLS/SSL encryption)
* [s3cmd](https://s3tools.org/s3cmd) (command line S3 Client and Backup for Linux and Mac)

Other IBM COS resources:
* [Infrastructure-as-code for IBM COS Trial VMs](https://github.com/hseipp/ibm-cos-vm-iac) (demonstrate virtual variant of the IBM Cloud Object Storage solution)
