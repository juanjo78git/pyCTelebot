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
	-- Valor de una unidad en USDT
	unit_value NUMERIC,
	-- Portentaje de beneficio de la estrategia
	take_profit NUMERIC,
	-- Porcentaje para comprobar cambio de dirección del precio
	buy_in_callback NUMERIC,
    PRIMARY KEY (strategy_id, exchange, symbol),
    FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
CREATE TABLE IF NOT EXISTS strategy_steps (
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	-- Número de orden del paso de la estrategia
	step INTEGER NOT NULL,
	-- Tipo de paso BUY/SELL
	step_type VARCHAR(50) NOT NULL,
	-- Porcentaje de variación de precio para activar el paso
	margin NUMERIC,
	-- Unidades con las que realizar el paso
	units NUMERIC,
  PRIMARY KEY (strategy_id, symbol, step),
  FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);


CREATE TABLE IF NOT EXISTS active_strategies (
	user_id VARCHAR(50) NOT NULL,
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	-- Valor de una unidad en USDT
	unit_value NUMERIC NOT NULL,
	-- Portentaje de beneficio de la estrategia
	take_profit NUMERIC,
	status VARCHAR(50) NOT NULL,
	-- Inversión actual
	current_invest NUMERIC,
	-- Porcentaje de beneficio actual
	current_profit NUMERIC,
	-- Fecha en la que se ha iniciado la estrategia
	start_audit_date TIMESTAMP,
	-- Fecha en la que ha acabado la estrategia
	end_audit_date TIMESTAMP,
	PRIMARY KEY (user_id, strategy_id, symbol),
	FOREIGN KEY (user_id)
      REFERENCES users (user_id),
	FOREIGN KEY (strategy_id)
      REFERENCES strategies (strategy_id)
);
CREATE TABLE IF NOT EXISTS active_strategy_steps (
	user_id VARCHAR(50) NOT NULL,
	strategy_id VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	-- Número de orden del paso de la estrategia
	step INTEGER NOT NULL,
	-- Tipo de paso BUY/SELL
	step_type VARCHAR(50) NOT NULL,
	-- Valor de una unidad en USDT
	unit_value NUMERIC NOT NULL,
	-- Portentaje de beneficio de la estrategia
	take_profit NUMERIC,
	-- Porcentaje de variación de precio para activar el paso
	margin NUMERIC,
	-- Unidades con las que realizar el paso
	units NUMERIC,
	status VARCHAR(50) NOT NULL,
	-- Precio real de compra
	real_price NUMERIC,
	-- Identificación de la orden realizada
	order_id VARCHAR,
	-- Fecha de ejecución de la orden
	order_audit_date TIMESTAMP,
	PRIMARY KEY (user_id, strategy_id, symbol, step),
	FOREIGN KEY (user_id, strategy_id)
      REFERENCES active_strategies (user_id, strategy_id, symbol)
);
CREATE TABLE IF NOT EXISTS exchange_prices (
	exchange VARCHAR(50) NOT NULL,
	symbol VARCHAR(50) NOT NULL,
	-- Precio anterior de compra
	last_buy_price NUMERIC,
	-- Precio actual de compra
	current_buy_price NUMERIC,
	-- Porcentaje de variación entre el precio de compra anterior y el actual
	buy_price_variation_percentage NUMERIC,
	-- Precio anterior de venta
	last_sell_price NUMERIC,
	-- Precio actual de venta
	current_sell_price NUMERIC,
	-- Porcentaje de variación entre el precio de venta anterior y el actual
	sell_price_variation_percentage NUMERIC,
	-- Fecha de obtención del precio anterior
	last_audit_date TIMESTAMP,
	-- Fecha de obtención del precio actual
	current_audit_date TIMESTAMP,
	PRIMARY KEY (exchange, symbol)
);
commit;