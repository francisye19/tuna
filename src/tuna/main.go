package main

import (
    "os"
    "os/signal"
    "syscall"
    "log"
    "tunnel"
    "encoding/json"
    "path/filepath"
    "runtime"
)

type Backend struct {
    Name  string // name
    Addr  string // host:port of the backend
    Using bool   // using
}

type Config struct {
    ClientMode bool   // if running at client mode
    ListenAddr string // host:port tuna listen on
    Secret     string // password used to encrypt the data
    Crypto     string // encryption method, rc4 or aes256cfb
    Backends   []Backend
}

const configFileName string = "config.json"

func (cfg *Config) loadConfig() {
    // Same folder of the exec file
    execFile, err := os.Executable()
    if err != nil {
        log.Fatal(err)
    }
    execDir := filepath.Dir(execFile)
    paths := make([]string, 0)
    paths = append(paths, filepath.Join(execDir, configFileName))
    // Same folder of the source file
    _, srcFile, _, ok := runtime.Caller(0)
    if ok {
        srcDir := filepath.Dir(srcFile)
        paths = append(paths, filepath.Join(srcDir, configFileName))
    }
    // Working folder
    wd, err := os.Getwd()
    if err != nil {
        log.Fatal(err)
    }
    paths = append(paths, filepath.Join(wd, configFileName))
    //
    var path *string
    for _, p := range paths {
        if _, err := os.Stat(p); err == nil {
            path = &p
            log.Printf("Found config file %v", *path)
            break
        }
    }
    if path == nil {
        log.Fatalf("Can not find %v", configFileName)
    }
    file, err := os.Open(*path)
    if err != nil {
        log.Fatal(err)
    }
    decoder := json.NewDecoder(file)
    err = decoder.Decode(cfg)
    if err != nil {
        log.Fatal(err)
    }
}

func waitSignal() {
    var sigChan = make(chan os.Signal, 1)
    signal.Notify(sigChan)
    for sig := range sigChan {
        if sig == syscall.SIGINT || sig == syscall.SIGTERM {
            log.Printf("terminated by signal %v\n", sig)
            return
        } else {
            log.Printf("received signal %v, ignore\n", sig)
        }
    }
}

func main() {
    log.SetOutput(os.Stdout)
    // Load config
    config := Config{}
    config.loadConfig()
    clientMode := config.ClientMode
    faddr := config.ListenAddr
    secret := config.Secret
    cryptoMethod := config.Crypto
    var backend Backend
    for _, be := range config.Backends {
        if be.Using == true {
            backend = be
        }
    }
    if backend == (Backend{}) {
        log.Fatal("Please specify the using backend server")
    }
    if clientMode {
        log.Printf("You are using backend server %v", backend.Name)
    } else {
        log.Println("You are running server mode")
    }

    baddr := backend.Addr
    // Start
    t := tunnel.NewTunnel(faddr, baddr, clientMode, cryptoMethod, secret, 4096)
    log.Println("tuna started")
    go t.Start()
    waitSignal()
}
