package main

import (
	"context"
	"io"
	"log"
	"net/http"

	"github.com/dispatchrun/dispatch-go"
)

type CatFactUnavailable struct{}

func (error *CatFactUnavailable) Error() string {
	return "failed to fetch a cat fact"
}

func (error *CatFactUnavailable) Temporary() bool {
	return true
}

func main() {
	fetchCatFact := dispatch.Func("fetchCatFact", func(ctx context.Context, arg string) (any, error) {
		response, err := http.Get("https://cat-facts.dispatch.run")

		if err != nil {
			return nil, &CatFactUnavailable{}
		}

		if response.StatusCode != 200 {
			return nil, &CatFactUnavailable{}
		}

		defer response.Body.Close()

		body, err := io.ReadAll(response.Body)

		if err != nil {
			return nil, &CatFactUnavailable{}
		}

		log.Printf("Cat fact: %s", body)

		return nil, nil
	})

	endpoint, err := dispatch.New(fetchCatFact)
	if err != nil {
		log.Fatal(err)
	}

	mux := http.NewServeMux()

	mux.Handle(endpoint.Handler())

	mux.Handle("/", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fetchCatFact.Dispatch(r.Context(), "")
		w.WriteHeader(http.StatusOK)
	}))

	if err := http.ListenAndServe("localhost:8000", mux); err != nil {
		log.Fatal(err)
	}
}
