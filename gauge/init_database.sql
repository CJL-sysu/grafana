CREATE Table IF NOT EXISTS grafana.gauge(
    TIME DATETIME,
    cpu DOUBLE,
    mem DOUBLE,
    gpu_load DOUBLE,
    gpu_mem DOUBLE
);
