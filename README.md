# Peer to Peer File Transfer CSC573
The purpose of this repository is to house a peer to peer multi-threaded file sharing system over TCP sockets.

## Instructions to setup and run the environment (also located in the make file)
IMPORTANT: All RFC file names should take the form <4 digit RFCs number><file name all underscores>.txt with no special characters.

Example: 8537updates_to_the_fast_reroute_procedures_for_co_routed_associated_bidirectional_label_switched_paths_lsps.txt

To fulfill the testing requirements, open three terminal windows.

In the first window, navigate to the location of the docker-compose.yml file and execute the following command:

docker-compose up

Doing so will bring the registration server, and the two peers, and allow them to submit/receive requests. A nice byproduct of this process is that the terminal in which the command was run, will present color coded output from all three servers running.

After ensuring that the server is ready to receive information in the first terminal (you will be presented with a blank line and blinking courser), open the next terminal and run the following command:

```bash
docker exec -it p2p_peerclient1_1 python3 /var/opt/src/imports/client.py
```

Doing so will bring up the client program, which is simply a while loop, ready to accept user input. As can be seen from the command, this client process is serving the first peer “p2p_peerclient1_1”.

Once complete, perform similar steps with the following command in a new terminal to open the client process for the second peer “p2p_peerclient2_1”:

```bash
docker exec -it p2p_peerclient2_1 python3 /var/opt/src/imports/client.py
```

As in the first case, you will now see a prompt come up that will allow you to control the function of the peer.

After a message is submitted, you will be presented with output that will label both the transmitted message and the response. Some of the messages will not have a response as they are simply necessary to communicate to the peer itself.

Should the servers need to be torn down, you can simply run the following command after the servers are exited with CTRL + C:

```bash
docker-compose down
```

This will remove all containers/images that have to do with this stack.

As an aside, if you do not want to enter the while loop for each server, you can simply provide the argument you want to submit to the client. An example of such a request is below.

```bash
docker exec -it p2p_peerclient1_1 python3 /var/opt/src/imports/client.py REGISTER
```

Finally, the RFC files that are to be tested, can be copied (with the appropriate naming structure) to each peers respective RFCs folder which is located just under each peer’s root.
