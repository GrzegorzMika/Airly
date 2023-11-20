package airly

import "time"

type Airly struct {
	InstallationID int        `json:"installation_id"`
	Current        Current    `json:"current"`
	History        []History  `json:"history"`
	Forecast       []Forecast `json:"forecast"`
}
type Values struct {
	Name  string  `json:"name"`
	Value float64 `json:"value"`
}
type Indexes struct {
	Name        string  `json:"name"`
	Value       float64 `json:"value"`
	Level       string  `json:"level"`
	Description string  `json:"description"`
	Advice      string  `json:"advice"`
	Color       string  `json:"color"`
}
type Standards struct {
	Name      string  `json:"name"`
	Pollutant string  `json:"pollutant"`
	Limit     float64 `json:"limit"`
	Percent   float64 `json:"percent"`
	Averaging string  `json:"averaging"`
}
type Current struct {
	FromDateTime time.Time   `json:"fromDateTime"`
	TillDateTime time.Time   `json:"tillDateTime"`
	Values       []Values    `json:"values"`
	Indexes      []Indexes   `json:"indexes"`
	Standards    []Standards `json:"standards"`
}
type History struct {
	FromDateTime time.Time   `json:"fromDateTime"`
	TillDateTime time.Time   `json:"tillDateTime"`
	Values       []Values    `json:"values"`
	Indexes      []Indexes   `json:"indexes"`
	Standards    []Standards `json:"standards"`
}
type Forecast struct {
	FromDateTime time.Time   `json:"fromDateTime"`
	TillDateTime time.Time   `json:"tillDateTime"`
	Values       []Values    `json:"values"`
	Indexes      []Indexes   `json:"indexes"`
	Standards    []Standards `json:"standards"`
}
