import os.path
import paramiko
import logging
from sys import stderr

"""
EteGatherDataListener implements the ROBOT listener API version 2 and is
instantiated via the robot cammmand line option

   --listener EteGatherDataListener:<jobbumber>:<key filename>

The purpose is to gather and preserve debugging data from each of the application
VMs when an ETE test fails.

This listener counts the number of test
cases that have failed and, if > 0 at then end of the robot exection (close()),
will connect to each application vm and

2. upload the gather_data.sh
2. execute gather_data.sh
3. Transfer the resulting zip file to the Robot reports folder

This will enable the Jenkins job to retrieve the debug data along with the
Robot logs and reports  and archive it with the failed job for later retreival.

Note that the gather_data.sh depends upon the application providing
a /opt/gather_application_data.sh on their respective VMs for the zip file
to be created.
"""


class EteGatherDataListener(object):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 2

    APPLICATIONS = {
        "aai" : "10.0.1.1",
        "appc" : "10.0.2.1",
        "sdc" : "10.0.3.1",
        "dcae" : "10.0.4.1",
        "mso" : "10.0.5.1",
        "policy" : "10.0.6.1",
        "sdnc" : "10.0.7.1",
        "vid" : "10.0.8.1",
        "portal" : "10.0.9.1",
        "message_router" : "10.0.11.1",
        "dcae_pstg00" : "10.0.4.101",
        "dcae_coll00" : "10.0.4.102",
        "dcae_cdap00" : "10.0.4.103",
        "dcae_cdap01" : "10.0.4.104",
        "dcae_cdap02" : "10.0.4.105"
        }

    keyfile = ""
    local_gather_data_sh = ""

    def __init__(self, job='10', keyfile='/share/config/key.pvt', shell="gather_data.sh"):
        self.tests_passed = 0
        self.tests_failed = 0
        self.output_folder = ''
        self.job = job
        self.folder= ''
        self.keyfile = keyfile
        self.local_gather_data_sh = shell
        print "EteGatherDataListener instantiated"

    def end_test(self, name, attrs):
        if attrs['status'] == 'PASS':
            self.tests_passed+=1
        else:
            self.tests_failed+=1

    def output_file(self, path):
        if (self.folder != ''):
            return
        self.folder = os.path.dirname(path)
        print(self.folder)

    def close(self):
        print "EteGatherDataListener tests failed=" + str(self.tests_failed)
        if (self.tests_failed > 0):
            self.gather_debug_data()

    def gather_debug_data(self):

        for application in self.APPLICATIONS.keys():
            self.gather_application_data(application, self.APPLICATIONS.get(application))

    def gather_application_data(self, application, ip):
        extra = {"_threadid" : 1}
        paramiko.util.log_to_file(self.folder + "/paramiko.log", level=0)
        log = logging.getLogger("paramiko")
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,username="root",  key_filename=self.keyfile)
        except paramiko.SSHException:
            log.error("Connection Failed to " + ip, extra=extra)
            return
        try:
            gather_data_sh = "/tmp/gather_data.sh"
            ftp = ssh.open_sftp()
            ftp.put(self.local_gather_data_sh, gather_data_sh)
            ftp.close()
            stdin, stdout, stderr = ssh.exec_command("/bin/bash "+ gather_data_sh + " " + application + " " + self.job)
            error = stderr.read()
            if (error != ''):
                log.info("stderr:" + error, extra=extra)
                ssh.close()
                return;
            # No error? ASsume we have a file to download.
            out = stdout.read()
            log.info("stdout:" + out, extra=extra)
            filename = application + "_" + self.job + ".tar.gz"
            localzip = self.folder + "/" + filename
            remotezip = "/tmp/gather_data/" + filename
            ftp = ssh.open_sftp()
            ftp.get(remotezip, localzip)
            ftp.close()
            stdin, stdout, stderr = ssh.exec_command("rm -rf " + remotezip);
            ssh.close()
        except paramiko.SSHException:
            ssh.close()
            return


