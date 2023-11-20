package airly

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func urlBuilder(installationID int) string {
	return fmt.Sprintf("https://airapi.airly.eu/v2/measurements/installation?installationId=%d", installationID)
}

func addHeaders(req *http.Request) {
	req.Header.Add("Accept", "application/json")
	req.Header.Add("apikey", os.Getenv("API_KEY"))
}

func prepareRequest(installationID int) (*http.Request, error) {
	req, err := http.NewRequest("GET", urlBuilder(installationID), nil)
	if err != nil {
		return nil, err
	}
	addHeaders(req)
	return req, nil
}

func makeRequest(installationID int, client http.Client) (Airly, error) {
	req, err := prepareRequest(installationID)
	if err != nil {
		return Airly{}, err
	}
	resp, err := client.Do(req)
	if err != nil {
		return Airly{}, err
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return Airly{}, err
	}
	var airly Airly
	err = json.Unmarshal(body, &airly)
	if err != nil {
		return Airly{}, err
	}
	return airly, nil
}
