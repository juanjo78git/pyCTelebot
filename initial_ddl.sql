set transaction read write;
CREATE TABLE IF NOT EXISTS users (
	user_id VARCHAR(50) PRIMARY KEY,
	telegram_id VARCHAR(50) UNIQUE NOT NULL,
	email VARCHAR(255) UNIQUE NOT NULL,
	role VARCHAR(50) NOT NULL,
	exchange VARCHAR(50),
	apiKey VARCHAR,
	secret VARCHAR,
	passphrase VARCHAR
);
CREATE TABLE IF NOT EXISTS strategies (
	strategy_id VARCHAR(50) NOT NULL,
	buy_in_callback NUMERIC,
  PRIMARY KEY (strategy_id)
);
CREATE TABLE IF NOT EXISTS strategy_steps (
	strategy_id VARCHAR(50) NOT NULL,
	step INTEGER NOT NULL,
	margin NUMERIC NOT NULL,
	units NUMERIC NOT NULL,
  PRIMARY KEY (strategy_id, step),
  FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
CREATE TABLE IF NOT EXISTS active_strategies (
	user_id VARCHAR(50) NOT NULL,
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	unit_value NUMERIC NOT NULL,
	profit NUMERIC,
	PRIMARY KEY (user_id, strategy_id),
	FOREIGN KEY (user_id)
      REFERENCES users (user_id),
	FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
commit;
