package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
	ginEngine := gin.Default()
	ginEngine.GET("/hello", func(c *gin.Context) {
		c.String(http.StatusOK, "Hello World")
	})
	ginEngine.Run(":8080")
}
