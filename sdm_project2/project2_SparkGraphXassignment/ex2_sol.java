package exercise_3;

import exercise_2.Exercise_2;
import org.antlr.v4.runtime.misc.Triple;
import org.apache.spark.api.java.JavaSparkContext;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Lists;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.graphx.*;
import org.apache.spark.sql.SQLContext;
import org.apache.spark.storage.StorageLevel;
import scala.Function3;
import scala.Tuple2;
import scala.collection.Iterator;
import scala.collection.JavaConverters;
import scala.reflect.ClassTag$;
import scala.runtime.AbstractFunction1;
import scala.runtime.AbstractFunction2;
import scala.runtime.AbstractFunction3;
import scala.runtime.AbstractFunction4;
import shapeless.Tuple;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Exercise_3 {

    private static class VProg extends AbstractFunction3<Long, Tuple2<Integer, ArrayList<Long>>, Tuple2<Integer, ArrayList<Long>>, Tuple2<Integer, ArrayList<Long>>> implements Serializable {
        @Override
        public Tuple2<Integer, ArrayList<Long>> apply(Long vertexID, Tuple2<Integer, ArrayList<Long>> vertexValue, Tuple2<Integer, ArrayList<Long>> message) {
            if (message._1 == Integer.MAX_VALUE) {             // superstep 0
                return vertexValue;
            } else { // superstep > 0
                if (vertexValue._1 <= message._1) {
                    return new Tuple2<Integer, ArrayList<Long>>(vertexValue._1, vertexValue._2);
                } else {
                    return new Tuple2<Integer, ArrayList<Long>>(message._1, message._2);
                }
                // return the tuple with the minimum value between the message value and the vertex value (last shortest path)
            }
        }
    }


    private static class sendMsg extends AbstractFunction1<EdgeTriplet<Tuple2<Integer, ArrayList<Long>>, Integer>, Iterator<Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>>> implements Serializable {
        @Override
        public Iterator<Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>> apply(EdgeTriplet<Tuple2<Integer, ArrayList<Long>>, Integer> triplet) {
            Tuple2<Object, Tuple2<Integer, ArrayList<Long>>> sourceVertex = triplet.toTuple()._1(); //source vertex
            Tuple2<Object, Tuple2<Integer, ArrayList<Long>>> dstVertex = triplet.toTuple()._2(); // destination vertex
            Integer edgeWeight = triplet.toTuple()._3(); //edge weight

            ArrayList<Long> path = sourceVertex._2._2;

            if (sourceVertex._2._1 == Integer.MAX_VALUE || dstVertex._2._1 - edgeWeight <= sourceVertex._2._1) {   // dst vertex value - edge weight is smaller than source vertex value?
                // do nothing
                return JavaConverters.asScalaIteratorConverter(new ArrayList<Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>>().iterator()).asScala();
            } else {
                // propagate source vertex value
                path.add(Long.parseLong(dstVertex._1.toString()));
                return JavaConverters.asScalaIteratorConverter(Arrays.asList(new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(triplet.dstId(), new Tuple2<Integer, ArrayList<Long>>(sourceVertex._2._1 + edgeWeight, path))).iterator()).asScala();
            }
        }
    }

    private static class merge extends AbstractFunction2<Tuple2<Integer, ArrayList<Long>>, Tuple2<Integer, ArrayList<Long>>, Tuple2<Integer, ArrayList<Long>>> implements Serializable {
        @Override
        public Tuple2<Integer, ArrayList<Long>> apply(Tuple2<Integer, ArrayList<Long>> o, Tuple2<Integer, ArrayList<Long>> o2) {
            if (o._1 <= o2._1) {
                return o;
            } else {
                return o2;
            }
        } // return the tuple with the minimum vertex value between o and o2
    }


    @SuppressWarnings("unchecked")
    public static void shortestPathsExt(JavaSparkContext ctx) {
        Map<Long, String> labels = ImmutableMap.<Long, String>builder()
                .put(1l, "A")
                .put(2l, "B")
                .put(3l, "C")
                .put(4l, "D")
                .put(5l, "E")
                .put(6l, "F")
                .build();

        @SuppressWarnings("unchecked")
        // Object: node ID, Tuple2<Integer, ArrayList<Long>: node value, shortest path
        List<Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>> vertices = Lists.newArrayList(
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(1l, new Tuple2<Integer, ArrayList<Long>>(0, new ArrayList<Long>(Arrays.asList(1l)))),
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(2l, new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>())),
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(3l, new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>())),
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(4l, new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>())),
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(5l, new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>())),
                new Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>(6l, new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>()))
        );

        @SuppressWarnings("unchecked")
        List<Edge<Integer>> edges = Lists.newArrayList(
                new Edge<Integer>(1l, 2l, 4), // A --> B (4)
                new Edge<Integer>(1l, 3l, 2), // A --> C (2)
                new Edge<Integer>(2l, 3l, 5), // B --> C (5)
                new Edge<Integer>(2l, 4l, 10), // B --> D (10)
                new Edge<Integer>(3l, 5l, 3), // C --> E (3)
                new Edge<Integer>(5l, 4l, 4), // E --> D (4)
                new Edge<Integer>(4l, 6l, 11) // D --> F (11)
        );


        JavaRDD<Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>> verticesRDD = ctx.parallelize(vertices);
        JavaRDD<Edge<Integer>> edgesRDD = ctx.parallelize(edges);

        Graph<Tuple2<Integer, ArrayList<Long>>, Integer> G = Graph.apply(verticesRDD.rdd(), edgesRDD.rdd(), new Tuple2<Integer, ArrayList<Long>>(0, new ArrayList<Long>()), StorageLevel.MEMORY_ONLY(), StorageLevel.MEMORY_ONLY(),
                scala.reflect.ClassTag$.MODULE$.apply(Tuple2.class), scala.reflect.ClassTag$.MODULE$.apply(Integer.class));

        GraphOps ops = new GraphOps(G, scala.reflect.ClassTag$.MODULE$.apply(Tuple2.class), scala.reflect.ClassTag$.MODULE$.apply(Integer.class));

        ops.pregel(new Tuple2<Integer, ArrayList<Long>>(Integer.MAX_VALUE, new ArrayList<Long>()),
                        Integer.MAX_VALUE,
                        EdgeDirection.Out(),
                        new Exercise_3.VProg(),
                        new Exercise_3.sendMsg(),
                        new Exercise_3.merge(),
                        ClassTag$.MODULE$.apply(Tuple2.class))
                .vertices()
                .toJavaRDD().sortBy(v -> ((Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>) v)._1, true, 0)//sort the JavaRDD
                .foreach(v -> {
                    Tuple2<Object, Tuple2<Integer, ArrayList<Long>>> vertex = (Tuple2<Object, Tuple2<Integer, ArrayList<Long>>>) v;
                    System.out.println("Minimum cost to get from " + labels.get(1l) + " to " + labels.get(vertex._1) + " is " + String.valueOf(vertex._2._2.stream().map(labels::get).collect(Collectors.toList()).toString()) + " with cost " + vertex._2._1);
                });
    }

}