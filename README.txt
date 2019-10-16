0. (Christopher Sheil, cjs337) (Jerry Lan, jl1881)

1. We implemented this structure by reading in the input with (key, challenge, hostname)
format and splitting it into its respective parts. We compute the digest on the client server
then send that and the challenge string to the authentication server. The AS server passes along
the challange string to both the top level servers, who already have their unique keys. They also compute
their own digest and send it back to the AS. The as then compares the results from the TS servers.
The one that matches what the client computed is the authenticated one. The IP of that server gets sent
back to the client so it can ask that servers DNS table for the result. The client does this and then the top
servers act as a regular DNS, sending back the entry if the hostname is found, and the error if not. The client
then recieves this message from the TS and writes to the outfile.

2. Yes. We got all the server logistics to communicate with the correct heirarchy and logistics for the most part. However
we ran into problems formatting the output. We believe the output to be correct for the most part, because the servers communicate and
we got to the point where the TS was sending back the correct result to the client. However I think there are timing issues or other logistical
issues that caused the output to contain the right source material for the correct answer, but it is not synched propery with our output
file. Its all formatting and timing I believe.

3. Our major problems were with synching the serevers up. Our only problem was getting the output
to look correct. So when the client is trying to accept an answer from one of two servers. I think the logistics
of how it recieves packets back is incorrect. Because its not waiting on only one socket, its waiting on two. and
we dont know which one the answer is coming from and which one is not authenticated. This made it way more 
difficult for us and we were not able to geet the correct answer becausee of it.

4. We learned the struggle of syncronising server events becasue if you arent careful it can get really confusing
the order in which things happen and trying to keep track of the timelines for each server to keep the logic 
consistent. Also we learned the difficulty of managing a higher number of connections across multuple servers. We now see 
how quickly the complexity can ramp up....