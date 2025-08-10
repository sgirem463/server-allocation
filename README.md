# Server Allocation
Server name allocation service<br>
There can be many different server types, e.g. database, web, api.
A server name is server type + id, e.g. web1, web2, database23, api32.<br>
Each allocation should return name with the lowest avaliable id, starting from 1.

The service supports deallocation when a server is no longer needed, its id should
be return to the pool for future allocation.<br>
The system should be able to detect deallocation with an invalid id, i.e. id that
hasn't been allocated.

This is a generic and useful service that can be easily adapted to many applications.
