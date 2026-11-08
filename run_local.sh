#!/usr/bin/env bash
# Prueba local de los jobs MapReduce: reproduce el flujo de Hadoop Streaming
#   entrada -> mapper -> sort (shuffle & sort) -> reducer -> salida
# Se usa para validar la lógica antes de enviar los jobs al clúster.
set -euo pipefail
export LC_ALL=C          # orden de bytes, igual que el shuffle de Hadoop
RAIZ="$(cd "$(dirname "$0")" && pwd)"
DATA="$RAIZ/data"; MR="$RAIZ/mapreduce"; OUT="$RAIZ/results"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$OUT"

# Simula la caché distribuida (-files): los archivos quedan en el directorio de trabajo.
cp "$DATA/productos.csv" "$DATA/clientes.csv" "$TMP/"
cd "$TMP"

echo "[0] Preprocesamiento JSON -> JSON Lines"
python3 "$RAIZ/scripts/json_a_jsonl.py" "$DATA/resenas.json" "$DATA/resenas.jsonl"

echo "[1] Ingresos por categoría"
cat "$DATA/detalle_venta.csv" | python3 "$MR/job1_ingresos_categoria/mapper.py" \
  | sort -t$'\t' -k1,1 | python3 "$MR/job1_ingresos_categoria/reducer.py" > "$OUT/job1_ingresos_categoria.tsv"
cat "$DATA/detalle_venta.csv" | python3 "$MR/job1_ingresos_categoria/mapper.py" producto \
  | sort -t$'\t' -k1,1 | python3 "$MR/job1_ingresos_categoria/reducer.py" > "$OUT/job1_ingresos_producto.tsv"

echo "[2] Join ventas + detalle_venta (+ clientes por caché)"
cat "$DATA/ventas.csv" "$DATA/detalle_venta.csv" | python3 "$MR/job2_join_ventas/mapper.py" \
  | sort -t$'\t' -k1,1 -k2,2r | python3 "$MR/job2_join_ventas/reducer.py" > "$OUT/job2_ventas_consolidadas.tsv"

echo "[3] Agregados encadenados sobre la salida del Job 2"
for dim in ciudad mes medio_pago cliente; do
  python3 "$MR/job3_agregados/mapper.py" "$dim" < "$OUT/job2_ventas_consolidadas.tsv" \
    | sort -t$'\t' -k1,1 | python3 "$MR/job3_agregados/reducer.py" > "$OUT/job3_por_${dim}.tsv"
done

echo "[4] Calificación por producto"
python3 "$MR/job4_calificacion_producto/mapper.py" < "$DATA/resenas.jsonl" \
  | sort -t$'\t' -k1,1 | python3 "$MR/job4_calificacion_producto/reducer.py" > "$OUT/job4_calificacion_producto.tsv"

echo "[5] Frecuencia de etiquetas"
python3 "$MR/job5_etiquetas/mapper.py" < "$DATA/resenas.jsonl" \
  | sort -t$'\t' -k1,1 | python3 "$MR/job5_etiquetas/reducer.py" > "$OUT/job5_etiquetas.tsv"

echo "Listo. Resultados en $OUT"
