GOPATH := $(shell pwd)
.PHONY: clean test

all:
	@GOPATH=$(GOPATH) go install tuna

clean:
	@rm -fr bin pkg

test:
	@GOPATH=$(GOPATH) go test tunnel
