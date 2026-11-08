#!/usr/bin/env bash
# Ejecución de los jobs en Apache Hadoop (pseudo-distribuido o clúster) con Hadoop Streaming.
# Requisitos: HDFS y YARN activos (start-dfs.sh && start-yarn.sh) y python3 en los nodos.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")" && pwd)"
MR="$RAIZ/mapreduce"; DATA="$RAIZ/data"
STREAMING=$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n1)
HDFS_BASE=/user/$USER/bigdata

# 0. Preprocesamiento y carga a HDFS
python3 "$RAIZ/scripts/json_a_jsonl.py" "$DATA/resenas.json" "$DATA/resenas.jsonl"
hdfs dfs -mkdir -p $HDFS_BASE/input/{ventas,detalle,resenas} $HDFS_BASE/cache
hdfs dfs -put -f "$DATA/ventas.csv"        $HDFS_BASE/input/ventas/
hdfs dfs -put -f "$DATA/detalle_venta.csv" $HDFS_BASE/input/detalle/
hdfs dfs -put -f "$DATA/resenas.jsonl"     $HDFS_BASE/input/resenas/
hdfs dfs -ls -R $HDFS_BASE/input

# Borra una salida previa (Hadoop no sobrescribe directorios de salida)
limpiar() { hdfs dfs -rm -r -f "$1" >/dev/null 2>&1 || true; }

# 1. Ingresos por categoría y por producto (join en el mapa + combiner)
for dim in categoria producto; do
  limpiar $HDFS_BASE/output/job1_$dim
  hadoop jar "$STREAMING" \
    -D mapreduce.job.name="job1_ingresos_$dim" \
    -files "$MR/job1_ingresos_categoria/mapper.py,$MR/job1_ingresos_categoria/reducer.py,$DATA/productos.csv" \
    -mapper "python3 mapper.py $dim" -combiner "python3 reducer.py" -reducer "python3 reducer.py" \
    -input $HDFS_BASE/input/detalle -output $HDFS_BASE/output/job1_$dim
done

# 2. Join en el reduce: ventas + detalle_venta (+ clientes por caché distribuida)
limpiar $HDFS_BASE/output/job2_join
hadoop jar "$STREAMING" \
  -D mapreduce.job.name="job2_join_ventas" \
  -D stream.num.map.output.key.fields=1 \
  -files "$MR/job2_join_ventas/mapper.py,$MR/job2_join_ventas/reducer.py,$DATA/clientes.csv" \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -input $HDFS_BASE/input/ventas -input $HDFS_BASE/input/detalle \
  -output $HDFS_BASE/output/job2_join

# 3. Jobs encadenados: la salida del Job 2 es la entrada del Job 3
for dim in ciudad mes medio_pago cliente; do
  limpiar $HDFS_BASE/output/job3_$dim
  hadoop jar "$STREAMING" \
    -D mapreduce.job.name="job3_agregado_$dim" \
    -files "$MR/job3_agregados/mapper.py,$MR/job3_agregados/reducer.py" \
    -mapper "python3 mapper.py $dim" -reducer "python3 reducer.py" \
    -input $HDFS_BASE/output/job2_join -output $HDFS_BASE/output/job3_$dim
done

# 4. Calificación por producto (datos semiestructurados JSON Lines)
limpiar $HDFS_BASE/output/job4
hadoop jar "$STREAMING" \
  -D mapreduce.job.name="job4_calificacion_producto" \
  -files "$MR/job4_calificacion_producto/mapper.py,$MR/job4_calificacion_producto/reducer.py" \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -input $HDFS_BASE/input/resenas -output $HDFS_BASE/output/job4

# 5. Frecuencia de etiquetas (patrón WordCount)
limpiar $HDFS_BASE/output/job5
hadoop jar "$STREAMING" \
  -D mapreduce.job.name="job5_etiquetas" \
  -files "$MR/job5_etiquetas/mapper.py,$MR/job5_etiquetas/reducer.py" \
  -mapper "python3 mapper.py" -reducer "python3 reducer.py" \
  -input $HDFS_BASE/input/resenas -output $HDFS_BASE/output/job5

# Consulta de resultados
for d in job1_categoria job1_producto job2_join job3_ciudad job3_mes job3_medio_pago job3_cliente job4 job5; do
  echo "== $d"; hdfs dfs -cat $HDFS_BASE/output/$d/part-*
done
