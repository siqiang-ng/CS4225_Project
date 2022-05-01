import org.apache.spark.SparkConf;
import org.apache.spark.sql.*;

public final class Main {
    private static Dataset<Row> readFile(SparkSession spark, String file) {
        Dataset<Row> csv = spark.read()
                .option("header", true)
                .format("csv")
                .load(file).cache();

        return csv;
    }

    public static void main(String[] args) throws Exception {
        String input = args[0];
        String output = args[1];

        SparkConf sparkConf = new SparkConf().setAppName("Main");
        sparkConf.setMaster("local[*]");
        SparkSession spark = SparkSession.builder().config(sparkConf).getOrCreate();

        // Read the csv File and drop the Sentence column
        Dataset<Row> data = readFile(spark, input).drop("Sentence");

        // Convert the Created_at column from timestamp type to date type
        // Convert all language code in Lang column to lowercase
        // Add a count column to each row
        data = data
                .withColumn("Created_at", functions.to_date(data.col("Created_at")))
                .withColumn("Lang", functions.lower(data.col("Lang")))
                .withColumn("Count", functions.lit(1));

        // Sum the Count column when group by the other columns to reduce the number of rows
        data = data
                .groupBy("Sentiment", "Lang", "Created_at", "Social_media")
                .agg(functions.sum("Count"))
                .withColumnRenamed("sum(Count)", "Count");

        data.repartition(1).write().option("header", true).csv(output);

        spark.stop();
    }
}