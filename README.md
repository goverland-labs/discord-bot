# Discord_bot
Fetches data from goverland server and sends to discord channels. Used for further promotion of our solution

Principles of work:

Bot can be added on any server.

Once added, user has a number of commands available:

-Gov_sub initiates creation of session_id for each server plus adds server_id and session_id to local databse for further use. This is the first command that user needs to call to start using the service
-Gov_add_dao allows user to add subscription to a particular dao by specifying correct dao id such as "868f59db-4e45-498f-a87a-3efa9db0c92c"
-Gov_start initiates sending of proposals as per subscribed DAOs to the server. Sent messages contain proposals name and link to snapshot. Once proposal is sent, it is marked as read for a particular session_id. Service only sends proposals which are posted within a day not to inform about aold ones
-Gov_stop stops feed of proposals
