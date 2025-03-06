module github.com/Farady-AI/Microsoft-Graph

go 1.20

require (
    github.com/gin-gonic/gin v1.9.0
    github.com/microsoftgraph/msgraph-sdk-go v1.0.0
    github.com/spf13/viper v1.12.0
)

// main.go

package main

import (
	"fmt"
	"log"
	"os"
	"net/http"
	"io/ioutil"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

// Load environment variables
func loadEnv() {
	viper.AutomaticEnv()
	requiredVars := []string{"MSCLIENTID", "MSCLIENTSECRET", "MSTENANTID"}
	for _, v := range requiredVars {
		if viper.GetString(v) == "" {
			log.Fatalf("Missing required environment variable: %s", v)
		}
	}
}

// Get Microsoft Graph Token
func getMicrosoftGraphToken() string {
	clientID := viper.GetString("MSCLIENTID")
	clientSecret := viper.GetString("MSCLIENTSECRET")
	tenantID := viper.GetString("MSTENANTID")

	url := fmt.Sprintf("https://login.microsoftonline.com/%s/oauth2/v2.0/token", tenantID)
	data := fmt.Sprintf("client_id=%s&client_secret=%s&grant_type=client_credentials&scope=https://graph.microsoft.com/.default", clientID, clientSecret)

	resp, err := http.Post(url, "application/x-www-form-urlencoded", strings.NewReader(data))
	if err != nil {
		log.Fatalf("Error fetching token: %v", err)
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body)
	return string(body) // Replace with actual JSON parsing logic
}

// Main function
func main() {
	loadEnv()
	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "pong"})
	})

	r.GET("/token", func(c *gin.Context) {
		token := getMicrosoftGraphToken()
		c.JSON(http.StatusOK, gin.H{"access_token": token})
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	r.Run(":" + port)
}
