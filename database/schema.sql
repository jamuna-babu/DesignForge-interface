/* DROP TABLE templates; */

CREATE TABLE IF NOT EXISTS templates (
  id TEXT(36),
  data JSONB,
  widget VARCHAR,
  device VARCHAR,
  created_date DATETIME,
  modified_date DATETIME,
  UNIQUE (widget, device)
);

