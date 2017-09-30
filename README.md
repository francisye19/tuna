### Tuna - a tunnel program

`Tuna` is a network tunneling software working as an encryption wrapper between clients and servers (remote/local).

`Tuna` is forked from [qTunnel](https://github.com/getqujing/qtunnel).

##### Why Tuna

- Support loading parameters from config file
- UI

### Requirements

[golang 1.9](http://golang.org/dl/)

### Build

To build `qtunnel`

`$ make`

To test `qtunnel`

`$ make test`

### Usage

	$ ./bin/qtunnel -h
	Usage of ./bin/qtunnel:
		-backend="127.0.0.1:6400": host:port of the backend
		-clientmode=false: if running at client mode
		-crypto="rc4": encryption method
		-listen=":9001": host:port qtunnel listen on
		-logto="stdout": stdout or syslog
		-secret="secret": password used to encrypt the data
 		
`qtunnel` supports two encryption methods: `rc4` and `aes256cfb`. Both servers and clients should use the same `crypto` and same `secret`.

### Example

Let's say, you have a `redis` server on `host-a`, you want to connect to it from `host-b`, normally, just use:

	$ redis-cli -h host-a -p 6379

will do the job. The topology is:

	redis-cli (host-b) <------> (host-a) redis-server

If the host-b is in some insecure network environment, i.e. another data center or another region, the clear-text based redis porocol is not good enough, you can use `qtunnel` as a secure wrapper

On `host-b`:

	$ qtunnel -listen=127.1:6379 -backend=host-a:6378 -clientmode=true -secret=secret -crypto=rc4

On `host-a`:

	$ qtunnel -listen=:6378 -backend=127.1:6379 -secret=secret -crypto=rc4

Then connect on `host-b` as:

	$ redis-cli -h 127.1 -p 6379

This will establish a secure tunnel between your `redis-cli` and `redis` server, the topology is:

	redis-cli (host-b) <--> qtunnel (client,host-b) <--> qtunnel (host-a) <--> redis-server

After this, you can communicate over a encrypted wrapper rather than clear text.
