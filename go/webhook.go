package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
)

func main() {
	apiKey := os.Getenv("DISPATCH_API_KEY")
	endpoint := os.Getenv("DISPATCH_TO_URL")
	endpoint = strings.TrimPrefix(endpoint, "https://")

	payload, _ := json.Marshal(map[string]any{
		"from":    "example",
		"to":      "webhook",
		"message": "hello, world!",
	})

	req, _ := http.NewRequest(http.MethodGet,
		"https://dispatch.stealthrocket.cloud/"+endpoint, bytes.NewBuffer(payload),
	)
	req.Header.Set("Proxy-Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json; charset=utf-8")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		log.Fatal("status:", res.Status)
	}

	io.Copy(os.Stdout, res.Body)
}
