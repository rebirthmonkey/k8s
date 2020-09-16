package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	l, err := net.Listen("tcp", "0.0.0.0:8080")
	if err != nil {
		log.Println("error listening:", err.Error())
		return
	}
	defer l.Close()
	log.Println("listen ok")

	for {
		conn, err := l.Accept()
		if err != nil {
			log.Println("error accept:", err)
			return
		}

		log.Println("accept conn ok: " + conn.RemoteAddr().String())
		go func() {
			msg := "Hello, I am svc6 for ingress-controller demo!"
			fmt.Println(msg)
			conn.Write([]byte(msg))
			conn.Close()
		}()
	}
}
