### Tuna - a tunnel program

`Tuna` is a network tunneling software working as an encryption wrapper between clients and servers (remote/local).

`Tuna` is forked from [qTunnel](https://github.com/getqujing/qtunnel).

##### Why Tuna

- Support loading parameters from config file
- UI

### Requirements

[golang 1.9](http://golang.org/dl/)

### Build

To build `tuna`

```
$ make
```

To test `tuna`

```
$ make test
```

### Usage

```
$ tuna
```

### Config

The topology is:
```
client <------> server
```

On `client`:
```
{
  "ClientMode": true,
  "ListenAddr": ":9527",
  "Log": "stdout",
  "Secret": "{{ secret }}",
  "Crypto": "aes256cfb",
  "Backends": [
    {
      "Name": "be-01",
      "Addr": "{{ ip }}:443",
      "Using": true
    }
  ]
}
```

On `server`:
```
{
  "ClientMode": false,
  "ListenAddr": ":443",
  "Log": "stdout",
  "Secret": "{{ secret }}",
  "Crypto": "aes256cfb",
  "Backends": [
    {
      "Name": "lo-01",
      "Addr": ":3128",
      "Using": true
    }
  ]
}
```

Both servers and clients should use the same `crypto` and same `secret`.

