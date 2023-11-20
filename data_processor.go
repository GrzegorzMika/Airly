package airly

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

func saveData(ctx context.Context, db *sql.DB, data []insertDataParams) error {
	for _, row := range data {
		err := saveRow(ctx, db, row)
		if err != nil {
			return fmt.Errorf("saveRow: %w, row: %s", err, row)
		}
	}
	return nil
}

func saveRow(ctx context.Context, db *sql.DB, row insertDataParams) error {
	query := `INSERT INTO data (installation_id, from_date_time, till_date_time, measurement_name, measurement_value) VALUES ($1, $2, $3, $4, $5) ON CONFLICT ON CONSTRAINT data_pk DO NOTHING;`
	_, err := db.ExecContext(ctx, query, row.InstallationID, row.FromDateTime, row.TillDateTime, row.MeasurementName, row.MeasurementValue)
	if err != nil {
		return fmt.Errorf("insert data: %v", err)
	}
	return nil
}

type insertDataParams struct {
	InstallationID   int     `json:"installation_id"`
	FromDateTime     string  `json:"from_date_time"`
	TillDateTime     string  `json:"till_date_time"`
	MeasurementName  string  `json:"measurement_name"`
	MeasurementValue float64 `json:"measurement_value"`
}

func parseData(airly []Airly) []insertDataParams {
	query := make([]insertDataParams, 0)
	for _, a := range airly {
		for _, measurement := range a.History {
			for _, value := range measurement.Values {
				query = append(query, insertDataParams{
					InstallationID:   a.InstallationID,
					FromDateTime:     measurement.FromDateTime.Format(time.RFC3339),
					TillDateTime:     measurement.TillDateTime.Format(time.RFC3339),
					MeasurementName:  value.Name,
					MeasurementValue: value.Value,
				})
			}
		}
	}
	return query
}
