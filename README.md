# TCPServerProject

<h1 align="center">
  
  ![python-logo-glassy](https://user-images.githubusercontent.com/103560553/204082228-92a30920-ca99-4517-9b9d-c3ab44d42a0b.png)

  Computer Networks
  <br>
</h1>

<h4 align="center">This gitHub repository is for the second assignments given in Computer Networks course, Bar Ilan University.


<p align="center">
  <a href="#description">Description</a> •
  <a href="#implementation">Implementation</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#installing-and-executing">Installing And Executing</a> •
  <a href="#authors">Authors</a> 
</p>

## Description

In this project, we implemented a TCP server. The server receives a request for a file from a web browser (such as Chrome, Firefox, etc) as a path or the name of the file. Then, the server searches for the file in a database (a folder named "files") and sends the data back to the client. 
The server takes into consideration the connection status of the client, so if the connection is "close" (FIN), the reply of the server will also contain the status "close" and will close the client's socket.

This project does not use threading, so when the server accepts a client, it assigns him the timeout value 1.0. Therefore, if the client does not send a new message within 1 second, the server closes the client's socket and accepts a new client. 

The server can "listen" to 5 clients at once, so if more than 5 clients are trying to connect, the server will ignore them.


## Implementation

The implementation is based on a single python module called "server.py". The server receives the port number as a system argument and binds it to the server's socket.

The Three main methods of the server are:

* "send_to_client" - responsible to send the requested data to the client.
* "extract_path_and_conn" - extracting the path or the file's name from the client's request.
* "search_file" - responsible for search for the requested file in the database.

As mentioned, the server doesn't use threading, so only one client is attended to at once. Therefore, the server closes every socket it accepts after the socket's timeout is activated, or when the status of the request is "closed".

## Dependencies
* The program build and tested for linux machines.
* The client is a web browser such as Chrome, Firefox, etc.
* Except "socket" and "sys", no other libraries where used.

## Installing And Executing

To clone and run this application, you'll need [Git](https://git-scm.com) installed on your computer. From your command line:

```bash
# Clone this repository.
$ git clone https://github.com/TalMizrahii/TCPServerProject

# Go into the repository.
$ cd TCPServerProject

# Run the server.
$ server.py [servers port number]
```
To run the client, open your browser and enter to the search line:
```bash
$ http://[Server IP]:[Server port][Path\file name]
```
## Authors
* [@Yuval Arbel](https://github.com/YuvalArbel1)
* [@Tal Mizrahi](https://github.com/TalMizrahii)


