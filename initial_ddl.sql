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
	description VARCHAR,
  PRIMARY KEY (strategy_id)
);
CREATE TABLE IF NOT EXISTS strategy_symbols (
	strategy_id VARCHAR(50) NOT NULL,
	exchange VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	unit_value NUMERIC,
	take_profit NUMERIC,
	buy_in_callback NUMERIC,
    PRIMARY KEY (strategy_id, exchange, symbol),
    FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
CREATE TABLE IF NOT EXISTS strategy_steps (
	strategy_id VARCHAR(50) NOT NULL,
	step INTEGER NOT NULL,
	step_type VARCHAR(50) NOT NULL,
	margin NUMERIC,
	units NUMERIC,
  PRIMARY KEY (strategy_id, step),
  FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);


CREATE TABLE IF NOT EXISTS active_strategies (
	user_id VARCHAR(50) NOT NULL,
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	unit_value NUMERIC NOT NULL,
	take_profit NUMERIC,
	status VARCHAR(50) NOT NULL,
	current_invest NUMERIC,
	current_profit NUMERIC,
	start_audit_date TIMESTAMP,
	end_audit_date TIMESTAMP,
	PRIMARY KEY (user_id, strategy_id),
	FOREIGN KEY (user_id)
      REFERENCES users (user_id),
	FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
CREATE TABLE IF NOT EXISTS active_strategy_steps (
	user_id VARCHAR(50) NOT NULL,
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	step INTEGER NOT NULL,
	step_type VARCHAR(50) NOT NULL,
	unit_value NUMERIC NOT NULL,
	take_profit NUMERIC,
	margin NUMERIC,
	units NUMERIC,
	status VARCHAR(50) NOT NULL,
	real_price NUMERIC,
	order_id VARCHAR,
	order_audit_date TIMESTAMP,
	PRIMARY KEY (user_id, strategy_id, step),
	FOREIGN KEY (user_id, strategy_id)
      REFERENCES active_strategies (user_id, strategy_id)
);
CREATE TABLE IF NOT EXISTS exchange_prices (
	exchange VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	last_buy_price NUMERIC,
	current_buy_price NUMERIC,
	buy_price_variation_percentage NUMERIC,
	last_sell_price NUMERIC,
	current_sell_price NUMERIC,
	sell_price_variation_percentage NUMERIC,
	last_audit_date TIMESTAMP,
	current_audit_date TIMESTAMP,
	PRIMARY KEY (exchange, symbol)
);
commit;