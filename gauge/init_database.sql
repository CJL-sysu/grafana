CREATE Table IF NOT EXISTS grafana.gauge(
    TIME DATETIME,
    cpu DOUBLE,
    mem DOUBLE,
    gpu_load DOUBLE,
    gpu_mem DOUBLE
);
CREATE TABLE IF NOT EXISTS grafana.memory(
    TIME DATETIME,
    total DOUBLE,
    used DOUBLE
);
CREATE TABLE IF NOT EXISTS grafana.gpumem(
    TIME DATETIME,
    total DOUBLE,
    used DOUBLE
);