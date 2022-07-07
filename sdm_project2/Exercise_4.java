package exercise_4;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.MetadataBuilder;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.graphframes.GraphFrame;

import java.io.*;
import java.util.ArrayList;


public class Exercise_4 {

	static final double DAMPING_FACTOR = 0.85; // 1-0.85 = 0.15 --> prob = 0.15
	static final int MAX_ITERATIONS = 100;

	public static void wikipedia(JavaSparkContext ctx, SQLContext sqlCtx) {

		//Loading vertices
		java.util.List<Row> vertices_list = new ArrayList<Row>();
		File file_vertices = new File("src/main/resources/wiki-vertices.txt");
		try (BufferedReader br = new BufferedReader(new FileReader(file_vertices))) {
			String idx;
			while ((idx = br.readLine()) != null) {
				String[] vertices = idx.split("\t");
				Row rowVertex = RowFactory.create(Long.parseLong(vertices[0]), vertices[1]);
				vertices_list.add(rowVertex);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		JavaRDD<Row> vertices_rdd = ctx.parallelize(vertices_list);

		StructType vertices_schema = new StructType(new StructField[]{
				new StructField("id", DataTypes.LongType, false, new MetadataBuilder().build()),
				new StructField("title", DataTypes.StringType, false, new MetadataBuilder().build())
		});
		Dataset<Row> vertices =  sqlCtx.createDataFrame(vertices_rdd, vertices_schema);


		//Loading edges
		java.util.List<Row> edges_list = new ArrayList<Row>();
		File file_edges = new File("src/main/resources/wiki-edges.txt");
		try (BufferedReader br = new BufferedReader(new FileReader(file_edges))) {
			String idx;
			while ((idx = br.readLine()) != null) {
				String[] edges = idx.split("\t");
				Row rowEdge = RowFactory.create(Long.parseLong(edges[0]), Long.parseLong(edges[1]));
				edges_list.add(rowEdge);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		JavaRDD<Row> edges_rdd = ctx.parallelize(edges_list);

		StructType edges_schema = new StructType(new StructField[]{
				new StructField("src", DataTypes.LongType, false, new MetadataBuilder().build()),
				new StructField("dst", DataTypes.LongType, false, new MetadataBuilder().build())
		});
		Dataset<Row> edges =  sqlCtx.createDataFrame(edges_rdd, edges_schema);

		GraphFrame gf = GraphFrame.apply(vertices,edges);

		// Computing PageRank
		gf.pageRank().maxIter(MAX_ITERATIONS).resetProbability(1-DAMPING_FACTOR).run().vertices().select("id", "title", "pagerank").orderBy(org.apache.spark.sql.functions.col("pagerank").desc()).show(10);

	}
}
