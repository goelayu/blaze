/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package tree_diff;

import eu.mihosoft.ext.apted.distance.APTED;
import eu.mihosoft.ext.apted.node.Node;
import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {
    /**
     * Tests if equal strings have zero edit distance
     * string is JSON representation of a tree
     */
    @Test public void equalTreesHaveZeroEditDistance() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1,2],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"2\":{\"children\":[],\"size\":50,\"type\":\"text/css\"},\"length\":3}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1,2],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"2\":{\"children\":[],\"size\":50,\"type\":\"text/css\"},\"length\":3}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(0.0, result, 0);
    }

    /**
     * left has one extra element. expect 1.
     * string is JSON representation of a tree
     */
    @Test public void leftHasOneExtra() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1,2],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"2\":{\"children\":[],\"size\":50,\"type\":\"text/css\"},\"length\":3}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(1.0, result, 0);
    }

    /**
     * right has one extra element. expect 1.
     * string is JSON representation of a tree
     */
    @Test public void rightHasOneExtra() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1,2],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"2\":{\"children\":[],\"size\":50,\"type\":\"text/css\"},\"length\":3}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 1.0, 0);
    }

    /**
     * right has one renamed element with one change. expect 0.25.
     * string is JSON representation of a tree
     */
    @Test public void rightHasOneElementWithOneChange() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 0.25, 0);
    }

    /**
     * left has one renamed element with one change. expect 0.25.
     * string is JSON representation of a tree
     */
    @Test public void leftHasOneElementWithOneChange() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 0.25, 0);
    }

    /**
     * right has one renamed element with two changes. expect 0.5.
     * string is JSON representation of a tree
     */
    @Test public void rightHasOneElementWithTwoChanges() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"image/png\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 0.5, 0);
    }

    /**
     * left has one renamed element with two changes. expect 0.5.
     * string is JSON representation of a tree
     */
    @Test public void leftHasOneElementWithTwoChanges() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"image/png\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 0.5, 0);
    }

    /**
     * right has two renamed elements with two changes each. expect 1.
     * string is JSON representation of a tree
     */
    @Test public void rightHasTwoElementsWithTwoChanges() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"image/png\"},\"1\":{\"children\":[],\"size\":70,\"type\":\"text/css\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 1, 0);
    }

    /**
     * left has two renamed elements with two change each. expect 1.
     * string is JSON representation of a tree
     */
    @Test public void leftHasTwoElementsWithTwoChanges() {
        InputParser parser = new InputParser();
        Node<NodeData> t1 = parser.fromString("{\"0\":{\"children\":[1],\"size\":90,\"type\":\"image/png\"},\"1\":{\"children\":[],\"size\":70,\"type\":\"text/css\"},\"length\":2}");
        Node<NodeData> t2 = parser.fromString("{\"0\":{\"children\":[1],\"size\":100,\"type\":\"text/html\"},\"1\":{\"children\":[],\"size\":75,\"type\":\"image/jpeg\"},\"length\":2}");
        APTED<CostModel, NodeData> apted = new APTED<>(new CostModel());
        float result = apted.computeEditDistance(t1, t2);
        assertEquals(result, 1, 0);
    }
}
