This archive contains the main scripts and configuration files that we created to run the experiments. We have excluded the binaries, source code, and basic configuration of the third-party protocols under analysis, but we include the code that defines our experimental methods.

./datastream-experiments

This folder contains samples of the code used to run most of the datastream experiments, including recording network traffic (via tshark), establishing proxies, producing traffic, etc. The experiments are run by running tshark.sh to monitor and then, e.g. allTests.sh.
allTests.sh repeatedly executes runTest.sh, which drives each individual test and produces entries in mainLog.txt. runTest.sh itself
executes client, server, and setup. After the tests are run by allTests.sh, extractFin.py is then run to analyze the tshark output file, break the experiments up by timestamp, and produce the analysis.

./datagram-experiments

This folder contains samples of the code used for the most recent datagram protocol experiments (Shadowsocks UDP and SWGP). This folder also contains scripts for the kcptun experiments because it transfers proxy data as datagrams and thus uses the datagram experiment patterns.

For Shadowsocks, after starting the shadowsocks binaries, the tests are executed by running the
client, server, mitm, and server scripts in order. For KCP, the test can be run with runTest.sh,
which calls scripts for the specified protocol to run a client and server, as well as an
intermediary proxy to record traffic. The kill.sh script is used to terminate the experiment once
sufficient data is collected.

The SWGP experiments were performed via docker compose. The relevant configuration files are in the swgp-go folder. The SWGP tests were performed by running swgp-go/run.sh.